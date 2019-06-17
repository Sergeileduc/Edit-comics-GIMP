#!/usr/bin/env python
# -*- coding: utf8 -*-
# -------------------------------------------------------------------------------------
#
# This file is a Python plug-in for GIMP which imports text from a file
# into layers, on a path.


# import sys
import re
import codecs
import io
from gimpfu import pdb, register, main
from gimpfu import PF_FILE, PF_SPINNER, PF_FONT, PF_BOOL, PF_OPTION, PF_COLOR
from gimpfu import TEXT_JUSTIFY_LEFT, TEXT_JUSTIFY_RIGHT
from gimpfu import TEXT_JUSTIFY_CENTER, TEXT_JUSTIFY_FILL
from gimpfu import TEXT_HINT_STYLE_NONE, TEXT_HINT_STYLE_SLIGHT
from gimpfu import TEXT_HINT_STYLE_MEDIUM, TEXT_HINT_STYLE_FULL
# Dequote next line to import all gimpfu
# from gimpfu import *


# def debugMessage(Message):
#    dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO,
#                               gtk.BUTTONS_OK, Message)
#    dialog.run()
#    dialog.hide()

justification_list = ["Aligné à gauche", "Aligné à droite",
                      "Centré", "Justifié"]
justification_values = [
                        TEXT_JUSTIFY_LEFT,
                        TEXT_JUSTIFY_RIGHT,
                        TEXT_JUSTIFY_CENTER,
                        TEXT_JUSTIFY_FILL]
alignment_list = ["top", "bottom", "middle"]
hintstyle_list = ["Aucun", "Léger", "Moyen", "Full/Justifié"]
hintstyle_values = [
                    TEXT_HINT_STYLE_NONE,
                    TEXT_HINT_STYLE_SLIGHT,
                    TEXT_HINT_STYLE_MEDIUM,
                    TEXT_HINT_STYLE_FULL]
boxmode_list = ["fixed", "dynamic"]
fontunit_list = ["pixels (px)", "pouces (in)",
                 "milimètres (mm)", "points (pt)"]


