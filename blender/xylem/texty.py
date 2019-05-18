from xylem.stringy import *
import bpy

def putFullText(cfg, number, title, artist, album):
     
    textBoxWidth = 7
    textSize = 0.7
    sceneH = 11
    txtX = 0.4
    padY = 0.4
    chineseTxt = False
    
    if (cfg.artist != False):
      artist = cfg.artist
    
    if (cfg.album != False):
      album = cfg.album

    if (cfg.louise_chinese_text):
        title = '                   (Our Song)'        
        bpy.ops.font.open(filepath="", relative_path=True)

        chineseFnt = bpy.data.fonts.load('C:\\Windows\\Fonts\\BIZ-UDMinchoM.ttc')
    
        chinese = r' 我們的歌'
        bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=(1.2, 0.9, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        chineseTxt = bpy.context.object
        chineseTxt.data.body = chinese
        chineseTxt.data.font = chineseFnt
        chineseTxt.data.size = textSize
        chineseTxt.data.text_boxes[0].width = textBoxWidth
        bpy.context.scene.update()
        chineseTxtW, chineseTxtH, foo = chineseTxt.dimensions
        
    s = ""
    if cfg.do_track_numberize:
        s = trackNumberize(number) + ' - ' + title
    else:
        s = title
    
    if cfg.do_insert_newlines_on_brackets:
        s = s.replace("(", "\n(")
    
    fnt = bpy.data.fonts.load('C:\\Users\\Lucas\\Desktop\\xylem\\fonts\\Futura Std Book.ttf')
    
    bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    titleTxt = bpy.context.object
    titleTxt.data.body = s
    titleTxt.data.font = fnt
    titleTxt.data.size = textSize
    titleTxt.data.text_boxes[0].width = textBoxWidth
    bpy.context.scene.update()
    titleTxtW, titleTxtH, foo = titleTxt.dimensions
    
    bpy.ops.transform.translate(value=(txtX, titleTxtH + padY, -0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    
    
    bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    albumInfoTxt = bpy.context.object
    albumInfoTxt.data.body = artist + '\n' + album
    albumInfoTxt.data.font = fnt
    albumInfoTxt.data.size = textSize
    albumInfoTxt.data.text_boxes[0].width = textBoxWidth
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
    
