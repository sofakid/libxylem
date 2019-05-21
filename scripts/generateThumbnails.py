import os
import subprocess

from xylem.filey import go_and_get_album_folders
from xylem.config import XylemConfig

magick = XylemConfig.magick
subfolders = go_and_get_album_folders()

for folder in subfolders:
  os.chdir(folder)

  cmd_bg = [magick, 'convert', 
    'cover_bg.png', '-gravity', 'center', 
    '-resize', '1280x1280^',
    '-extent', '1280x720',
    'ytt_bg.png']

  cmd_fg = [magick, 'convert',
    '-background', 'transparent', 
    'cover_fg.png', '-gravity', 'center', 
    '-resize', '720x720^',
    '-extent', '1280x720',
    'ytt_fg.png']

  cmd_combine = [magick, 'convert', '-gravity', 'center', 
    'ytt_bg.png', 'ytt_fg.png',
    '-layers', 'flatten',
    'thumbnail_yt.png']

  for cmd in [cmd_bg, cmd_fg, cmd_combine]:
    subprocess.call(cmd)

  os.remove('ytt_bg.png')
  os.remove('ytt_fg.png')