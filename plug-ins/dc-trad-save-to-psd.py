#!/usr/bin/env python

# Save to "PSD"
# Created by Sergeileduc
# ------------
# | Change Log |
# ------------
# Rel 1: Initial release.

from gimpfu import pdb, register, main, PF_IMAGE
# from gimpfu import *
import os


def pythonSaveToPSD(image):

    # Prep
    pdb.gimp_image_undo_group_start(image)
    pdb.gimp_context_push()

    # Code
    drawable = pdb.gimp_image_get_active_drawable(image)
    filename = pdb.gimp_image_get_filename(image)
    temp = filename.replace("_CLEAN", "")
    temp2 = temp.replace("_EDIT", "")
    temp = temp2.replace("_XCF", "")
    filename = temp.replace("_PSD", "")
    path = os.path.dirname(filename)
    path += "_PSD"
    name = os.path.basename(filename)
    out_psd = os.path.join(path, name)
    out_psd = os.path.splitext(out_psd)[0]+'.psd'

    # Create folder
    if not os.path.exists(path):
        os.makedirs(path)

    pdb.gimp_file_save(image, drawable, out_psd, out_psd)
    pdb.gimp_image_clean_all(image)

    # Finish
    pdb.gimp_context_pop()
    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_displays_flush()


register(
    "python-save-to-psd",
    "Sauvegarde vers le dossier PSD (en .psd)",
    "Sauvegarde vers le dossier PSD (en .psd) (format PHOTOSHOP)",
    "Sergeileduc",
    "Sergeileduc",
    "2018-08",
    "9) [PHOTOSHOP] Sauve vers le dossier \"_PSD\" (en .psd)",  # Menu path
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image",       "Input image", None),
        # (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],
    [],
    pythonSaveToPSD,
    menu="<Image>/DC-trad/Sauvegarder/"
)

main()
