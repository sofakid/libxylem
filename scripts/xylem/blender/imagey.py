import bpy
import struct
import imghdr

from xylem.config import XylemConfig

# ===================================================================
# get_image_size: thanks stack overflow
def get_image_size(fname):
  '''Determine the image type of fhandle and return its size.
  from draco'''
  with open(fname, 'rb') as fhandle:
    head = fhandle.read(24)
    if len(head) != 24:
      return
    if imghdr.what(fname) == 'png':
      check = struct.unpack('>i', head[4:8])[0]
      if check != 0x0d0a1a0a:
        return
      width, height = struct.unpack('>ii', head[16:24])
    elif imghdr.what(fname) == 'gif':
      width, height = struct.unpack('<HH', head[6:10])
    elif imghdr.what(fname) == 'jpeg':
      try:
        fhandle.seek(0) # Read 0xff next
        size = 2
        ftype = 0
        while not 0xc0 <= ftype <= 0xcf:
          fhandle.seek(size, 1)
          byte = fhandle.read(1)
          while ord(byte) == 0xff:
            byte = fhandle.read(1)
          ftype = ord(byte)
          size = struct.unpack('>H', fhandle.read(2))[0] - 2
        # We are at a SOFn block
        fhandle.seek(1, 1)  # Skip `precision' byte.
        height, width = struct.unpack('>HH', fhandle.read(4))
      except Exception: #IGNORE:W0703
        return
    else:
      return
    return width, height

# put the images in the scene
def coverImage(custom, folder):
  coverFgFilename = 'cover_fg.png'
  coverBgFilename = 'cover_bg.png'
  
  #print(folder + ' :: ' + coverFgFilename)
  imgX, imgY = get_image_size(folder + coverFgFilename)
  
  theta = imgY / imgX
  
  bgX = XylemConfig.profile.bg_w
  bgY = bgX * theta
  
  bpy.ops.import_image.to_plane(
    files=[{"name":coverBgFilename, "name":coverBgFilename}],
    directory=folder,
    relative=False)
  bpy.context.object.active_material.use_shadeless = True

  bgImage = bpy.context.object  
  bgImage.dimensions = bgX, bgY, 0
  bgImage.location = 0, 0, -2
  
  nice = 6.8
  nice_shift = 4
  
  fgX = nice
  fgY = fgX * theta
  x_shift = 0
  
  if (fgY != fgX):
    fgY = nice
    fgX = fgY / theta
    x_shift = (fgX - nice) / 2
  
  bpy.ops.import_image.to_plane(
    files=[{"name":coverFgFilename, "name":coverFgFilename}],
    directory=folder, 
    relative=False)
  
  bpy.context.object.active_material.use_shadeless = True
  
  fgImage = bpy.context.object
  fgImage.dimensions = fgX, fgY, 0
  fgImage.location = XylemConfig.profile.origin_x, XylemConfig.profile.origin_y, 0
  
  bpy.ops.transform.translate(value=(-nice_shift + x_shift, XylemConfig.profile.fg_raise, 0))

  return 2 * x_shift