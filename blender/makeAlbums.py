import bpy
import sys

scripts = 'C:\\Users\\Lucas\\Desktop\\xylem\\blender\\'
if (sys.path[0] != scripts):
    sys.path.insert(0, scripts)

from xylem.albumy import process_albums_folder, save_albums_project

albums_folder = 'C:\\Users\\Lucas\\Desktop\\xylem\\albums_wip'

process_albums_folder(albums_folder)
save_albums_project(albums_folder, 'albums_wip')

