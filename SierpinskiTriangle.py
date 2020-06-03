#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product
from PIL import Image, ImageDraw
import random
import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def save_animated_gif(filename, images, durations):
    """
    Save images as frames of an animated GIF.  Durations should specify the
    milliseconds to display each frame, and should be of the same length as
    images.
    """
    # https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#saving
    first_image, *other_images = images
    backwards_images = other_images[::-1] #reversing using list slicing
    all_images = other_images + backwards_images + [first_image]
    durations = durations + durations
    first_image.save(filename, save_all=True, append_images=all_images, duration=durations, loop=0)

def punch_hole(draw, x, y, length, hole_color):
    """
    For a triangle with a point at (x, y) and sides of length section_size,
    divide it into 4 tiles, and fill the center tile with background_color.
    """
    bottom_point = (x, y + math.sqrt(3) * length/2)
    left_point = (x - length/4, y + math.sqrt(3) * length/4)
    right_point = (x + length/4, y + math.sqrt(3) * length/4)
    draw.polygon((bottom_point, left_point, right_point), fill=hole_color)

def make_triangles(n, triangle_color, background_color):
    """
    Generate n PIL Images, each of Sierpiński's triangle with increasing levels
    of detail.
    """
    image_width = 343
    image_height = 297 
    image = Image.new("RGBA", (image_width, image_height), background_color)
    yield image
    image = image.copy()
    draw = ImageDraw.Draw(image)
    
    # draw first triangle
    draw.polygon([(0, image_height), (image_width/2, 0), (image_width,image_height)], fill = triangle_color)
    yield image
    image = image.copy()
    draw = ImageDraw.Draw(image)
    # draw frist hole
    punch_hole(draw, image_width/2, 0, image_width, background_color)
    #draw.polygon([(image_size/2,image_size), (image_size/4, image_size/2), (3*image_size/4,image_size/2)], fill = background_color)
    yield image
    for i in [-1, 0, 1]:
        image = image.copy()
        draw = ImageDraw.Draw(image)
        punch_hole(draw, image_width/2 + (i*image_width/4), abs(i) * (math.sqrt(3) * image_width/4), image_width/2, background_color)
    yield image

        
def random_color():
    """
    Generate a random hex color.
    """
    r = lambda: random.randint(0,255)
    return('#%02X%02X%02X' % (r(),r(),r()))

def main():
    N = 7
    
    triangle_color = random_color()
    background_color = random_color()
    
    #image = Image.new("RGBA", (N*3, N*3), background_color)

    triangles = make_triangles(N, triangle_color=triangle_color, background_color=background_color)
    durations = [800] * 6

    save_animated_gif("SierpinskiTriangle.gif", triangles, durations)

if __name__ == '__main__':
    main()