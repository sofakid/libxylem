import bpy
import math
import os
import glob
import json

from xylem.blender.sceney import *
from xylem.blender.imagey import *
from xylem.blender.texty import *
from xylem.blender.sequencey import *
from xylem.customy import *
from xylem.stringy import *
from xylem.filey import *
from xylem.config import *
    
def makeTrackScene(number, title, folder, artist, album):
  custom = XylemCustomize(number, title, artist, album)
  folder = folder + "\\"
  scene_name = track_image_label(number, artist, album)
  new_scene(scene_name, folder)
  set_camera()
  coverImage(custom, folder)
  putFullText(custom, number, title, artist, album)
  bpy.ops.render.render(write_still=True)

def getFolderData(folder):
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
  
  return folder_out


def getData(albums_folder):

  data_out = []

  subfolders = go_and_get_subfolders(albums_folder)

  for folder in subfolders:
    folder_out = getFolderData(folder)
    data_out.append([folder, folder_out])
  return data_out


def make_album_graphics(folder):
  albumData = getFolderData(folder)
  for song in albumData:
    artist, album, track, track_title, soundfile = song
    # number, title, folder, artist, album):
    makeTrackScene(track, track_title, folder, artist, album)

def make_album_track_movies(folder):
  albumData = getFolderData(folder)
  
  start = 0
  for song in albumData:
    artist, album, track, track_title, soundfile = song
  
    s_track = track_numberize(track)
    movie = movie_track_label(artist, album, s_track)
    new_movie_scene(movie, folder + "\\")
    
    dur = sequence_add_sound_and_image(
          folder, soundfile, artist, album, track, start)
    
    render_movie(False, dur)

def make_album_movie(folder):
  albumData = getFolderData(folder)

  for song in albumData:
    artist, album, track, track_title, soundfile = song
    break

  s_header = ''
  s_txt = ''

  movie = movie_label(artist, album)
  new_movie_scene(movie, folder + "\\")
  
  start = 0

  for song in albumData:
    artist, album, track, track_title, soundfile = song
    
    if (s_header == ''):
      s_header = artist + ' - ' + album + '\n' + 'Xylem Records' + '\n\n'
    s_txt += frames_to_time(start) + ' - ' + track_title + '\n'
    
    dur = sequence_add_sound_and_image(
      folder, soundfile, artist, album, track, start)
    
    start += dur

  print(s_header + s_txt)
  with open(folder + '\\' + 'nfo.txt', 'w', encoding='utf-8') as fd:
    s_out = s_header + s_txt
    fd.write(s_out)
  
  render_movie(False, start)

def process_albums_folder():
  subfolders = go_and_get_album_folders()

  # do all the graphics scenes first
  #for folder in subfolders:
  #    make_album_graphics(folder) 

  # now make the movie scenes
  for folder in subfolders:
    make_album_movie(folder)
    make_album_track_movies(folder)

def save_albums_project():

  scenes = bpy.data.scenes.keys()
  albums = list(filter(lambda x: x.startswith('alb_'), scenes))
  tracks = list(filter(lambda x: x.startswith('trk_'), scenes))

  try:
    os.remove(XylemConfig.blender_file)
    os.remove(XylemConfig.json_file)
  except:
    pass

  # save the blender file
  bpy.ops.wm.save_as_mainfile(filepath=XylemConfig.blender_file)
  
  # save the list of movies to render
  with open(XylemConfig.json_file, "w") as fd:
    j = { 
      'albums': albums,
      'tracks': tracks
    }
    json.dump(j, fd)
