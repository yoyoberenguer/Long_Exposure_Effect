"""
This algorithm comes with a MIT license.

Copyright (c) 2018 Yoann Berenguer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

Please acknowledge and give reference if using the source code for your project
"""

# This program requires pyglet, numpy, pygame and AVbin
# pip install pyglet
# pip install pygame
# https://avbin.github.io/AVbin/Download.html --> download AVbin


__author__ = "Yoann Berenguer"
__copyright__ = "Copyright 2007."
__credits__ = ["Yoann Berenguer"]
__license__ = "MIT License"
__version__ = "2.0.0"
__maintainer__ = "Yoann Berenguer"
__email__ = "yoyoberenguer@hotmail.com"
__status__ = "Version 1"

import sys

try:
    import pygame
except ImportError:
    print('\nPygame library is missing.')
    print('Try C:\>pip install pygame.')
    raise SystemExit

try:
    import pyglet
except ImportError:
    print('\npyglet library is missing.')
    print('Try C:\>pip install pyglet.')
    raise SystemExit

try:
    import numpy
except ImportError:
    print('\nnumpy library is missing.')
    print('Try C:\>pip install numpy.')
    raise SystemExit

import time as time
import argparse
import os

# All compatible video formats
# For a complete list, see the AVbin sources.
compatible = ['AVI', 'DivX', 'H.263', 'H.264', 'MPEG', 'MPEG-2', 'OGG/Theora', 'Xvid', 'WMV']
# video info
header = {'Title': 'source.info.title',
          'Author': 'source.info.author',
          'Copyright': 'source.info.copyright',
          'Comment': 'source.info.comment',
          'Album': 'source.info.album',
          'Year': 'source.info.year',
          'Track': 'source.info.track',
          'Genre': 'source.info.genre'
          }


