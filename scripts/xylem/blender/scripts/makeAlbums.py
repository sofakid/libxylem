import sys

scripts = sys.argv[-1]
if (sys.path[0] != scripts):
  sys.path.insert(0, scripts)

from xylem.blender.albumy import process_albums_folder, save_albums_project

process_albums_folder()
save_albums_project()
