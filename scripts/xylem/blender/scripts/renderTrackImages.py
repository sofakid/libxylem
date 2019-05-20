import sys

scripts = sys.argv[-1]
if (sys.path[0] != scripts):
  sys.path.insert(0, scripts)

from xylem.filey import go_and_get_album_folders
from xylem.blender.albumy import make_album_graphics

import addon_utils
addon_utils.enable('io_import_images_as_planes')

subfolders = go_and_get_album_folders()

# do all the graphics scenes first
for folder in subfolders:
    make_album_graphics(folder)
