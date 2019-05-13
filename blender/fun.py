import bpy
import math
import os
import glob
import time

def deleteCamera():
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    # Select the object
    bpy.data.objects['Camera'].select = True    # Blender 2.7x
    # https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Python_API/Scene_and_Object_API
    #bpy.data.objects['Camera'].select_set(True) # Blender 2.8x
    bpy.ops.object.delete() 

def setCamera():
    
    try:
        deleteCamera()
    except:
        pass
    
    # camera
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, 0, 20), rotation=(0, -0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    #bpy.context.space_data.lock_camera = True
    camera = bpy.context.object
    
    camera.lock_location[2] = True
    camera.lock_location[1] = True
    camera.lock_location[0] = True
    camera.lock_rotation[2] = True
    camera.lock_rotation[1] = True
    camera.lock_rotation[0] = True
    
    bpy.context.scene.camera = camera


def putFullText(number, title, artist, album):
    
    textBoxWidth = 7
    textSize = 0.7
    sceneH = 11
    txtX = 0.4
    padY = 0.3
    
    s = trackNumberize(number) + ' - ' + title
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
    
    

#setCamera()
#putText('02 - Zerp')

def newScene(name, folder):
    try:
        delete_scene = bpy.data.scenes.get(name)
        bpy.data.scenes.remove(delete_scene, do_unlink=True)
    except:
        pass
    
    bpy.ops.scene.new(type='NEW')
    sc = bpy.context.scene
    sc.name = name
    sc.render.use_raytrace = False
    sc.render.use_sss = False
    sc.render.use_envmaps = False
    sc.render.alpha_mode = 'TRANSPARENT'
    sc.render.display_mode = 'SCREEN'
    sc.render.filepath = folder + name + '.png'


def newMovieScene(name, folder):
    try:
        delete_scene = bpy.data.scenes.get(name)
        bpy.data.scenes.remove(delete_scene, do_unlink=True)
    except:
        pass
    
    bpy.ops.scene.new(type='NEW')
    sc = bpy.context.scene
    sc.name = name
    sc.render.use_raytrace = False
    sc.render.use_sss = False
    sc.render.use_envmaps = False
    sc.render.alpha_mode = 'TRANSPARENT'
    sc.render.display_mode = 'SCREEN'
    sc.render.filepath = folder + name + '.mkv'

def trackNumberize(number):
    return str(number) if (number > 9) else '0' + str(number)

def sceneNameForOverlayTrack(number):
    return 'overlay_track_' + trackNumberize(number)

def makeTrackOverlay(number, title):
    newScene(sceneNameForOverlayTrack(number))
    setCamera()
    putText(trackNumberize(number) + ' - ' + title)

# ===================================================================
import struct
import imghdr

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height
    
# ===================================================================
def doCoverImage(folder, filename, frame_start, frame_end):
    area = bpy.context.area
    old_type = area.type
    area.type = 'SEQUENCE_EDITOR'
    bpy.ops.sequencer.image_strip_add(directory=folder, files=[{"name":filename, "name":filename}], frame_start=frame_start, frame_end=frame_end, channel=1)
    #bpy.context.scene.sequence_editor.sequences_all["cover.png"].use_translation = False
    #bpy.context.scene.sequence_editor.sequences_all["cover.png"].frame_final_duration = frame_end - frame_start
    
    #print(folder + ' :: ' + filename)
    #imgX, imgY = get_image_size(folder + filename)
    #vidX = 1920
    #vidY = 1080
    
    #bpy.ops.sequencer.effect_strip_add(frame_start=frame_start, frame_end=frame_end, type='TRANSFORM')
    #bpy.context.scene.sequence_editor.sequences_all["Transform"].scale_start_x = (imgX / vidX)
    #bpy.context.scene.sequence_editor.sequences_all["Transform"].scale_start_y = (imgY / vidY)
    
    bpy.context.area.type = old_type


def coverImage(folder):
    coverFgFilename = 'cover_fg.png'
    coverBgFilename = 'cover_bg.png'
    
    
    print(folder + ' :: ' + coverFgFilename)
    imgX, imgY = get_image_size(folder + coverFgFilename)
    
    theta = imgY / imgX
    
    bgX = 25
    bgY = bgX * theta
    
    bpy.ops.import_image.to_plane(files=[{"name":coverBgFilename, "name":coverBgFilename}], directory=folder, relative=False)
    bpy.context.object.active_material.use_shadeless = True

    bgImage = bpy.context.object
    
    bgImage.dimensions = bgX, bgY, 0
    bgImage.location = 0, 0, -2
    
    nice = 6.8
    
    fgX = nice
    fgY = fgX * theta
    xShift = 0
    
    if (fgY > fgX):
        fgY = nice
        fgX = fgY / theta
        xShift = (nice - fgX) / 3    
    
    bpy.ops.import_image.to_plane(files=[{"name":coverFgFilename, "name":coverFgFilename}], directory=folder, relative=False)
    bpy.context.object.active_material.use_shadeless = True
    fgImage = bpy.context.object
    
    fgImage.dimensions = fgX, fgY, 0
    fgImage.location = 0, 0, 0
    
    bpy.ops.transform.translate(value=(-4 + xShift, 0.5, 0))

def makeTrackScene(number, title, folder, artist, album):
    folder = folder + "\\"
    scene_name = sceneNameForOverlayTrack(number)
    newScene(scene_name, folder)
    setCamera()
    #putText(trackNumberize(number) + ' - ' + title)
    coverImage(folder)
    putFullText(number, title, artist, album)
    bpy.ops.render.render(write_still=True)
    #bpy.data.images["Render Result"].name = "Render Result"
    
    #scene_img = folder + scene_name + ".png"
    #bpy.ops.image.save_as(save_as_render=True, copy=True, filepath=scene_img, relative_path=True, show_multiview=False, use_multiview=False)

#makeTrackOverlay(1, 'Burgels')
#makeTrackOverlay(2, 'Durgles')
#makeTrackOverlay(3, 'Hamburgers')
#makeTrackOverlay(4, 'Dungeons and Dragons Dungeons and Dragons Dungeons and Dragons')
#makeTrackOverlay(5, 'Swords')
#makeTrackOverlay(6, 'Anger')


#makeTrackScene(1, 'A Great Debate', "C:\\Users\\Lucas\\Desktop\\xylem\\albums_wip\\A Small Glass Ghost - ∞\\", "A Small Glass Ghost", "∞")
#makeTrackScene(2, 'Jumping Jiggawatts, Great Balls Of Lightning', "C:\\Users\\Lucas\\Desktop\\xylem\\albums_wip\\A Small Glass Ghost - ∞\\", "cover.png")
#makeTrackScene(3, 'JKL jklk dus fhekeh fkd s a s fff eeee www Jumping Jiggawatts', "C:\\Users\\Lucas\\Desktop\\xylem\\albums_wip\\A Small Glass Ghost - ∞\\", "cover.png")

#makeTrackScene(2, 'sphere', "C:\\Users\\Lucas\\Desktop\\xylem\\albums_todo\\Norah Lorway - Sea of Strangers\\", "Norah Lorway", "Sea of Strangers")

this_folder = r'C:\Users\Lucas\Desktop\xylem\albums_wip'

def getData(albums_folder):

  data_out = []

  os.chdir(albums_folder)

  subfolders = [f.path for f in os.scandir(albums_folder) if f.is_dir() ]

  for folder in subfolders:
    #print(folder)
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
    
    data_out.append([folder, folder_out])
  return data_out

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

data = getData(this_folder)
for folderData in data:
    folder, albumData = folderData

    s_header = ''
    s_txt = ''
    
    for song in albumData:
        artist, album, track, trackTitle, filename = song
        # number, title, folder, artist, album):
        makeTrackScene(track, trackTitle, folder, artist, album)

    newMovieScene('movie', folder + "\\")
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
        
        overlay_png = sceneNameForOverlayTrack(track) + ".png"
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
        
    
def render_movie():
    scene = bpy.context.scene
    scene.frame_end = start
    scene.render.image_settings.file_format = 'FFMPEG'
    #scene.render.image_settings.file_format = 'XVID'
    #scene.render.ffmpeg.format = 'AVI'
    scene.render.ffmpeg.codec = 'H264'
    #scene.render.ffmpeg.audio_codec = 'MP3'
    #scene.render.ffmpeg.audio_bitrate = 320
    scene.render.ffmpeg.audio_codec = 'MP3'
    scene.render.ffmpeg.audio_bitrate = 320
    scene.render.ffmpeg.format = 'MKV'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.use_shadows = False
    bpy.ops.render.render(animation=True)
    