#!/usr/bin/env python3

"""
This file is a Python plug-in for GIMP which imports text from a file
into layers, on a path.
"""


import re
import codecs

import gettext
from gi.repository import GLib  # pylint: disable=no-name-in-module
from gi.repository import Gio  # pylint: disable=no-name-in-module
from gi.repository import Gimp  # pylint: disable=no-name-in-module
from gi.repository import GObject
from pathlib import Path
import sys

import gi
gi.require_version('Gimp', '3.0')


_ = gettext.gettext
def N_(message): return message  # noqa: E704


JUSTIFICATION = [
    (Gimp.TextJustification.LEFT, "Aligné à gauche"),
    (Gimp.TextJustification.RIGHT, "Aligné à droite"),
    (Gimp.TextJustification.CENTER, "Centré"),
    (Gimp.TextJustification.FILL, "Justifié")
]

HINTSTYLE = [
    (Gimp.TextHintStyle.NONE, "Aucun"),
    (Gimp.TextHintStyle.SLIGHT, "Léger"),
    (Gimp.TextHintStyle.MEDIUM, "Moyen"),
    (Gimp.TextHintStyle.FULL, "Full/Justifié")
]


BOXMODE_LIST = ["fixed", "dynamic"]

FONTUNIT_LIST = ["pixels (px)", "pouces (in)",
                 "milimètres (mm)", "points (pt)"]

JUSTIFICATION_GIMP = [x[0] for x in JUSTIFICATION]
JUSTIFICATION_FRENCH = [x[1] for x in JUSTIFICATION]
HINTSTYLE_GIMP = [x[0] for x in HINTSTYLE]
HINTSTYLE_FRENCH = [x[1] for x in HINTSTYLE]


def read_file(source_path):
    """Lit un fichier texte et retourne son contenu en UTF-8."""
    try:
        with open(source_path, "r", encoding="utf-8") as source_file:
            raw_source = source_file.read()
    except UnicodeDecodeError:
        Gimp.message(
            "Le script n'a pas pu utiliser l'encodage UTF-8.\n"
            "Il va essayer un encodage par défaut.\n"
            "En cas de problème, pensez à enregistrer vos fichiers en UTF-8."
        )
        try:
            with open(source_path, "r") as source_file:
                raw_source = source_file.read()
        except Exception as e:
            Gimp.message(f"Erreur de lecture du fichier : {e}")
            return None
    except Exception as e:
        Gimp.message(f"Erreur d'ouverture du fichier : {e}")
        return None

    if raw_source:
        # Supprimer le BOM si présent
        if raw_source.startswith(codecs.BOM_UTF8.decode("utf-8")):
            raw_source = raw_source.replace(
                codecs.BOM_UTF8.decode("utf-8"), "", 1)
        return raw_source
    else:
        Gimp.message(f"Échec : fichier source invalide («{source_path}»)")
        return None


def replace(string, substitutions):
    """Replace multiple substitions in string."""
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)


def splitpages(source):
    """Split long text in a list of texts (separator is "Page XX")."""
    # Regex used for split the page
    regex = r"(?i)^page\s[0-9]+.*(\r\n|\r|\n)"

    return filter(lambda x: not re.match(r'^\s*$', x),
                  re.split(regex, source, flags=re.MULTILINE | re.UNICODE))


def get_path_points(image):
    """Retourne le nombre de points et la liste des points du chemin actif."""
    vectors = image.get_active_vectors()
    if vectors is None:
        Gimp.message("Vous devriez tracer un chemin avec l'outil Chemin.")
        return 0, []

    strokes = vectors.get_strokes()  # Liste de tuples (closed, points)
    if not strokes:
        Gimp.message("Le chemin actif ne contient aucun tracé.")
        return 0, []

    closed, cpoints = strokes[0]  # On prend le premier tracé
    # 6 valeurs par point (x, y, contrôle1, contrôle2)
    n_points = len(cpoints) // 6
    return n_points, cpoints


