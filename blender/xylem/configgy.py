
class XylemConfig:
  pass

  
def xylemConfigure(number, title, artist, album):
    
    cfg = XylemConfig()

    cfg.centerline = 0
    cfg.louise_chinese_text = False
    cfg.do_insert_newlines_on_brackets = True
    cfg.do_track_numberize = True

    cfg.album = False
    cfg.artist = False
    
    if (artist == 'A Small Glass Ghost' and len(album) == 1):
        cfg.do_insert_newlines_on_brackets = False
        
    if (artist == 'D.N.P' and album.startswith("RUSSIA")):
        cfg.album = "RUSSIA, 1937-1957,\nTHE 'ANSWER'"
       
    if (artist == 'Nicholas Starke' and album == 'Abstraction'):
        cfg.do_insert_newlines_on_brackets = False
        
    if (artist == 'Nick Starke' and album == 'Electro Iowa Winter'):
        cfg.do_track_numberize = False
    
    if (artist == 'Gohj-ji' and album == 'Summer Romance'):
        cfg.do_insert_newlines_on_brackets = False

    if (artist == 'D.N.P and David Duell'):
        cfg.artist = 'D.N.P & David Duell'
        cfg.album = 'The fullest roar I have ever heard'         
        
    if (artist == 'Louise Rossiter' and album == 'Traces' and number == 1):
        cfg.do_insert_newlines_on_brackets = False
        cfg.louise_chinese_text = True

    if (artist == 'madamme cell' and album == 'autotempo'):
        cfg.do_track_numberize = False   
    
    if (artist == 'Norah Lorway'):
        if (album == 'drone bølge III' or 
            album == 'superworlds' or
            album == 'THIS IS HOW THE WORLD WILL END' or
            album == 'w a v e c h a n g e'):
            cfg.do_track_numberize = False
        if (album == 'WAKING'):
            cfg.do_insert_newlines_on_brackets = False
    
    if (artist == "Ryan Roth" and album == "DISTILLED CORRUPTION"):
        cfg.do_track_numberize = False
        
    if (artist == 'The Over Greenland' and album == 'The Evergreen Land'):
        cfg.do_insert_newlines_on_brackets = False
              
    if (artist == 'Trevor Reznik' and album == 'Waves One & Two'):
        cfg.do_track_numberize = False
        
    if (album == 'I Am A Dead Man'):
        cfg.do_insert_newlines_on_brackets = False
    
    return cfg
