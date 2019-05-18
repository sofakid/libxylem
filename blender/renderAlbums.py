import os
import sys
import glob
import subprocess
import json
import time

from collections import deque

blender = r'C:\Program Files\Blender Foundation\Blender\blender.exe'
albums_folder = r'C:\Users\Lucas\Desktop\xylem\albums_wip'
json_file = albums_folder + r'\albums_wip.json'
blender_file = albums_folder + r'\albums_wip.blend'

threads = 3

start_time = time.time()

os.chdir(albums_folder)

with open(json_file, 'r') as fd:
  o = json.load(fd)

print(str(o))

q = deque()

for movie in o['movies']:

  cmd = [
    blender, 
    '--background', 
    '--factory-startup',
    blender_file,
    '-S', movie, # switch active scene
    '-a' # render animation
  ]

  #proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
  q.append([movie, cmd])


  #proc = subprocess.call(argv) #, stdout=subprocess.DEVNULL)

procs = []
running = 0
def spawn(x):
  for i in range(x):
      if (len(q) == 0):
        break
      movie, cmd = q.popleft()
      proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
      procs.append([movie, proc])

spawn(threads)

n = len(procs)
while n > 0:
  n = len(procs)
  print('-------------------------------------')
  for mp in procs:
    movie, proc = mp
    ret = proc.poll()
    print('Rendering ' + movie + ': ', end='')
    if (ret != None):
      n -= 1
      print('Complete.')

    else:
      print('Running...')
  
  if (n < threads):
    available = threads - n
    spawn(available)

  elapsed_time = time.time() - start_time
  s_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
  print(s_time)

  time.sleep(30) 
#'''
elapsed_time = time.time() - start_time
s_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

print('Done in %s.' % s_time)