def get_box_dim(layer_height, lenght):
    """Return text_box width and heigt

    Args:
        layer_height (int): image height
        lenght (int): text lenght (in chars)

    Returns:
        tuple: width and height of text box
    """
    # Short text -> small box
    if lenght < 20:
        tlayer_width = 150 * layer_height / 3056
        tlayer_height = 100 * layer_height / 3056
    elif lenght < 40:
        tlayer_width = 250 * layer_height / 3056
        tlayer_height = 120 * layer_height / 3056
    elif lenght < 80:
        tlayer_width = 350 * layer_height / 3056
        tlayer_height = 150 * layer_height / 3056
    elif lenght < 120:
        tlayer_width = 380 * layer_height / 3056
        tlayer_height = 200 * layer_height / 3056
    # Long text -> large box
    else:
        tlayer_width = 500 * layer_height / 3056
        tlayer_height = 250 * layer_height / 3056
    return tlayer_width, tlayer_height


def get_box_position(n_points, x_index, y_index, cpoints, layer_height):
    """Return text box coordinates x and y, from path.

    Args:
        n_points (int): number of points in the path
        x_index (int): index for point x coordinate
        y_index (int): index for point y coordinate
        cpoints (list): list of points
        layer_height (int): image height

    Returns:
        int, int: x and y coordinates
    """
    # Test if number of poins is correct
    flag = False
    if x_index < n_points:
        # Text position from path
        x_pos = cpoints[x_index]
        y_pos = cpoints[y_index]
    else:
        x_pos = 500
        y_pos = layer_height - 200
        flag = True

    return x_pos, y_pos, flag


def add_text_layer(image, text, font, font_size, fontunit_index,
                   layer_position, antialias, font_color, indent,
                   justification, hintstyle, language, letter_spacing,
                   line_spacing, tlayer_width, tlayer_height, x_pos, y_pos):
    """Ajoute un calque de texte à l'image."""

    # Convertir l'index d'unité en Gimp.Unit
    unit = Gimp.Unit.from_value(fontunit_index)

    # Créer le calque texte
    tlayer = Gimp.TextLayer.new(image, text, font, font_size, unit)

    # Ajouter le calque à l'image
    image.add_layer(tlayer, layer_position)

    # Appliquer les propriétés
    tlayer.set_antialias(antialias)
    tlayer.set_color(font_color)
    tlayer.set_indent(indent)
    tlayer.set_justification(justification)
    tlayer.set_hint_style(hintstyle)
    tlayer.set_language(language)
    tlayer.set_letter_spacing(letter_spacing)
    tlayer.set_line_spacing(line_spacing)

    # Redimensionner et positionner
    tlayer.resize(tlayer_width, tlayer_height)
    tlayer.set_offsets(x_pos, y_pos)
    tlayer.set_visible(True)

    return tlayer


def plugin_import_text_layers_path_dctrad(
        image,
        active_layer,
        source_path,
        page_index,
        font,
        fontunit_index,
        font_size,
        antialias,
        hintstyle_index,
        font_color,
        justification_index,
        line_spacing,
        letter_spacing):
    # box_mode_index
    # use_markdown):
    """"Import text on path (plugin)."""
    indent = 0
    box_mode_index = 0  # box fixed mode
    # font_color = '#000000'
    language = 'fr'
    font_size_int = int(font_size)
    use_markdown = False
    source_escaped = False

    return import_text_layers(image, active_layer, source_path, page_index,
                              source_escaped, font, fontunit_index,
                              font_size_int, antialias,
                              HINTSTYLE_GIMP[hintstyle_index], font_color,
                              JUSTIFICATION_GIMP[justification_index],
                              indent, letter_spacing, line_spacing,
                              BOXMODE_LIST[box_mode_index],
                              language, use_markdown)