class ProgressBar(object):

    def __init__(self, total, prefix='Progress:', suffix='Complete', decimals=2, bar_length=50):
        """
        It is used to show a progress bar.
        :param total: the total value of the progress bar (100%)
        :param prefix: the prefix show before the progress bar (default is 'Progress:')
        :param suffix: the suffix show after the progress bar (default is 'Complete')
        :param decimals: the number of decimal places
        :param bar_length: the length/width of the progress bar
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.bar_length = bar_length

    def update(self, progress):
        """
        Function used to update the progress bar.
        :param progress: the current progress (should be lower than the total)
        """
        str_format = "{0:." + str(self.decimals) + "f}"
        percents = str_format.format(100 * (progress / float(self.total)))
        filled_length = int(round(self.bar_length * progress / float(self.total)))
        bar = '#' * filled_length + '-' * (self.bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (self.prefix, bar, percents, '%', self.suffix))

        if progress >= self.total:
            sys.stdout.write('\n')
        sys.stdout.flush()


if __name__ == '__main__':
    numpy.set_printoptions(threshold=numpy.nan)
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True, help="Path to input video file")
    ap.add_argument("-o", "--output", required=True, help="Path to output 'long exposure' image")
    ap.add_argument("-i", "--iter", type=int, default=1, help="Step used to get the iteration, must be >0")
    ap.add_argument("-s", "--start", type=int, default=0, help="Starting playback, must be >=0")
    ap.add_argument("-e", "--end", type=int, default=None, help="End time, must be >0")
    args = vars(ap.parse_args())

    player = pyglet.media.Player()
    video = args["video"]
    output = args["output"]
    assert os.path.isfile(video), '\n[-] Error - Video not found.'
    assert int(args['step']) > 0, '\n[-] Error - invalid int value for argument step: %s ' % str(args['step'])
    assert args['start'] >= 0, '\n[-] Error - invalid int value for argument start: %s ' % str(args['start'])
    if args['end'] is not None:
        assert args['end'] > 0, '\n[-] Error - invalid int value for argument start: %s ' % str(args['end'])
        assert args['end'] > args['start'], '\n[-] Error - Wrong start/end time, start time must be < end time. '

    try:
        source = pyglet.media.load(video, streaming=True)
    except Exception as e:
        print('\n[-] Error - Could not open the video ' + str(video))
        raise SystemExit


    vformat = source.video_format
    player.queue(source)
    player.play()

    path = os.path.realpath(video)

    if source:
        print('Duration         : %s seconds' % source.duration)
        if args['end'] is not None and args['end'] > source.duration:
            print('[-] Warning - End time out of range, value is adjusted to %s\n' % source.duration)
        assert args['start'] < source.duration,\
            '[-] Error - Start time is over the allowed playback time.'

        print('Video            : %s ' % path)
        print('Video width      : %s pixels ' % vformat.width,
              '\nVideo height     : %s pixels ' % vformat.height,
              '\nAspect ratio     : %s        ' % vformat.sample_aspect,
              '\nVideo frame rate : %s fps    ' % vformat.frame_rate)
        if source.info is not None:
            for info in header:
                cmd = str(eval(header[str(info)]))
                width = len(cmd)
                print("{: <9} {: >8} {: >{}}".format(str(info), ':', cmd, str(width)))

        print('\n')
    else:
        print('\n[-] Error - Could not read the video header. ')
        print('[-] Info  - Make sure the video format is compatible (list below).')
        print('[-] Info  - ' + str(compatible))
        raise SystemExit

    # Frame number approximation
    number_of_frames = int(vformat.frame_rate * source.duration)
    if args['step'] > number_of_frames:
        print('\n[-] Error - Step value is a little too high!, value adjusted to 1.')
        args['step'] = 1

    # Initialize the progress bar
    progress_bar = ProgressBar(number_of_frames)
    progress_bar.update(0)

    pygame.init()
    screen = pygame.display.set_mode((vformat.width, vformat.height), 0)
    window = pyglet.window.Window(visible=False)

    # Array for summing all the pixels.
    # The pixels averaging over the time will create the long exposure effect.
    summing_array = numpy.full((vformat.width, vformat.height, 3), 0)

    start = args['start']
    stop = args['end'] if args['end'] is not None else source.duration

    print("\n[+] Info - Video starting at %s " % start)
    print("[+] Info - Video stopping at %s " % stop)
    print("[+] Info - Step %s iteration \n" % args['step'])

    # Variable initialisation
    iteration = 1
    processed_frame = 0
    step = int(args['step'])
    signal = True
    frame = 0

    player.source.seek(start)

    play_time = 0

    while signal:

        t = time.time()
        # Another frame
        iteration += 1

        pyglet.clock.tick()

        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')

        pygame.event.pump()

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                signal = False
            if keys[pygame.K_ESCAPE]:
                signal = False
        pygame.event.clear()

        if iteration % step == 0 and player.time >= start:
            # An image of any class can be converted into a Texture or ImageData
            # using the get_texture and get_image_data methods defined on AbstractImage
            texture = player.get_texture()
            # Accessing or providing pixel data
            # The ImageData class represents an image as a string or sequence of pixel data,
            # or as a ctypes pointer.Details such as the pitch and component layout
            # are also stored in the class.You can access an ImageData object for
            # any image with get_image_data
            # For example, a vformat string of "RGBA" corresponds to four bytes of colour data,
            # in the order red, green, blue, alpha. Note that machine endianness has no impact
            #  on the interpretation of a vformat string.
            # To retrieve pixel data in a particular vformat, use the get_data method,
            # specifying the desired vformat and pitch. The following example reads tightly packed rows in RGBA vformat
            # data always returns a string, however it can be set to a ctypes array, stdlib array,
            # list of byte data, string, or ctypes pointer. To set the image data use set_data,
            #  again specifying the vformat and pitch
            raw = texture.get_image_data().get_data('RGBA', texture.width * 4)

            # Interpret a buffer as a 1 dimensional array and reshape it
            buff = numpy.frombuffer(raw, dtype=numpy.uint8).reshape(texture.height, texture.width, 4)
            # create the rgb array (remove the alpha channel) and transpose axes (flipped the surface)
            summing_array += buff[:, :, :3].transpose(1, 0, 2)

            if processed_frame > 0:
                pygame.surfarray.blit_array(screen, summing_array / (processed_frame + 1))
            else:
                pygame.surfarray.blit_array(screen, summing_array)

            processed_frame += 1

            progress_bar.update(frame)

        if source.get_next_video_timestamp() is None:
            signal = True
            break
        else:
            if source.get_next_video_timestamp() >= stop or player.time > source.duration:
                signal = False

        pygame.display.flip()

        # Keep the frame rate below the video fps
        while time.time() - t < (1 / vformat.frame_rate - 1.89e-3):
            time.sleep(0.0001)

        # Elapsed time since video has started
        # for a video with 25 fps, add 40ms for every frame
        play_time += 1 / vformat.frame_rate

        # Exact frame number corresponding to the elapsed time * fps
        frame = round(player.time * vformat.frame_rate, 1)

    # Make sure that the progress bar state is 100%
    progress_bar.update(number_of_frames)

    # Write the long exposure image to disk
    pygame.image.save(screen, str(args['output']))
    print('Image %s saved' % args['output'])
    print('Processed : %s images' % processed_frame)
    print('\n[+] Frames: %s, play time: %s ' % (frame, player.time))