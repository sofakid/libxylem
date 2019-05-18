import bpy
import math
import os
import glob
import json

from xylem.stringy import *
from xylem.sceney import *
from xylem.imagey import *
from xylem.texty import *
from xylem.configgy import *

def go_and_get_subfolders(folder):
  os.chdir(folder)
  return [f.path for f in os.scandir(folder) if f.is_dir() ]

def makeTrackScene(number, title, folder, artist, album):
    cfg = xylemConfigure(number, title, artist, album)
    folder = folder + "\\"
    scene_name = sceneNameForOverlayTrack(number, artist, album)
    newScene(scene_name, folder)
    setCamera()
    coverImage(cfg, folder)
    putFullText(cfg, number, title, artist, album)
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
      artist, album, track, trackTitle, filename = song
      # number, title, folder, artist, album):
      makeTrackScene(track, trackTitle, folder, artist, album)

def make_album_movie(folder):
    albumData = getFolderData(folder)

    for song in albumData:
      artist, album, track, trackTitle, filename = song
      break

    s_header = ''
    s_txt = ''

    movie = movie_label(artist, album)
    newMovieScene(movie, folder + "\\")
    scene = bpy.data.scenes.get(movie)
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    
    bpy.context.area.type = 'SEQUENCE_EDITOR'

    start = 0

    for song in albumData:
        artist, album, track, trackTitle, filename = song
        
        if (s_header == ''):
            s_header = artist + ' - ' + album + '\n' + 'Xylem Records' + '\n\n'
        s_txt += frames_to_time(start) + ' - ' + trackTitle + '\n'
        
        fullPath = folder + "\\" + album
        
        print(fullPath)
        
        bpy.ops.sequencer.sound_strip_add(
            filepath=fullPath, 
            files=[{"name":filename, "name":filename}],
            relative_path=True, frame_start=1, channel=1)
        
        sound_strip = bpy.context.scene.sequence_editor.active_strip
        
        dur = sound_strip.frame_duration
        sound_strip.frame_start = start
        
        overlay_png = sceneNameForOverlayTrack(track, artist, album) + ".png"
        doCoverImage(folder, overlay_png, start, start + dur)
        
        #bpy.ops.sequencer.scene_strip_add(scene=overlay_scene)
        #overlay_strip = bpy.context.scene.sequence_editor.active_strip
        #overlay_strip.frame_final_duration = dur
        #overlay_strip.frame_start = start
        
        start += dur

    print(s_header + s_txt)
    with open(folder + '\\' + 'nfo.txt', 'w', encoding='utf-8') as fd:
        s_out = s_header + s_txt
        fd.write(s_out)
    
    render_movie(False, start)

def process_albums_folder(albums_folder):
    subfolders = go_and_get_subfolders(albums_folder)

    # do all the graphics scenes first
    for folder in subfolders:
        make_album_graphics(folder) 
  
    # now make the movie scenes
    for folder in subfolders:
        make_album_movie(folder) 

def save_albums_project(albums_folder, project_name):

    movies = list(filter(lambda x: x.startswith('m_'), bpy.data.scenes.keys()))

    project_name = '\\' + project_name
    
    # these two files are used by renderAlbums.py
    blender_file = albums_folder + project_name + '.blend'
    json_file = albums_folder + project_name + '.json'

    try:
      os.remove(blender_file)
      os.remove(json_file)
    except:
      pass
      
    # save the blender file
    bpy.ops.wm.save_as_mainfile(filepath=blender_file)
    
    # save the list of movies to render
    with open(json_file, "w") as fd:
      j = { 'movies': movies }
      json.dump(j, fd)
