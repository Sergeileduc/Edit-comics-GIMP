#!/usr/bin/env python3

"""
Sauve le fichier en .jpg, dans un dossier cousin avec le suffixe _EDIT

Exemple :
    .../Mon dossier/Mon image.jpg
    sera sauvé dans:
    .../Mon dossier_EDIT/Mon image.jpg
"""

import gettext
from gi.repository import GLib  # pylint: disable=no-name-in-module
from gi.repository import Gio  # pylint: disable=no-name-in-module
from gi.repository import Gimp  # pylint: disable=no-name-in-module
from pathlib import Path
import sys

import gi
gi.require_version('Gimp', '3.0')


_ = gettext.gettext
def N_(message): return message  # noqa: E704


def clean_dirname(dirname):
    temp = dirname.replace("_CLEAN", "")
    temp2 = temp.replace("_EDIT", "")
    dirname = temp2.replace("_XCF", "")
    return dirname


def save_to_edit_jpeg(image):

    current_file = image.get_file()  # only if saved in xc, None if imported
    if not current_file:
        current_file = image.get_imported_file()  # if imported in jpeg, etc...

    # file_ = image.get_imported_file()
    # filename = file_.get_basename()
    path = Path(current_file.get_path()).resolve()

    filename = path.stem
    dirname = clean_dirname(path.parent.name)
    new_dirname = f"{dirname}_EDIT"
    root = path.parents[1]
    new_dir = root / new_dirname

    if not new_dir.exists():
        new_dir.mkdir()

    new_file = new_dir / f"{filename}.jpg"

    # Save File
    Gimp.file_save(1,
                   image,
                   Gio.file_new_for_path(str(new_file))
                   )

    # Clean
    image.clean_all()


class SaveToEditJpeg(Gimp.PlugIn):

    def do_query_procedures(self):
        # Return procedure name, elsewhere this is "name"
        return ['python-fu-save-to-edit-jpeg']

    def do_set_i18n(self, name):
        return False

    def do_create_procedure(self, name):
        procedure = None
        if name == 'python-fu-save-to-edit-jpeg':
            procedure = Gimp.ImageProcedure.new(self, name,
                                                Gimp.PDBProcType.PLUGIN,
                                                self.run, None)
            procedure.set_image_types("RGB*, GRAY*")
            procedure.set_documentation(N_("Sauvegarde vers les dossiers Edit en jpeg uniquement"),
                                        globals()["__doc__"],
                                        name)
            procedure.set_menu_label(
                N_("_8) Sauve vers le dossier \"-Edit\" en jpeg uniquement"))
            procedure.set_attribution("Sergeileduc",
                                      "Sergeileduc",
                                      "2025")
            procedure.add_menu_path("<Image>/DC-trad/Sauvegarder/")
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        save_to_edit_jpeg(image)
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


Gimp.main(SaveToEditJpeg.__gtype__, sys.argv)
