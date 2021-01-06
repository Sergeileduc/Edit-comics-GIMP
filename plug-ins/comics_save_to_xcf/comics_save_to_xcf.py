#!/usr/bin/env python3

"""
Sauve le fichier en .xcf, dans un dossier cousin avec le suffixe _XCF

Exemple :
    .../Mon dossier/Mon image.jpeg
    sera sauvé dans:
    .../Mon dossier_XCF/Mon image.xcf
"""
import gettext
from pathlib import Path
import sys

# import gi
# gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import Gio
from gi.repository import GLib

# _ = gettext.gettext
localdir = Path(__file__).resolve().parents[2] / 'locales'
gettext.install('comicssavexcf', localedir=localdir)
def N_(message): return message  # noqa: E704


def clean_dirname(dirname):
    temp = dirname.replace("_CLEAN", "")
    temp2 = temp.replace("_EDIT", "")
    dirname = temp2.replace("_XCF", "")
    return dirname


def save_to_xcf(procedure, run_mode, image, drawable, args, data):

    current_file = image.get_file()  # only if saved in xc, None if imported
    if not current_file:
        current_file = image.get_imported_file()  # if imported in jpeg, etc...

    # file_ = image.get_imported_file()
    # filename = file_.get_basename()
    path = Path(current_file.get_path()).resolve()
    filename = path.stem
    dirname = clean_dirname(path.parent.name)
    new_dirname = dirname + "_XCF"
    root = path.parents[1]
    new_dir = root / new_dirname

    if not new_dir.exists():
        new_dir.mkdir()

    new_file = new_dir / (filename + ".xcf")
    Gimp.file_save(0,
                   image,
                   image.get_layers(),
                   Gio.file_new_for_path(str(new_file))
                   )

    image.clean_all()

    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


class SaveToXCF(Gimp.PlugIn):
    # Parameters #

    # GimpPlugIn virtual methods #
    def do_query_procedures(self):
        self.set_translation_domain("gimp30-python",
                                    Gio.file_new_for_path(Gimp.locale_directory()))

        return ['python-fu-save-to-xcf']  # Return procedure name, elsewhere this is "name"

    def do_create_procedure(self, name):
        procedure = None
        if name == 'python-fu-save-to-xcf':
            procedure = Gimp.ImageProcedure.new(self, name,
                                                Gimp.PDBProcType.PLUGIN,
                                                save_to_xcf, None)
            procedure.set_image_types("RGB*, GRAY*")
            procedure.set_documentation(_("Save to _XCF folder (in .xcf)"),
                                        globals()["__doc__"],
                                        name)
            procedure.set_menu_label(_("6) Save to \"-XCF\" (in .xcf)"))
            procedure.set_attribution("Sergeileduc",
                                      "Sergeileduc",
                                      "2020")
            procedure.add_menu_path(_("<Image>/DC-trad/Save/"))
        return procedure


Gimp.main(SaveToXCF.__gtype__, sys.argv)
