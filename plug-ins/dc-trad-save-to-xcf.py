#!/usr/bin/env python

# Save to "XCF"
# Created by Sergeileduc
# ------------
#| Change Log |
# ------------
# Rel 1: Initial release.

from gimpfu import *
import os

def pythonSaveToXCF(image) :

	#Prep
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()

	#Code
	drawable = pdb.gimp_image_get_active_drawable(image)
	filename = pdb.gimp_image_get_filename(image)
	temp = filename.replace("_CLEAN", "")
	temp2 = temp.replace("_EDIT", "")
	filename = temp2.replace("_XCF", "")
	path=os.path.dirname(filename)
	path += "_XCF"
	name=os.path.basename(filename)
	out_xcf=os.path.join(path,name)
	out_xcf=os.path.splitext(out_xcf)[0]+'.xcf'

	if not os.path.exists(path):
		os.makedirs(path)

	pdb.gimp_file_save(image, drawable, out_xcf, out_xcf)
	pdb.gimp_image_clean_all(image)

	#finish
	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()

register(
"python-save-to-xcf",
"Sauvegarde vers le dossier XCF (en xcf)",
"Sauvegarde vers le dossier XCF (en xcf)",
"Sergeileduc",
"Sergeileduc",
"2018-08",
"6) Sauve vers le dossier \"-XCF\" (en xcf)",		#Menu path
"RGB*, GRAY*",
[
(PF_IMAGE, "image",       "Input image", None),
#(PF_DRAWABLE, "drawable", "Input drawable", None),
],
[],
pythonSaveToXCF,
menu="<Image>/DC-trad/Sauvegarder/"
)

main()
