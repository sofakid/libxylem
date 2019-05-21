
class Profile_1280x720:
  def __init__(self):
    self.tag = '720p'
    self.origin_x = 0
    self.origin_y = 0
    self.res_x = 1280
    self.res_y = 720
    self.camera_z = 20
    self.textbox_w = 7
    self.text_h = 0.7
    self.song_h = 0.9
    self.bg_w = 25
    self.fg_raise = 0.5

class Profile_1920x854:
  def __init__(self):
    self.tag = 'wider'
    self.origin_x = -3
    self.origin_y = 0
    self.res_x = 1920
    self.res_y = 854
    self.camera_z = 25
    self.textbox_w = 13
    self.text_h = 0.7
    self.song_h = 0.9
    self.bg_w = 25
    self.fg_raise = 0.7
    
class Profile_1920x400:
  def __init__(self):
    self.tag = 'thin'
    self.origin_x = -14
    self.origin_y = 0
    self.res_x = 1920
    self.res_y = 400
    self.camera_z = 50
    self.textbox_w = 30
    self.text_h = 1.5
    self.song_h = 2

    self.bg_w = 50
    self.fg_raise = 0
    
class Profile_1280x1280:
  def __init__(self):
    self.tag = 'square'
    self.origin_x = -3
    self.origin_y = 6
    self.res_x = 1280
    self.res_y = 1280
    self.camera_z = 25
    self.textbox_w = 20
    self.text_h = 0.7
    self.song_h = 0.9

    self.bg_w = 25
    self.fg_raise = 0
    
#0.9 * x = 1.2
#x = 1.2/0.7 = 1.71