# Multiple replace function
def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)


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
                              hintstyle_values[hintstyle_index], font_color,
                              justification_values[justification_index],
                              indent, letter_spacing, line_spacing,
                              boxmode_list[box_mode_index], language,
                              use_markdown)


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
    # Regex used for split the page
    regex = r"^(?i)page [0-9]+.*(\r\n|\r|\n)"
    # special character for page jumps : u"\u2003"
    # special character for supspension marks : u"\u2026"
    # special character like WORD page jump, UTF-8 (...), etc... to be replaced
    substitutions = {u"\u2003": '', u"\u2026": '...', ' \n': '\n'}

    try:
        source_file = io.open(source_path, "rt", encoding="utf_8")
        raw_source = source_file.read()
        source_file.close()
    except UnicodeDecodeError:
        pdb.gimp_message("Le script n'a pas pu utiliser l'encodage de texte "
                         "UTF-8, et va utiliser un encodage par défaut.\n"
                         "En cas de problème, vous devriez envisager "
                         "d'enregistrer les fichiers textes avec l'encodage "
                         "UTF-8, à l'avenir")
        source_file = io.open(source_path, "rt")
        raw_source = source_file.read()
        source_file.close()
    if (raw_source):
        # BOM or NO-BOM UTF-8 files
        if raw_source.startswith(codecs.BOM_UTF8):
            # pdb.gimp_message("FICHIER AVEC BOM")
            source = raw_source.replace(codecs.BOM_UTF8, '', 1)
        else:
            source = raw_source
    else:
        pdb.gimp_message("failure: invalid source file(\""+source_path+"\")")
        return

    # Split pages
    pages_array = filter(lambda x: not re.match(r'^\s*$', x),
                         re.split(regex, source, flags=re.MULTILINE))
    # Clean working page
    page = replace(pages_array[int(page_index)-1], substitutions)
    # Split into lines
    text_lines = page.splitlines()

    pdb.gimp_image_undo_group_start(image)

    layer_position = 0
    flag = False
    if (active_layer):
        layer_height = pdb.gimp_image_height(image)
        layer_position = pdb.gimp_image_get_layer_position(image, active_layer)
        # tlayer_x = active_layer.offsets[0]
        # tlayer_y = active_layer.offsets[1]

        # Get active vector, path and points
        vectors = pdb.gimp_image_get_active_vectors(image)
        if vectors is None:
            pdb.gimp_message("Vous devriez tracer un chemin "
                             "avec l'outil chemin")
            n_points = 0
        else:
            nstrokes, strokes = pdb.gimp_vectors_get_strokes(vectors)
            stroke_type, n_points, cpoints, closed = \
                pdb.gimp_vectors_stroke_get_points(vectors, strokes[0])
    # indexes in cpoints array
    x_index = 0
    y_index = 1
    # (x,y) positions for text
    x_pos = 0.0
    y_pos = 0.0
    tlayer_width = 450
    tlayer_height = 150

    for rawtext in text_lines:
        if (source_escaped):
            text = rawtext.decode('unicode_escape')
        else:
            text = rawtext

        if (text != '//' and text != '' and text != '// '):
            if (len(text) < 20):
                tlayer_width = 150
                tlayer_height = 100
            else:
                tlayer_width = 450
                tlayer_height = 150

            if (x_index < n_points):
                # Text position from path
                x_pos = cpoints[x_index]
                y_pos = cpoints[y_index]
            else:
                if not flag:
                    pdb.gimp_message('Attention !!!\n'
                                     'Le nombre de points que vous avez '
                                     'selectionné ne correspond pas au nombre '
                                     'de lignes de texte du fichier.\n'
                                     'Le script va continuer en placant les '
                                     'lignes de texte restantes en bas '
                                     'de la page.\n'
                                     'Vous devriez vérifier vos bulles, ou '
                                     'annuler pour recommencer, en pointant '
                                     'toutes les bulles et encarts de texte.')
                    flag = True
                x_pos = 500
                y_pos = layer_height - 200

            x_index += 6
            y_index += 6

            tlayer = pdb.gimp_text_layer_new(image, text, font, font_size,
                                             fontunit_index)
            pdb.gimp_image_add_layer(image, tlayer, layer_position)

            pdb.gimp_text_layer_set_antialias(tlayer, antialias)
            pdb.gimp_text_layer_set_color(tlayer, font_color)
            pdb.gimp_text_layer_set_indent(tlayer, indent)
            pdb.gimp_text_layer_set_justification(tlayer, justification)
            pdb.gimp_text_layer_set_hint_style(tlayer, hintstyle)
            pdb.gimp_text_layer_set_language(tlayer, language)
            pdb.gimp_text_layer_set_letter_spacing(tlayer, letter_spacing)
            pdb.gimp_text_layer_set_line_spacing(tlayer, line_spacing)

            pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
            pdb.gimp_layer_set_offsets(tlayer, x_pos, y_pos)
            pdb.gimp_item_set_visible(tlayer, True)

    pdb.gimp_image_undo_group_end(image)
    return  # end of function


# Register in Gimp
register(
    "plugin_import_text_layers_path_dctrad",
    "Importer le texte le long du chemin trace",
    "Import text from file to layers on path",
    "Sergeileduc",
    "",
    "2018-08",
    "<Image>/DC-trad/Importer un texte sur un chemin",
    "*",
    # (type, name, description, default [, extra])
    [
        (PF_FILE, "source_path", "Fichier texte", ''),
        (PF_SPINNER, "page_index",
         "Numero de page (la première page est tout le temps 1)",
         1, (1, 50, 1)),
        # (PF_BOOL,     "source_escaped",   "text is escaped",  False),
        (PF_FONT, "font", "Police", 'Sans'),
        (PF_OPTION, "fontunit_index",
         "Unité pour taille de police", 0, fontunit_list),
        (PF_SPINNER, "font_size", "Taille de police", 27, (1, 200, 1)),
        (PF_BOOL, "antialias", "Lissage (antialiasing)", True),
        (PF_OPTION, "hintstyle_index",
         "Ajustement", 0, hintstyle_list),
        (PF_COLOR, "font_color", "Couleur texte", '#000000'),
        (PF_OPTION, "justification_index",
         "Justification", 2, justification_list),
        (PF_SPINNER, "line_spacing",
         "Espacement de ligne", 0.0, (-200.0, 200.0, 0.1)),
        (PF_SPINNER, "letter_spacing",
         "Espacement de lettre", 0.0, (0.0, 200.0, 0.1))
    ],
    # (PF_OPTION, "box_mode_index", "Boite", 0, boxmode_list),
    [],
    plugin_import_text_layers_path_dctrad)

main()
