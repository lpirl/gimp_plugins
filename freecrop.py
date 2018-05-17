#!/usr/bin/env python
from gimpfu import *
from os.path import dirname, join, basename, splitext
from uuid import uuid4

def freecrop(img, _, grayscale=False, save=False, quit_gimp=False,
                    delete_other=False, grow_percent=0):

  # get selection bounding box
  bounds = pdb.gimp_selection_bounds(img)
  if not bounds[0]:
    return

  # calculate crop area:
  offx = bounds[1]
  offy = bounds[2]
  w = bounds[3] - bounds[1]
  h = bounds[4] - bounds[2]

  # grow crop area
  if grow_percent:
    growx = int(w / 100 * grow_percent)
    growy = int(h / 100 * grow_percent)
    offx = max(offx - growx, 0)
    offy = max(offy - growy, 0)
    w = min(w + 2 * growx, img.width)
    h = min(h + 2 * growy, img.height)

  pdb.gimp_image_crop(img,w,h,offx,offy)

  # delete other
  if delete_other:
    pdb.gimp_selection_invert(img)
    img.active_layer.add_alpha()
    if not pdb.gimp_selection_is_empty(img):
      pdb.gimp_edit_clear(pdb.gimp_image_get_active_drawable(img))

  # grayscale image
  if grayscale:
    img_is_gray = img.type == 1
    if not img_is_gray:
      pdb.gimp_image_convert_grayscale(img)

  # save
  if save:
    abspath = img.filename
    fname = uuid4().hex + ".png"
    dname = dirname(abspath)
    outabspath = join(dname, fname)

    pdb.file_png_save2(
        img,        # image
        pdb.gimp_image_get_active_drawable(img),
        outabspath,     # filename
        outabspath,     # raw file name
        0,          # interlacing
        9,          # compression
        0,          # save background
        0,          # save gamma
        0,          # save offset
        0,          # save size
        1,          # save creating time
        0,          # save comment
        0         # preserve color of transparent pixels
      )

  if quit_gimp:
    pdb.gimp_quit(1)

  return



def freecrop_transparency_save_quit(in_img, in_drawable):
  freecrop(in_img, in_drawable, quit_gimp=True, delete_other=True,
          save=True)

register(
  "freecrop_transparency_save_quit",
  "Crop to selection, make non-selection transparent, save under a random name, quit.",
  """The image will be cropped to the selection, non-selected pixels will
be made transparent,the image will be saved under a random name in the
same directory, and Gimp will close.""",
  "Lukas Pirl",
  "Lukas Pirl",
  "2018",
  "<Image>/File/non-rectangular crop, save (random name, same directory), quit",
  "*",
  [],
  [],
  freecrop_transparency_save_quit
)


GROW_PERCENT = 5
def freecrop_grayscale(in_img, in_drawable):
  freecrop(in_img, in_drawable, grayscale=True, grow_percent=GROW_PERCENT)

register(
  "freecrop_grayscale",
  "Crop to selection grown by %i %%, make grayscale." % GROW_PERCENT,
  """The selection will be grown by %i %%, the image will be cropped to
the selection and converted to grayscale.""" % GROW_PERCENT,
  "Lukas Pirl",
  "Lukas Pirl",
  "2018",
  "<Image>/Edit/rectangular crop (grown %i %%), grayscale" % GROW_PERCENT,
  "*",
  [],
  [],
  freecrop_grayscale
)



main()
