import os
import glob
import subprocess

from xylem.filey import go_and_get_album_folders
from xylem.config import XylemConfig

magick = XylemConfig.magick
subfolders = go_and_get_album_folders()

for folder in subfolders:
  #print(folder)
  os.chdir(folder)

  cover = glob.glob('cover.*')[0]
  print(folder + ' :: ' + cover)
  subprocess.call([magick, 'convert', cover, '-blur', '0x20', '-brightness-contrast', '-30', 'cover_bg.png'])
  subprocess.call([magick, 'convert', cover, 'cover_fg.png'])