def import_text_layers(
        image,
        active_layer,
        source_path,
        page_index,
        source_escaped,
        font,
        fontunit_index,
        font_size,
        antialias,
        hintstyle,
        font_color,
        justification,
        indent,
        letter_spacing,
        line_spacing,
        box_mode,
        language,
        use_markdown):
    """Import text on path (function)."""
    # special character for page jumps : u"\u2003"
    # special character for supspension marks : u"\u2026"
    # special character like WORD page jump, UTF-8 (...), etc... to be replaced
    substitutions = {u"\u2003": '', u"\u2026": '...', ' \n': '\n'}

    # Read file
    source = read_file(source_path)

    # Split pages
    pages_array = splitpages(source)
    # Clean working page
    page = replace(pages_array[int(page_index) - 1], substitutions)
    # Split into lines
    text_lines = page.splitlines()

    image.undo_push_group_start()

    layer_position = 0
    layer_height = 3056

    if active_layer:
        layer_height = image.get_height()
        layer_position = image.get_layer_position(active_layer)

    n_points, cpoints = get_path_points(image)

    # indexes in cpoints array
    x_index = 2
    y_index = 3

    flag_message = False

    for rawtext in text_lines:
        if source_escaped:
            text = rawtext.decode('unicode_escape')
        else:
            text = rawtext

        if text != '//' and text != '' and text != '// ':

            tlayer_width, tlayer_height = get_box_dim(layer_height, len(text))

            x_pos, y_pos, flag = get_box_position(n_points, x_index, y_index,
                                                  cpoints, layer_height)

            if flag and not flag_message:
                Gimp.message('Attention !!!\n'
                             'Le nombre de points que vous avez '
                             'selectionné ne correspond pas au nombre '
                             'de lignes de texte du fichier.\n'
                             'Le script va continuer en placant les '
                             'lignes de texte restantes en bas '
                             'de la page.\n'
                             'Vous devriez vérifier vos bulles, ou '
                             'annuler pour recommencer, en pointant '
                             'toutes les bulles et encarts de texte.')
                flag_message = True

            add_text_layer(image, text, font, font_size, fontunit_index,
                           layer_position, antialias, font_color, indent,
                           justification, hintstyle, language, letter_spacing,
                           line_spacing, tlayer_width, tlayer_height,
                           x_pos, y_pos)

            # cpoints structure is so that a point is made of 6 values
            x_index += 6
            y_index += 6
    # end of loop on rawtext

    image.undo_push_group_end()
    return  # end of function


