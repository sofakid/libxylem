from xylem.config import XylemConfig

class XylemCustom:
  pass

def XylemCustomize(number, title, artist, album):
    
  custom = XylemCustom()

  custom.centerline = 0
  custom.louise_chinese_text = False

  if XylemConfig.profile.tag == '720p':
    custom.do_insert_newlines_on_brackets = True
  else:
    custom.do_insert_newlines_on_brackets = False

  custom.do_track_numberize = True

  custom.album = False
  custom.artist = False
  
  if (artist == 'A Small Glass Ghost' and len(album) == 1):
    custom.do_insert_newlines_on_brackets = False

  if (artist == 'A Small Glass Ghost' and album == 'windchimes-synths'):
    custom.do_insert_newlines_on_brackets = False
      
  if (artist == 'Alex Charles'):
    if (album == 'Ocarina'):
      custom.do_track_numberize = False
    if (album == 'Singing Bowl'):
      custom.do_track_numberize = False

  if (artist == 'D.N.P' and album.startswith("RUSSIA")):
    custom.album = "RUSSIA, 1937-1957,\nTHE 'ANSWER'"
      
  if (artist == 'Nicholas Starke' and album == 'Abstraction'):
    custom.do_insert_newlines_on_brackets = False
      
  if (artist == 'Nick Starke' and album == 'Electro Iowa Winter'):
    custom.do_track_numberize = False
  
  if (artist == 'Gohj-ji' and album == 'Summer Romance'):
    custom.do_insert_newlines_on_brackets = False

  if (artist == 'D.N.P and David Duell'):
    custom.artist = 'D.N.P & David Duell'
    custom.album = 'The fullest roar I have ever heard'         
    
  if (artist == 'Louise Rossiter' and album == 'Traces' and number == 1):
    custom.do_insert_newlines_on_brackets = False
    custom.louise_chinese_text = True

  if (artist == 'madamme cell' and album == 'autotempo'):
    custom.do_track_numberize = False   
  
  if (artist == 'FIRE' and album == 'triangle'):
    custom.do_track_numberize = False

  if (artist == 'Francesco Sani' and album == 'of cosmic bodies and infinite'):
    custom.album = 'of cosmic bodies and infinite music'
    custom.centerline = 0.5

  if (artist == 'Lu_shush' and album == 'Something Shared'):
    custom.do_insert_newlines_on_brackets = False
  
  if (artist == 'Norah Lorway'):
    if (album == 'drone bølge III' or 
      album == 'superworlds' or
      album == 'THIS IS HOW THE WORLD WILL END' or
      album == 'w a v e c h a n g e'):
      custom.do_track_numberize = False
    if (album == 'WAKING'):
      custom.do_insert_newlines_on_brackets = False
  
  if (artist == "Ryan Roth" and album == "DISTILLED CORRUPTION"):
    custom.do_track_numberize = False
      
  if (artist == 'The Over Greenland' and album == 'The Evergreen Land'):
    custom.do_insert_newlines_on_brackets = False
            
  if (artist == 'Trevor Reznik' and album == 'Waves One & Two'):
    custom.do_track_numberize = False
      
  if (album == 'I Am A Dead Man'):
    custom.do_insert_newlines_on_brackets = False
  
  return custom
