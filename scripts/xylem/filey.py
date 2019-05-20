import os

from xylem.config import XylemConfig

def go_and_get_subfolders(folder):
  os.chdir(folder)
  return [f.path for f in os.scandir(folder) if f.is_dir() ]

def go_and_get_album_folders():
  return go_and_get_subfolders(XylemConfig.albums_folder)