# Register in Gimp
class ImportTextOnPathPlugin(Gimp.PlugIn):
    def do_query_procedures(self):
        return ["sl-gimp-import-text-on-path"]

    def do_set_i18n(self, name):
        return False

    def do_create_procedure(self, name):
        if name != "sl-gimp-import-text-on-path":
            return None

        # Création d'une ImageProcedure
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            self.run,
            None
        )

        procedure.set_image_types("RGB*, GRAY*")
        procedure.set_menu_label("Importer un texte sur un chemin")
        procedure.set_documentation(
            "Importe le texte depuis un fichier et le place le long d'un chemin",
            "Plugin de test minimal",
            name
        )
        procedure.set_attribution("Sergeileduc", "Sergeileduc", "2025")

        # Ajout d'un paramètre string
        # procedure.add_argument_string(
        #     "source_path",                # identifiant interne
        #     "Fichier texte",              # label affiché
        #     "Chemin du fichier texte",    # description
        #     "C:/Users/serge/test.txt"     # valeur par défaut
        # )

        procedure.add_menu_path("<Image>/DC-trad/")
        return procedure

        # procedure = Gimp.ImageProcedure.new(self, name,
        #                                     Gimp.PDBProcType.PLUGIN,
        #                                     self.run, None)
        # procedure.set_image_types("RGB*, GRAY*")
        # procedure.set_menu_label("Importer un texte sur un chemin")
        # procedure.set_documentation(
        #     "Importe le texte depuis un fichier et le place le long d'un chemin",
        #     globals()["__doc__"],
        #     name
        # )
        # procedure.set_attribution("Sergeileduc", "Sergeileduc", "2025")

        # procedure.add_argument_string(
        #     "source_path",                # identifiant interne
        #     "Fichier texte",              # label affiché
        #     "Chemin du fichier texte",    # description
        #     "C:/Users/serge/test.txt"     # valeur par défaut (non vide)
        # )

        # # procedure.add_argument_string(
        # #     "source_path",
        # #     "Fichier texte",
        # #     "Chemin du fichier texte",
        # #     "/tmp/test.txt"
        # # )

        # # procedure.add_font_argument("font", "_Font", "Font", True,
        # #                             Gimp.Font.get_by_name("Serif"),
        # #                             False,
        # #                             GObject.ParamFlags.READWRITE)

        # # Ajout des paramètres
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.string(
        # #         "source_path", "Fichier texte", "Chemin du fichier texte",
        # #         GObject.ParamFlags.READWRITE)
        # # )

        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.int(
        # #         "page-index", "Page", "Numéro de page", GObject.ParamFlags.READWRITE)
        # # )
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.string(
        # #         "font", "Police", "Nom de la police", GObject.ParamFlags.READWRITE)
        # # )
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.int(
        # #         "fontunit-index", "Unité de taille", "Index d’unité", GObject.ParamFlags.READWRITE)
        # # )
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.double(
        # #         "font-size", "Taille", "Taille de la police", GObject.ParamFlags.READWRITE)
        # # )
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.boolean(
        # #         "antialias", "Lissage", "Antialiasing", GObject.ParamFlags.READWRITE)
        # # )
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.int(
        # #         "hintstyle-index", "Ajustement", "Style d’ajustement", GObject.ParamFlags.READWRITE)
        # # )
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.boxed(
        # #         "font-color", "Couleur", "Couleur du texte", Gimp.RGB, GObject.ParamFlags.READWRITE)
        # # )
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.int("justification-index", "Justification",
        # #                              "Justification du texte", GObject.ParamFlags.READWRITE)
        # # )
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.double("line-spacing", "Espacement lignes",
        # #                                 "Espacement entre les lignes", GObject.ParamFlags.READWRITE)
        # # )
        # # procedure.add_argument_from_property(
        # #     GObject.PropertySpec.double("letter-spacing", "Espacement lettres",
        # #                                 "Espacement entre les lettres", GObject.ParamFlags.READWRITE)
        # # )

        # procedure.add_menu_path("<Image>/DC-trad/")

        # return procedure

    # def run(self, procedure, run_mode, image, drawables, config, run_data):
    #     # source_path = args.index(0).get_string()
    #     # page_index = args.index(1).get_int32()
    #     # font = args.index(2).get_string()
    #     # fontunit_index = args.index(3).get_int32()
    #     # font_size = args.index(4).get_double()
    #     # antialias = args.index(5).get_boolean()
    #     # hintstyle_index = args.index(6).get_int32()
    #     # font_color = args.index(7).get_rgb()
    #     # justification_index = args.index(8).get_int32()
    #     # line_spacing = args.index(9).get_double()
    #     # letter_spacing = args.index(10).get_double()

    #     # active_layer = drawables[0] if n_drawables > 0 else None

    #     # plugin_import_text_layers_path_dctrad(
    #     #     image=image,
    #     #     active_layer=active_layer,
    #     #     source_path=source_path,
    #     #     page_index=page_index,
    #     #     font=font,
    #     #     fontunit_index=fontunit_index,
    #     #     font_size=font_size,
    #     #     antialias=antialias,
    #     #     hintstyle_index=hintstyle_index,
    #     #     font_color=font_color,
    #     #     justification_index=justification_index,
    #     #     line_spacing=line_spacing,
    #     #     letter_spacing=letter_spacing
    #     # )
    #     Gimp.message("coucou")

    #     return procedure.new_return_values(
    #         Gimp.PDBStatusType.SUCCESS, GLib.Error())

    # def run(self, procedure, run_mode, image, drawables, config, run_data):
    #     source_path = config.get_property("source_path")
    #     Gimp.message(f"Chemin reçu : {source_path}")
    #     return procedure.new_return_values(
    #         Gimp.PDBStatusType.SUCCESS, GLib.Error())

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        # Récupération du paramètre via config
        # source_path = config.get_property("source_path")
        Gimp.message("COUCOU")
        # Gimp.message(f"Chemin reçu : {source_path}")

        return procedure.new_return_values(
            Gimp.PDBStatusType.SUCCESS,
            GLib.Error()
        )


Gimp.main(ImportTextOnPathPlugin.__gtype__, sys.argv)
