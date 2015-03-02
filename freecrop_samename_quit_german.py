#!/usr/bin/env python

"""
Same as freecroy.py but the resulting file name is the original plus a
(German) suffix.
Additionally, this plug-in is in German only.
"""

from gimpfu import *

def python_crop_to_png(in_img, in_drawable):
	img=in_img

	# crop
	bounds=pdb.gimp_selection_bounds(img)
	if not bounds[0]:
		return
	offx = bounds[1]
	offy = bounds[2]
	w = bounds[3]-offx
	h = bounds[4]-offy
	pdb.gimp_image_crop(img,w,h,offx,offy)

	# delete other
	pdb.gimp_selection_invert(img)
	img.active_layer.add_alpha()
	if not pdb.gimp_selection_is_empty(img):
		pdb.gimp_edit_clear(pdb.gimp_image_get_active_drawable(img))
	# save
	from os.path import dirname, join, basename, splitext
	abspath = img.filename
	fname, ext = splitext( basename(abspath) )
	fname = fname + "_ausgeschnitten.png"
	dname = dirname(abspath)
	outabspath = join(dname, fname)

	pdb.file_png_save2(
			img,				# image
			pdb.gimp_image_get_active_drawable(img),
			outabspath,			# filename
			outabspath,			# raw file name
			0,					# interlacing
			9,					# compression
			0,					# save background
			0,					# save gamma
			0,					# save offset
			0,					# save size
			1,					# save creating time
			0,					# save comment
			0					# preserve color of transparent pixels
		)
	pdb.gimp_quit(1)
	return

register(
	"python_crop_to_png",
	"Crops a Selection and saves it to an png.",
	"The image will be cropped to the selection, everything exept the selection will be cleared to transparent pixels, the image will be saved to a png postfixed with '_ausgeschnitten'.",
	"Lukas Pirl",
	"Lukas Pirl",
	"2012",
	"<Image>/File/Freigestellt speichern als PNG und beenden",
	"*",
	[],
	[],
	python_crop_to_png
)

main()
