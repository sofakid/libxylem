import os
from xylem.config import XylemConfig

def error_msg(msg):
  print('libxylem not configured correctly!')
  print(' -- ' + msg)
  print('\nEnsure xylem/config.py is done right')
  exit()

def is_exe(fpath):
  return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def test_exe(exe, name):
  if (not is_exe(exe)):
    error_msg(name + ' path not correct.')

def test_folder(folder, name):
  if (not os.path.isdir(folder)):
    error_msg(name + ' folder not right.')

def test_file(file, name):
  if (not os.path.isfile(file)):
    error_msg(name + ' not right.')


test_exe(XylemConfig.blender, 'Blender')
test_exe(XylemConfig.magick, 'ImageMagick')
test_exe(XylemConfig.ffmpeg, 'FFmpeg')

test_folder(XylemConfig.albums_folder, 'albums_folder')

test_file(XylemConfig.font, 'font')

