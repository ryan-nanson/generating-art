#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Credit for the logic: https://www.youtube.com/watch?v=IRY1HoU2Qo0

from PIL import Image, ImageDraw
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def sierpinkspi(p1, p2, p3, degree, draw, image, colors):
    """
    Draw Sierpinksi Triangles.
    """
    colour = colors
    draw.polygon(((p1[0], p1[1]), (p2[0], p2[1]), (p3[0], p3[1])), fill=colour[degree])
    
    if degree > 0:
        sierpinkspi(p1, mid(p1, p2), mid(p1, p3), degree-1, draw, image, colors)
        sierpinkspi(p2, mid(p1, p2), mid(p2, p3), degree-1, draw, image, colors)
        sierpinkspi(p3, mid(p1, p3), mid(p2, p3), degree-1, draw, image, colors)
        
    else:
        return image
    
def mid(p1, p2):
    """
    Get mid point of two points.
    """
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]

def triangle(p1, p2, p3, colour, draw):
    """
    Draw a single Triangle.
    """
    logger.info(f"triangle:, {p1}, {p2}, {p3}")
    draw.polygon(((p1[0], p1[1]), (p2[0], p2[1]), (p3[0], p3[1])), fill=colour)
    return draw
        
def random_color():
    """
    Generate a random hex color.
    """
    r = lambda: random.randint(0,255)
    return('#%02X%02X%02X' % (r(),r(),r()))

def save_animated_gif(filename, images, durations):
    """
    Save images as frames of an animated GIF. Durations should specify the
    milliseconds to display each frame, and should be of the same length as
    images.
    """
    #set up images and durations to play GIF forward and back
    first_image, *other_images = images
    backwards_images = other_images[::-1]
    all_images = other_images + backwards_images + [first_image]
    durations = durations + durations

    logger.info("Creating GIF")
    first_image.save(fp=filename, format='GIF', save_all=True, 
                     append_images=all_images, duration=durations, loop=0)

def main():
    # set up constants
    degree = 6
    image_width, image_height = 690, 600
    frames = []
    
    # set up colors for images and gif 
    triangle_color, background_color = random_color(), random_color()
    colors = [background_color] * (degree - 1)
    colors.insert(0, triangle_color)

    # draw outer triangle
    p1, p2, p3 = [0, image_height], [image_width, image_height], [image_width/2, 0]
    
    # draw image for each layer of the Sierpinski Triangle
    for i in range(0, degree):
        logger.info(f"iteration: {i}")
        image = Image.new("RGBA", (690, 600), background_color)
        draw = ImageDraw.Draw(image) 
        sierpinkspi(p1, p2, p3, i, draw, image, colors)
        frames.append(image)
        # to save each intermediate image, unccoment the line below
        #image.save(f"output/triangle{i}.png")
    
    # set up times for gif
    durations = [800] * degree
    save_animated_gif("output/SierpinskiTriangle.gif", frames, durations)

if __name__ == '__main__':
    main()