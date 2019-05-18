import os
import glob
import subprocess

magick = r'C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe'
albums_folder = r'C:\Users\Lucas\Desktop\xylem\albums_todo'

os.chdir(albums_folder)

subfolders = [f.path for f in os.scandir(albums_folder) if f.is_dir() ]

for folder in subfolders:
  #print(folder)
  os.chdir(folder)

  cover = glob.glob('cover.*')[0]
  print(folder, end=' :: ')
  print(cover)
  subprocess.call([magick, 'convert', cover, '-blur', '0x10', '-brightness-contrast', '-30', 'cover_bg.png'])
  subprocess.call([magick, 'convert', cover, 'cover_fg.png'])
