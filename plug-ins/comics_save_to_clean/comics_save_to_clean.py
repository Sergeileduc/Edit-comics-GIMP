#!/usr/bin/env python3

"""
Sauve le fichier en .jpg, dans un dossier cousin avec le suffixe _CLEAN

Exemple :
    .../Mon dossier/Mon image.jpg
    sera sauvé dans:
    .../Mon dossier_CLEAN/Mon image.jpg
"""

from pathlib import Path
import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import Gio
from gi.repository import GLib


import gettext
_ = gettext.gettext
def N_(message): return message


def clean_dirname(dirname):
    temp = dirname.replace("_CLEAN", "")
    temp2 = temp.replace("_EDIT", "")
    dirname = temp2.replace("_XCF", "")
    return dirname



def save_to_clean(procedure, run_mode, image, drawable, args, data):

    current_file = image.get_file()  # only if saved in xc, None if imported
    if not current_file:
        current_file = image.get_imported_file()  # if imported in jpeg, etc...
    
    # file_ = image.get_imported_file()
    #filename = file_.get_basename()
    path = Path(current_file.get_path()).resolve()
    print(path)

    filename = path.stem
    dirname = clean_dirname(path.parent.name)
    print(dirname)
    new_dirname = dirname + "_CLEAN"
    root = path.parents[1]
    new_dir = root / new_dirname
    print(new_dir)

    if not new_dir.exists():
        new_dir.mkdir()

    new_file = new_dir / (filename + ".jpg")
    
    # Merge visible layers in new image and export in CLEAN folder
    new_image = image.duplicate()
    layer = new_image.merge_visible_layers(Gimp.MergeType.CLIP_TO_IMAGE)
    
    # Save File
    Gimp.file_save(1,
                   new_image,
                   [layer],
                   Gio.file_new_for_path(str(new_file))
                   )

    # Clean
    image.clean_all()
    new_image.delete()

    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())



class SaveToClean(Gimp.PlugIn):
    ## Parameters ##

    ## GimpPlugIn virtual methods ##
    def do_query_procedures(self):
        self.set_translation_domain("gimp30-python",
                                    Gio.file_new_for_path(Gimp.locale_directory()))

        return [ 'python-fu-save-to-clean' ]  # Return procedure name, elsewhere this is "name"

    def do_create_procedure(self, name):
        procedure = None
        if name == 'python-fu-save-to-clean':
            procedure = Gimp.ImageProcedure.new(self, name,
                                                Gimp.PDBProcType.PLUGIN,
                                                save_to_clean, None)
            procedure.set_image_types("RGB*, GRAY*");
            procedure.set_documentation (N_("Sauvegarde vers le dossier clean (en jpeg)"),
                                        globals()["__doc__"],
                                        name)
            procedure.set_menu_label(N_("_5) Sauve vers le dossier \"-clean\" (en jpeg)"))
            procedure.set_attribution("Sergeileduc",
                                      "Sergeileduc",
                                      "2020")
            procedure.add_menu_path ("<Image>/DC-trad/Sauvegarder/")
        return procedure

Gimp.main(SaveToClean.__gtype__, sys.argv)
