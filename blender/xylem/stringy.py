import re

def truncate_start(s, maxlen):
  if (len(s) <= maxlen):
    return s
  return s[-maxlen:-1]

def truncate_end(s, maxlen):
  if (len(s) <= maxlen):
    return s
  return s[0:maxlen]  

def movie_label_fixed(prefix, artist, album, maxlen):
  s = simple_string(prefix)
  if len(s) > 0:
    s += '_'
  n = 2
  chunk_len = int(((maxlen - len(s))/n) - 1) 
  
  s += simple_string(truncate_end(artist, chunk_len))
  s += '_'
  s += simple_string(truncate_end(album, chunk_len))
  return s

def movie_label(artist, album):
  maxlabel = 60
  return movie_label_fixed('m', artist, album, maxlabel)

def simple_string(s):
  return re.sub(r'\W', '_', s)

def trackNumberize(number):
    return str(number) if (number > 9) else '0' + str(number)

def sceneNameForOverlayTrack(number, artist, album):
  maxlabel = 60
  s = 't_'
  n = 2
  chunk_len = int(((maxlabel - len(s) - 4)/n)) 
  
  s += simple_string(truncate_end(artist, chunk_len))
  s += '_'
  s += simple_string(truncate_end(album, chunk_len))
  s += '_'
  s += trackNumberize(number)
  return s

def zero_pad(x):
    y = int(x)
    z = '0' if y < 9 else ''
    return z + str(y)
     
def frames_to_time(frames):
    fps = 24
    seconds = int(frames / fps)
    minutes = int(seconds / 60)
    hours = int(minutes / 60)
    
    ss = seconds % 60
    mm = minutes % 60
    
    hh = '' if hours == 0 else (zero_pad(hours) + ";")
    return hh + zero_pad(mm) + ":" + zero_pad(ss)
