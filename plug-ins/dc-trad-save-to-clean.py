#!/usr/bin/env python

# Save to "Clean"
# Created by Sergeileduc
# ------------
#| Change Log |
# ------------
# Rel 1: Initial release.

from gimpfu import *
import os

def pythonSaveToClean(image) :

	#Prep
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()

	#Code
	filename_old = pdb.gimp_image_get_filename(image)
	filename = filename_old.replace("_CLEAN", "")
	drawable = pdb.gimp_image_get_active_drawable(image)
	path=os.path.dirname(filename)
	path += "_CLEAN"
	name=os.path.basename(filename)
	out_file=os.path.join(path,name)

	if not os.path.exists(path):
		os.makedirs(path)
	pdb.gimp_file_save(image, drawable, out_file, out_file)
	pdb.gimp_image_clean_all(image)

	#finish
	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()

register(
"python-save-to-clean",
"Sauvegarde vers le dossier clean (en jpeg)",
"Sauvegarde vers le dossier clean (en jpeg)",
"Sergeileduc",
"Sergeileduc",
"2018",
"5) Sauve vers le dossier \"-clean\" (en jpeg)",             #Menu path
"RGB*, GRAY*",
[
(PF_IMAGE, "image",       "Input image", None),
#(PF_DRAWABLE, "drawable", "Input drawable", None),
],
[],
pythonSaveToClean,
menu="<Image>/DC-trad/Sauvegarder/"
)

main()
