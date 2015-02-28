#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import numpy as np
from scipy.io import wavfile

import Image
import ImageFont, ImageDraw

from random import choice

FACTOR = 1.30
FPS = 1

# Text position
X = 50
Y = 50

# Text colors
FILLCOLOR = "white"
SHADOWCOLOR = "black"


def speedup_audio(sound_array, factor):
    """ Multiplies the sound's speed by some factor
        source: http://goo.gl/MlI9UM """

    indices = np.round(np.arange(0, len(sound_array), factor))
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[indices.astype(int)]


def prepare_image(text, v_id):
    """ Load the specified image from file, add text to it and save it in the
        folder for temporary files with its unique id as filename. """

    # Select an image at random from a library
    image_file = choice([file for file in os.listdir("./images")])

    image = Image.open("./images/" + image_file)

    # TODO: translate the text to japanese (or fake japanese?)
    draw = ImageDraw.Draw(image)
    # Use unicode for kanji support
    unicode_text = unicode(text)

    font = ImageFont.truetype('font.ttf', 48)

    # Fake a border around the text
    draw.text((X-2, Y-2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X,   Y-2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X+2, Y-2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X+2, Y  ), text, font=font, fill=SHADOWCOLOR)
    draw.text((X-2, Y  ), text, font=font, fill=SHADOWCOLOR)
    draw.text((X-2, Y+2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X,   Y+2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X+2, Y+2), text, font=font, fill=SHADOWCOLOR)

    draw.text((X, Y), unicode_text, font=font, fill=FILLCOLOR)
    image.save("tmp/" + str(v_id) + ".png")


def prepare_audio(input_file, v_id):
    """ Speed up the input sound and save it in the temporary folder using its
        unique video id as filename. """

    rate, data = wavfile.read(input_file)
    data = speedup_audio(data, FACTOR)
    wavfile.write("tmp/" + str(v_id) + ".wav", rate, data)


def build_video(id):
    """ Combine the new audio and image to make a nightcore video """

    cmd = ('ffmpeg -loop 1 -r %s -i %s -i %s -shortest -acodec copy -f avi %s' %
        (FPS, "tmp/" + str(v_id) + ".png", "tmp/" + str(v_id) + ".wav", output_file))

    os.system(cmd)
    print 'Video is complete, output written to %s' % output_file


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "usage: nightcore.py <inputfile.wav> <outputfile.avi> <title>"
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    text = sys.argv[3]

    v_id = 1
    # v_id = generate_unique_id()

    # Prepare the image and audio. The files are saved to tmp/<unique id>
    prepare_image(text, v_id)
    prepare_audio(input_file, v_id)

    build_video(v_id)
