#!/usr/bin/env python3

"""
Sauve le fichier en .xcf, dans un dossier cousin avec le suffixe _XCF
Et en .jpeg, dans le dossier cousin avec le suffixe _EDIT

Exemple :
    .../Mon dossier/Mon image.jpeg
    sera sauvé dans:
    .../Mon dossier_XCF/Mon image.xcf
    .../Mon dossier_EDIT/Mon image.jpg
"""

from pathlib import Path
import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp  # pylint: disable=no-name-in-module
from gi.repository import Gio  # pylint: disable=no-name-in-module
from gi.repository import GLib  # pylint: disable=no-name-in-module


import gettext
_ = gettext.gettext
def N_(message): return message  # noqa: E704


def clean_dirname(dirname):
    temp = dirname.replace("_CLEAN", "")
    temp2 = temp.replace("_EDIT", "")
    dirname = temp2.replace("_XCF", "")
    return dirname


def save_to_edit(procedure, run_mode, image, drawable, args, data):

    current_file = image.get_file()  # only if saved in xc, None if imported
    if not current_file:
        current_file = image.get_imported_file()  # if imported in jpeg, etc...

    # file_ = image.get_imported_file()
    # filename = file_.get_basename()
    path = Path(current_file.get_path()).resolve()
    filename = path.stem
    dirname = clean_dirname(path.parent.name)
    xcf_dirname = dirname + "_XCF"
    edit_dirname = dirname + "_EDIT"
    root = path.parents[1]
    xcf_dir = root / xcf_dirname
    edit_dir = root / edit_dirname

    if not xcf_dir.exists():
        xcf_dir.mkdir()
    if not edit_dir.exists():
        edit_dir.mkdir()

    # Save xcf in XCF
    xcf_file = xcf_dir / (filename + ".xcf")
    Gimp.file_save(0,
                   image,
                   image.get_layers(),
                   Gio.file_new_for_path(str(xcf_file))
                   )

    # Save jpeg in EDIT
    new_image = image.duplicate()
    layer = new_image.merge_visible_layers(Gimp.MergeType.CLIP_TO_IMAGE)
    edit_file = edit_dir / (filename + ".jpg")
    Gimp.file_save(1,
                   new_image,
                   [layer],
                   Gio.file_new_for_path(str(edit_file))
                   )
    new_image.delete()

    # Clean
    image.clean_all()

    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


class SaveToEdit(Gimp.PlugIn):
    # Parameters #

    # GimpPlugIn virtual methods #
    def do_query_procedures(self):
        self.set_translation_domain("gimp30-python",
                                    Gio.file_new_for_path(Gimp.locale_directory()))

        return ['python-fu-save-to-edit']  # Return procedure name, elsewhere this is "name"

    def do_create_procedure(self, name):
        procedure = None
        if name == 'python-fu-save-to-edit':
            procedure = Gimp.ImageProcedure.new(self, name,
                                                Gimp.PDBProcType.PLUGIN,
                                                save_to_edit, None)
            procedure.set_image_types("RGB*, GRAY*")
            procedure.set_documentation(N_("Sauvegarde vers les dossiers Edit et XCF"),
                                        globals()["__doc__"],
                                        name)
            procedure.set_menu_label(N_("_7) Sauve vers les dossiers \"-Edit\" et \"-XCF\""))
            procedure.set_attribution("Sergeileduc",
                                      "Sergeileduc",
                                      "2020")
            procedure.add_menu_path("<Image>/DC-trad/Sauvegarder/")
        return procedure


Gimp.main(SaveToEdit.__gtype__, sys.argv)
