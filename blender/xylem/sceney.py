import bpy

def deleteCamera():
    bpy.ops.object.select_all(action='DESELECT')
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


def render_movie(do_render_step, frame_end):
    scene = bpy.context.scene
    scene.frame_end = frame_end
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
    if do_render_step:
        bpy.ops.render.render(animation=True)
    
