import os

from xylem.profiles import *

def getOptimalBlenders():
  cpus = os.cpu_count()
  if (cpus != None):
    if (cpus > 0):
      return int(cpus * 0.75)
  return 2
  
class XylemConfig:

  blender = r'C:\Program Files\Blender Foundation\Blender\blender.exe'
  magick = r'C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe'
  ffmpeg = r'C:\Program Files\ImageMagick-7.0.8-Q16\ffmpeg.exe'
  albums_folder = r'C:\Users\Lucas\Desktop\xylem\albums_wip'
  
  json_file = albums_folder + r'\albums_wip.json'
  blender_file = albums_folder + r'\albums_wip.blend'

  blenders = getOptimalBlenders()

  font = r'C:\Users\Lucas\Desktop\xylem\fonts\Futura Std Book.ttf'

  #profile = Profile_1280x720()
  profile = Profile_1920x854()
  #profile = Profile_1920x400()
  #profile = Profile_1280x1280()