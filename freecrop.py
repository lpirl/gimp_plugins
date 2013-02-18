#!/usr/bin/env python
from gimpfu import *
from uuid import uuid4

def python_freecrop_uuid(in_img, in_drawable):
	img=pdb.gimp_image_duplicate(in_img)

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
	pdb.gimp_edit_clear( pdb.gimp_image_get_active_drawable(img) )

	# save
	from os.path import dirname, join, basename, splitext
	abspath = in_img.filename
	fname = uuid4().hex + ".png"
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
	return

register(
	"python_freecrop_uuid",
	"Crops a selection and saves it to a png.",
	"The image will be cropped to the selection, everything except the selection will be cleared to transparent pixels, the image will be saved to a png renamed to some UUID.",
	"Lukas Pirl",
	"Lukas Pirl",
	"2012",
	"<Image>/File/non-rectangular crop to PNG with random name",
	"*",
	[],
	[],
	python_freecrop_uuid
)

main()
