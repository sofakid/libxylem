import bpy
import struct
import imghdr

# ===================================================================
# get_image_size: thanks stack overflow
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
# put the image in the video sequence
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

# put the images in the scene
def coverImage(cfg, folder):
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
