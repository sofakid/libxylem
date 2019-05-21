from xylem.stringy import *
from xylem.config import XylemConfig
import bpy

def putFullText(custom, number, title, artist, album, x_shift):
     
  ox = XylemConfig.profile.origin_x + x_shift
  oy = XylemConfig.profile.origin_y

  textBoxWidth = XylemConfig.profile.textbox_w
  textSize = XylemConfig.profile.text_h
  songSize = XylemConfig.profile.song_h
  txtX = 0.4
  padY = 0.4
  chineseTxt = False
  
  if (custom.artist != False):
    artist = custom.artist
  
  if (custom.album != False):
    album = custom.album

  if (custom.louise_chinese_text):
    title = '                   (Our Song)'        
    bpy.ops.font.open(filepath="", relative_path=True)

    chineseFnt = bpy.data.fonts.load('C:\\Windows\\Fonts\\BIZ-UDMinchoM.ttc')

    chinese = r' 我們的歌'

    if XylemConfig.profile.tag == '720p':
      omega_x = 1.29
      omega_y = 0.9
    elif XylemConfig.profile.tag == 'wider':
      omega_x = 1.35
      omega_y = 1.05
    else:
      omega_x = 0
      omega_y = 0


    chinese_x = ox + omega_x
    chinese_y = oy + omega_y

    bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=(chinese_x, chinese_y, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    chineseTxt = bpy.context.object
    chineseTxt.data.body = chinese
    chineseTxt.data.font = chineseFnt
    chineseTxt.data.size = songSize
    chineseTxt.data.text_boxes[0].width = textBoxWidth
    #bpy.context.scene.update()
    #chineseTxtW, chineseTxtH, foo = chineseTxt.dimensions
    
  s = ""
  if custom.do_track_numberize:
    s = track_numberize(number) + ' - ' + title
  else:
    s = title
  
  if custom.do_insert_newlines_on_brackets:
    s = s.replace("(", "\n(")
  
  fnt = bpy.data.fonts.load(XylemConfig.font)
  
  bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=(ox, oy + custom.centerline, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
  titleTxt = bpy.context.object
  titleTxt.data.body = s
  titleTxt.data.font = fnt
  titleTxt.data.size = songSize
  titleTxt.data.text_boxes[0].width = textBoxWidth - x_shift
  bpy.context.scene.update()
  titleTxtW, titleTxtH, foo = titleTxt.dimensions
  
  bpy.ops.transform.translate(value=(txtX, titleTxtH + padY, -0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
  
  
  bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=(ox, oy + custom.centerline, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
  albumInfoTxt = bpy.context.object
  albumInfoTxt.data.body = artist + '\n' + album
  albumInfoTxt.data.font = fnt
  albumInfoTxt.data.size = textSize
  albumInfoTxt.data.text_boxes[0].width = textBoxWidth - x_shift
  bpy.context.scene.update()
  albumInfoTxtW, albumInfoTxtH, fooTwo = albumInfoTxt.dimensions
  
  bpy.ops.transform.translate(value=(txtX, 0 - padY, -0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
  #bpy.ops.transform.translate(value=(txtX, albumInfoTxtH/2, -0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
  
  # Get material
  mat = bpy.data.materials.get("Material")
  if mat is None:
    # create material
    mat = bpy.data.materials.new(name="Material")

  mat.use_shadeless = True
  mat.diffuse_color = (1, 1, 1)
  
  def assignMat(o):
    if o.data.materials:
      # assign to 1st material slot
      o.data.materials[0] = mat
    else:
      # no slots
      o.data.materials.append(mat)
      
  assignMat(titleTxt)
  assignMat(albumInfoTxt)    
  
  if (chineseTxt != False):
    assignMat(chineseTxt)
  
