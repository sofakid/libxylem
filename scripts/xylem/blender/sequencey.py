import bpy
import os

from xylem.stringy import track_image_label, png_suffix

def find_sequencer_area():
  bpy.context.window.screen = bpy.data.screens['Video Editing']
  screens = [bpy.context.screen]+list(bpy.data.screens)
  for screen in screens:
    for area in screen.areas:
      if area.type == 'SEQUENCE_EDITOR':
        return area
  return None

def sequence_add_image(folder, filename, frame_start, frame_end):
    area = find_sequencer_area()
    bpy.ops.sequencer.image_strip_add(
      {'area':area},
      directory=folder,
      files=[{ "name": filename, "name": filename }],frame_start=frame_start,
      frame_end=frame_end,
      channel=1)

def sequence_add_sound(full_path, filename):
    area = find_sequencer_area()
    
    bpy.ops.sequencer.sound_strip_add(
      {'area':area},
      filepath=full_path, 
      files=[{"name":filename, "name":filename}],
      relative_path=True, frame_start=1, channel=1)

    return bpy.context.scene.sequence_editor.active_strip

def sequence_add_sound_and_image(folder, soundfile, artist, album, track, start):
  full_path = os.path.join(folder, album)
  
  sound_strip = sequence_add_sound(full_path, soundfile)
  
  dur = sound_strip.frame_duration
  sound_strip.frame_start = start
  
  scene_png = track_image_label(track, artist, album) + png_suffix()
  sequence_add_image(folder, scene_png, start, start + dur)

  return dur
