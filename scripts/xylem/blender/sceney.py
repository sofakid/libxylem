import bpy
import os

from xylem.config import XylemConfig
from xylem.stringy import *

def delete_camera():
  bpy.ops.object.select_all(action='DESELECT')
  bpy.data.objects['Camera'].select = True    # Blender 2.7x
  # https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Python_API/Scene_and_Object_API
  #bpy.data.objects['Camera'].select_set(True) # Blender 2.8x
  bpy.ops.object.delete() 

def set_camera():
    
  try:
    delete_camera()
  except:
    pass
  
  # camera
  bpy.ops.object.camera_add(location=(0, 0, XylemConfig.profile.camera_z), rotation=(0, -0, 0))
  #bpy.context.space_data.lock_camera = True
  camera = bpy.context.object
  
  camera.lock_location[2] = True
  camera.lock_location[1] = True
  camera.lock_location[0] = True
  camera.lock_rotation[2] = True
  camera.lock_rotation[1] = True
  camera.lock_rotation[0] = True
  
  bpy.context.scene.camera = camera


def new_scene(name, folder):
  try:
    delete_scene = bpy.data.scenes.get(name)
    bpy.data.scenes.remove(delete_scene, do_unlink=True)
  except:
    pass
  
  outfile = name + png_suffix()

  bpy.ops.scene.new(type='NEW')
  scene = bpy.context.scene
  scene.name = name
  scene.render.use_raytrace = False
  scene.render.use_sss = False
  scene.render.use_envmaps = False
  scene.render.alpha_mode = 'TRANSPARENT'
  scene.render.display_mode = 'SCREEN'
  scene.render.filepath = os.path.join(folder, outfile)
  scene.render.resolution_percentage = 100
  scene.render.resolution_x = XylemConfig.profile.res_x
  scene.render.resolution_y = XylemConfig.profile.res_y


def new_movie_scene(name, folder):
  try:
    delete_scene = bpy.data.scenes.get(name)
    bpy.data.scenes.remove(delete_scene, do_unlink=True)
  except:
    pass
  
  outfile = name + mkv_suffix()

  bpy.ops.scene.new(type='NEW')
  scene = bpy.context.scene
  scene.name = name
  scene.render.use_raytrace = False
  scene.render.use_sss = False
  scene.render.use_envmaps = False
  scene.render.alpha_mode = 'TRANSPARENT'
  scene.render.display_mode = 'SCREEN'
  scene.render.filepath = os.path.join(folder, outfile)

  if not scene.sequence_editor:
    scene.sequence_editor_create()

  return scene

def render_movie(do_render_step, frame_end):
  scene = bpy.context.scene
  scene.frame_end = frame_end
  scene.render.image_settings.file_format = 'FFMPEG'
  scene.render.ffmpeg.codec = 'H264'
  scene.render.ffmpeg.audio_codec = 'MP3'
  scene.render.ffmpeg.audio_channels = 'STEREO'
  scene.render.ffmpeg.audio_bitrate = 320
  scene.render.ffmpeg.format = 'MKV'
  scene.render.ffmpeg.constant_rate_factor = 'HIGH'
  scene.render.resolution_percentage = 100
  scene.render.resolution_x = XylemConfig.profile.res_x
  scene.render.resolution_y = XylemConfig.profile.res_y
  scene.render.use_shadows = False
  if do_render_step:
    bpy.ops.render.render(animation=True)
    
