#!/usr/bin/env python

# Save to "Edit"
# Created by Sergeileduc
# ------------
# | Change Log |
# ------------
# Rel 1: Initial release.

from gimpfu import pdb, register, main, PF_IMAGE, CLIP_TO_IMAGE
# from gimpfu import *
import os


def pythonSaveToEdit(image):

    # Prep
    pdb.gimp_image_undo_group_start(image)
    pdb.gimp_context_push()

    # Code
    drawable = pdb.gimp_image_get_active_drawable(image)
    filename = pdb.gimp_image_get_filename(image)
    temp = filename.replace("_CLEAN", "")
    temp2 = temp.replace("_EDIT", "")
    filename = temp2.replace("_XCF", "")
    path = os.path.dirname(filename)
    path2 = os.path.dirname(filename)
    path += "_EDIT"
    path2 += "_XCF"
    name = os.path.basename(filename)
    out_file = os.path.join(path, name)
    out_xcf = os.path.join(path2, name)
    out_file = os.path.splitext(out_file)[0]+'.jpg'
    out_xcf = os.path.splitext(out_xcf)[0]+'.xcf'

    # Create folders
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path2):
        os.makedirs(path2)

    # pdb.gimp_file_save(image, drawable, out_file, out_file)
    new_image = pdb.gimp_image_duplicate(image)
    layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
    pdb.gimp_file_save(new_image, layer, out_file, out_file)
    pdb.gimp_image_delete(new_image)
    pdb.gimp_file_save(image, drawable, out_xcf, out_xcf)
    pdb.gimp_image_clean_all(image)

    # Finish
    pdb.gimp_context_pop()
    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_displays_flush()


register(
    "python-save-to-edit",
    "Sauvegarde vers les dossiers Edit et XCF",
    "Sauvegarde vers les dossiers Edit et XCF",
    "Sergeileduc",
    "Sergeileduc",
    "2018-08",
    "7) Sauve vers les dossiers \"-Edit\" et \"-XCF\"",  # Menu path
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image", "Input image", None),
        # (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],
    [],
    pythonSaveToEdit,
    menu="<Image>/DC-trad/Sauvegarder/"
)

main()
