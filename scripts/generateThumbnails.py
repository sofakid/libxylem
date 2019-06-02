import os
import subprocess

from xylem.filey import go_and_get_album_folders
from xylem.config import XylemConfig

magick = XylemConfig.magick
subfolders = go_and_get_album_folders()

for folder in subfolders:
  os.chdir(folder)

  cmd_s = 'convert -gravity center ' \
    + '( cover_bg.png -strip -resize 1280x1280^ -extent 1280x720 ) ' \
    + '( -background transparent cover_fg.png -strip -resize 720x720^ -extent 1280x720 ) ' \
    + '-layers flatten PNG24:thumbnail_yt.png'
  
  cmd = [magick] + cmd_s.split(' ')
  subprocess.call(cmd)

  #print('magick ' + cmd_s)