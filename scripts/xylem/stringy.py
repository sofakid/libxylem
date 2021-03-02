import re
from xylem.config import XylemConfig

maxlabel = 60

def truncate_start(s, maxlen):
  if (len(s) <= maxlen):
    return s
  return s[-maxlen:-1]

def truncate_end(s, maxlen):
  if (len(s) <= maxlen):
    return s
  return s[0:maxlen]  

def movie_label_fixed(prefix, artist, album, suffix, maxlen):
  s = simple_string(prefix)
  sx = suffix if len(suffix) == 0 else '_' + suffix
  if len(s) > 0:
    s += '_'
  n = 2
  chunk_len = int(((maxlen - len(s) - len(sx) - 1)/n)) 
  
  s += simple_string(truncate_end(artist, chunk_len))
  s += '_'
  s += simple_string(truncate_end(album, chunk_len))
  s += simple_string(sx)
  return s

def movie_label(artist, album):
  return movie_label_fixed('alb', artist, album, '', maxlabel)

def movie_track_label(artist, album, sTrackNumber):
  return movie_label_fixed('trk', simple_string(artist), simple_string(album), sTrackNumber, maxlabel)

def simple_string(s):
  return re.sub(r'[^0-9A-Za-z]', '_', s)

def track_numberize(number):
    return str(number) if (number > 9) else '0' + str(number)

def track_image_label(number, artist, album):
  s = 'img_'
  n = 2

  track = track_numberize(number)
  cruft = '__' + track
  chunk_len = int(((maxlabel - len(s) - len(cruft))/n)) 
  
  s += simple_string(truncate_end(artist, chunk_len))
  s += '_'
  s += simple_string(truncate_end(album, chunk_len))
  s += '_'
  s += track_numberize(number)
  return s

def zero_pad(x):
    y = int(x)
    z = '0' if y <= 9 else ''
    return z + str(y)
     
def frames_to_time(frames):
    fps = 24
    seconds = int(frames / fps)
    minutes = int(seconds / 60)
    hours = int(minutes / 60)
    
    ss = seconds % 60
    mm = minutes % 60
    
    hh = '' if hours == 0 else (zero_pad(hours) + ":")
    return hh + zero_pad(mm) + ":" + zero_pad(ss)

def png_suffix():
  return '___' + XylemConfig.profile.tag + '.png'

def mkv_suffix():
  return '___' + XylemConfig.profile.tag + '.mkv'