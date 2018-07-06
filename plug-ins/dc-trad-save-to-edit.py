#!/usr/bin/env python

# Save to "Edit"
# Created by Sergeileduc
# ------------
#| Change Log |
# ------------
# Rel 1: Initial release.

from gimpfu import *
import os

def pythonSaveToEdit(image,drawable) :

	#Prep
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()

	#Code
	filename = pdb.gimp_image_get_filename(image)
	filename2 = filename.replace("_CLEAN", "")
	drawable = pdb.gimp_image_get_active_drawable(image)
	path=os.path.dirname(filename2)
	path2=os.path.dirname(filename2)
	path += "_EDIT"
	path2 += "_XCF"
	name=os.path.basename(filename2)
	out_file=os.path.join(path,name)
	out_xcf=os.path.join(path2,name)
	out_xcf=os.path.splitext(out_xcf)[0]+'.xcf'
	
	if not os.path.exists(path):
		os.makedirs(path)
	if not os.path.exists(path2):
		os.makedirs(path2)
	pdb.gimp_file_save(image, drawable, out_file, out_file)
	pdb.gimp_file_save(image, drawable, out_xcf, out_xcf)
	pdb.gimp_image_clean_all(image)
	
	#finish
	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()

register(
	"python-save-to-edit",                           
	"Sauvegarde vers les dossiers Edit et XCF",
	"Sauvegarde vers les dossiers Edit et XCF",
	"Sergeileduc",
	"Sergeileduc",
	"2018",
	"6) Sauve vers les dossiers \"-Edit\" et \"-XCF\"",             #Menu path
	"RGB*, GRAY*", 
	[
	(PF_IMAGE, "image",       "Input image", None),
    (PF_DRAWABLE, "drawable", "Input drawable", None),
	],
	[],
	pythonSaveToEdit,
	menu="<Image>/DC-trad/"
	)

main()
