#!/usr/bin/env python3

"""
Sauve le fichier en .psd, dans un dossier cousin avec le suffixe _PSD

Exemple :
    .../Mon dossier/Mon image.jpeg
    sera sauvé dans:
    .../Mon dossier_PSD/Mon image.psd
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
    temp = temp2.replace("_XCF", "")
    dirname = temp.replace("_PSD", "")
    return dirname


def save_to_psd(procedure, run_mode, image, drawable, args, data):

    current_file = image.get_file()  # only if saved in xc, None if imported
    if not current_file:
        current_file = image.get_imported_file()  # if imported in jpeg, etc...

    # file_ = image.get_imported_file()
    # filename = file_.get_basename()
    path = Path(current_file.get_path()).resolve()
    filename = path.stem
    dirname = clean_dirname(path.parent.name)
    new_dirname = f"{dirname}_PSD"
    root = path.parents[1]
    new_dir = root / new_dirname

    if not new_dir.exists():
        new_dir.mkdir()

    new_file = new_dir / f"{filename}.psd"
    Gimp.file_save(0,
                   image,
                   Gio.file_new_for_path(str(new_file))
                   )

    image.clean_all()

    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


class SaveToPSD(Gimp.PlugIn):
    # Parameters #

    # GimpPlugIn virtual methods #
    def do_query_procedures(self):
        return ['python-fu-save-to-psd']  # Return procedure name, elsewhere this is "name"

    def do_set_i18n(self, name):
        return False

    def do_create_procedure(self, name):
        procedure = None
        if name == 'python-fu-save-to-psd':
            procedure = Gimp.ImageProcedure.new(self, name,
                                                Gimp.PDBProcType.PLUGIN,
                                                save_to_psd, None)
            procedure.set_image_types("RGB*, GRAY*")
            procedure.set_documentation(N_("Sauvegarde vers le dossier PSD (en .psd)"),
                                        globals()["__doc__"],
                                        name)
            procedure.set_menu_label(N_("_9) [PHOTOSHOP] Sauve vers le dossier \"_PSD\" (en .psd)"))
            procedure.set_attribution("Sergeileduc",
                                      "Sergeileduc",
                                      "2025")
            procedure.add_menu_path("<Image>/DC-trad/Sauvegarder/")
        return procedure


Gimp.main(SaveToPSD.__gtype__, sys.argv)
