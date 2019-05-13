import os
import glob
import subprocess

this_folder = r'C:\Users\Lucas\Desktop\xylem\albums_todo'

def getData(albums_folder):

  data_out = []

  os.chdir(albums_folder)

  subfolders = [f.path for f in os.scandir(albums_folder) if f.is_dir() ]

  for folder in subfolders:
    #print(folder)
    os.chdir(folder)

    folderbase = os.path.basename(folder)
    [ folder_artist, folder_album ] = folderbase.split(" - ")
    x = len(folderbase)

    files = glob.glob('*.mp3')
    #print(folder, end=' :: ')
    #print(files)

    folder_out = []
    for filename in files:
      base, ext = os.path.splitext(filename)

      fartist = len(folder_artist)
      falbum = len(folder_album)

      artist = base[0:fartist]
      base = base[fartist+3:]
      
      album = base[0:falbum]
      base = base[falbum+3:]

      sTrack = base[0:2]
      base = base[3:] # strip track number
      track = int(sTrack)

      folder_out.append([artist, album, track, base, filename])
      print(artist + " :: " + album + " :: " + str(track) + " :: " + base)
    
    data_out.append([folder, folder_out])
  return data_out

data = getData(this_folder)

print(str(data))