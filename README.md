# Long exposure with Pyglet, Pygame and Python

from WIKIPEDIA 
Long-exposure, time-exposure, or slow-shutter photography involves using a long-duration shutter speed to sharply capture the stationary elements of images while blurring, smearing, or obscuring the moving elements. Long-exposure photography captures one element that conventional photography does not: an extended period of time.
The paths of bright moving objects become clearly visible. Clouds form broad bands, vehicle lights draw bright streaks, stars leave trails in the sky, and water waves appear smooth. Only bright objects leave visible trails, whereas dark objects usually disappear. Boats in long exposures disappear during daytime, but draw bright trails from their lights at night.

# Requirments
if you are using the source Exposure.py you will need the following libraries

  - Pyglet  (pip install pyglet)
  
  - Pygame  (pip install pygame)
  
  - AVBin   https://avbin.github.io/AVbin/Download.html --> download AVbin binary installer
  
Pyglet installed without AVBin will throw the following error message 
- WAVEFormatException: AVbin is required to decode compressed media

# Supported media types
If AVbin is not installed, only uncompressed RIFF/WAV files encoded with linear PCM can be read.
With AVbin, many common and less-common formats are supported. Due to the large number of combinations of audio and video codecs, options, and container formats, it is difficult to provide a complete yet useful list. Some of the supported audio formats are:

AU, MP2, MP3, OGG/Vorbis, WAV, WMA

Some of the supported video formats are:

AVI, DivX, H.263, H.264, MPEG, MPEG-2, OGG/Theora, Xvid, WMV

For a complete list, see the AVbin sources. Otherwise, it is probably simpler to simply try playing back your target file with the media_player.py example.
New versions of AVbin as they are released may support additional formats, or fix errors in the current implementation. AVbin is completely future- and backward-compatible, so no change to pyglet is needed to use a newer version of AVbin – just install it in place of the old version.

# Usage
C:\>python Exposure.py -v Assets\\cascade11.ts -o LongExposure.png 

# Arguments
-video: you must pass the file path and file name as the video argument. E.g.: PATH\MyVideo.avi. (PATH = C:)

-output: you must pass the file path and file name for the output file (image). E.g. PATH\MyLongExposureEffect.png. (PATH = C:)

-iter: you can pass a step value as an argument. Its default value is 1. It is used to skip some frames and make the processing **faster. Keep in mind that using higher step values will result in losing frames/information. (must be > 0)

-start: starting averaging data from a specific position, default is t=0s. Must be >=0 

-end: End the averaging at a specific time, must be > 0

** The algorythm will not process the data for specific frames (This will slighly improve the overall process).

# Links for OPENCV
https://github.com/kelvins 
