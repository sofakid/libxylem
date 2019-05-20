import glob
import json
import os
import sys
import subprocess
import time
from collections import deque

from xylem.config import XylemConfig
from xylem.filey import go_and_get_album_folders
from xylem.stringy import mkv_suffix

def load_json():
  with open(XylemConfig.json_file, 'r') as fd:
    o = json.load(fd)
  return o

def make_images_cmd():
  scripts = sys.path[0]
  return [
    XylemConfig.blender, 
    '--background',
    '--factory-startup',
    '--python', os.path.join(scripts, 'xylem', 'blender', 'scripts', 'renderTrackImages.py'),
    '--', scripts
  ]

def make_albums_cmd():
  scripts = sys.path[0]
  return [
    XylemConfig.blender,
    '--background',
    '--factory-startup',
    '--python', os.path.join(scripts, 'xylem', 'blender', 'scripts', 'makeAlbums.py'),
    '--', scripts
  ]

def movie_cmd(movie):
  return [
    XylemConfig.blender, 
    '--background', 
    '--factory-startup',
    XylemConfig.blender_file,
    '-S', movie, # switch active scene
    '-a' # render animation
  ]

def concat_cmd(files_txt, out_file):
  return [
    XylemConfig.ffmpeg,
    '-nostdin', '-y',
    '-f', 'concat',
    '-safe', '0',
    '-i', files_txt,
    '-c', 'copy',
    out_file
  ]

def enqueue_movies(movies):
  q = deque()
  for movie in movies:
    cmd = movie_cmd(movie)
    q.append([movie, cmd])
  return q

def enqueue_albums(o):
  return enqueue_movies(o['albums'])

def enqueue_tracks(o):
  return enqueue_movies(o['tracks'])

def enqueue_all(o):
  return enqueue_movies(o['albums'] + o['tracks'])

def process_queue(q, blenders):
  start_time = time.time()
  procs = []
  def spawn(x):
    for i in range(x):
        if (len(q) == 0):
          break
        movie, cmd = q.popleft()
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
        procs.append([movie, proc])

  spawn(blenders)

  n = len(procs)
  while n > 0:
    n = len(procs)
    print('-------------------------------------')
    for mp in procs:
      movie, proc = mp
      ret = proc.poll()
      print(movie + ': ', end='')
      if (ret != None):
        n -= 1
        print('Complete.')

      else:
        print('Running...')
    
    if (n < blenders):
      available = blenders - n
      spawn(available)

    elapsed_time = time.time() - start_time
    s_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(s_time)

    time.sleep(60) 
  
  elapsed_time = time.time() - start_time
  s_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

  print('Done in %s.' % s_time)

def process_albums():
  o = load_json()
  q = enqueue_albums(o)
  process_queue(q, XylemConfig.blenders)

def process_tracks():
  o = load_json()
  q = enqueue_tracks(o)
  process_queue(q, XylemConfig.blenders)

def process_all():
  o = load_json()
  q = enqueue_all(o)
  process_queue(q, XylemConfig.blenders)

def make_track_images():
  cmd = make_images_cmd()
  print('Rendering track images...')
  subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  print('Done.')

def make_albums_project():
  cmd = make_albums_cmd()
  print('Making blender project for albums...')
  subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  print('Done.')

def make_albums_from_tracks():  
  subfolders = go_and_get_album_folders()

  for folder in subfolders:
    os.chdir(folder)
    suffix = mkv_suffix()
    tracks = glob.glob('trk_*' + suffix)
    tracks.sort()
    
    tracklist = 'tracklist.ffmpeg'

    with open(tracklist, 'w') as fd:
      for track in tracks:
        fd.write("file '" + track + "'\n")
        
    s = tracks[0][4:-(len(suffix) + 3)]
    outfile = 'album_' + s + suffix

    try:
      os.remove(outfile)
    except:
      pass

    print('Concatenating tracks to album :: ' + outfile, end='')
    cmd = concat_cmd(tracklist, outfile)
    subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(' :: done.')

    os.remove(os.path.join(folder, tracklist))