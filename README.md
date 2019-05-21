libxylem
========

Requirements
------------

Software
* Blender 2.79b - note the path of the executable
* ImageMagick - note path to magick
* FFmpeg - note path to ffmpeg
* Python 3

Data
* Albums in the file-naming format you'd get from Bandcamp:
  * `artist - album/artist - album - 01 song.mp3`
  * `cover.png` or `cover.jpg`

If you are renaming things manually, and can't use weird charcters in the folder name, use another character (like `_`), but make sure it's the same length as the album in the mp3 file names.

Install
-------

* clone git repo somewhere simple.
* Create a folder to put albums in, to be processed.
* Edit `scripts/xylem/config.py`
  * set `albums_folder` to the processing folder you just made
  * set paths to the executables for `blender`, `magick`, `ffmpeg`
  * `profile` is how you choose the output resolution and shape
    * 720p is `Profile_1280x720()`
    * wider is `Profile_1920x854()`
    * there's a few others to play with but they're unfinished

Formats
-------
Inputs:
* Only tested with 320kbps mp3s, but others probably work, maybe.
* album artwork in `png` or `jpg`

Outputs: 
* `mkv` files
* `h.264` video
* `mp3` audio
* `320kbps` audio bitrate

To change output formats look in `xylem/blender/sceney.py`

Workflow
--------

Copy albums to `albums_folder`. All the outputs go into each album folder, like, alongside the mp3s and the cover.  

Open a terminal, `cd` to the `scripts` folder in the git repo.

Step 1: `python processCovers.py`
---------------------------------
This will use imagemagick to create:
  * `cover_fg.png` -- Just a `.png` version of cover.png/.jpg
  * `cover_bg.png` -- A blurred and darkened version of the cover
  * these files will be in the album folder alongside the mp3s, all output will.

Step 2: `python generateThumbnails.py`
-------------------------------------- 
* makes `thumbnail_yt.png` -- a 1280x720 youtube thumbnail

Step 3: `python renderImages.py`
--------------------------------

This will use blender to render scene images for each track. At this point go look at them and see if anything needs tweaking.

Tweaks you can do:
  * edit `cover_bg.png` in an image editor.
  * change font in `xylem/config.py`
  * put special cases in `xylem/customy.py`
    * change the text
    * move the text up or down
    * change default behaviour of showing track numbers or putting newlines on brackets
  * hack at the code

Now the images look good, render the albums with:

Step 4: `python renderTracks.py`
--------------------------------
Video rendering is slow and single-threaded with blender, so we start a bunch of blenders to render the track videos. This number is calculated as 75% of the number of cores (real or hyper).

When this step is done, the track videos will be concatenated with ffmpeg into a full album video. (this step is very fast)

Look in the album folder for these files:
* `album_...`
* `trk_...`

Additional YouTube asset created:
* `nfo.txt` -- a list of songs preceded by timestamps, paste into description so people can click to skip to the song in a full album video

