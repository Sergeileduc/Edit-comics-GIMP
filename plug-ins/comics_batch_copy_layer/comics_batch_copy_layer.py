#!/usr/bin/env python3

"""
Dupplique le calque image de toutes les images ouvertes.
"""

# from pathlib import Path
import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp  # pylint: disable=no-name-in-module
from gi.repository import Gio  # pylint: disable=no-name-in-module
from gi.repository import GLib  # pylint: disable=no-name-in-module


import gettext
_ = gettext.gettext
def N_(message): return message  # noqa: E704


def batch_copy_layer(procedure, run_mode, image, drawable, args, data):

    images = Gimp.get_images()

    for image in images:
        Gimp.get_pdb().run_procedure('script-fu-copy-layer',
                                     [Gimp.RunMode.INTERACTIVE, image])

    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


class BatchCopyLayer(Gimp.PlugIn):
    # Parameters #

    # GimpPlugIn virtual methods #
    def do_query_procedures(self):
        self.set_translation_domain("gimp30-python",
                                    Gio.file_new_for_path(Gimp.locale_directory()))

        return ['python-fu-copy-layer-all']  # Return procedure name, elsewhere this is "name"

    def do_create_procedure(self, name):
        procedure = None
        if name == 'python-fu-copy-layer-all':
            procedure = Gimp.ImageProcedure.new(self, name,
                                                Gimp.PDBProcType.PLUGIN,
                                                batch_copy_layer, None)
            procedure.set_image_types("RGB*, GRAY*")
            procedure.set_documentation(N_("Duplique le calque de TOUTES les images ouvertes, pour avoir un calque de travail \"Edit\" et une calque de reference \"Original\""
                                           "Le script verouille les calques en deplacement, et verouille le calque original pour le rendre non modifiable"),
                                        globals()["__doc__"],
                                        name)
            procedure.set_menu_label(N_("_1) Dupliquer toutes les images ouvertes garder l'original..."))
            procedure.set_attribution("Sergeileduc",
                                      "Sergeileduc",
                                      "2020")
            procedure.add_menu_path("<Image>/DC-trad Traitement par lot/")
        return procedure


Gimp.main(BatchCopyLayer.__gtype__, sys.argv)
