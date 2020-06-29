#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib, math, imageio, numpy, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt 
from matplotlib import patches

ar = numpy.array
imageFilePrefix = "tempImage"
imageFileType = ".png"
tileFileName = "output/octagonTile.gif"
wallFileName = "output/octagonWall.gif"

def Rotate2D(points, center, angle = numpy.pi/4):
    '''
    Rotates points about center by given angle in radians (default 45 degrees).
    '''
    return center + numpy.dot(points - center, 
                    ar([[numpy.cos(angle), numpy.sin(angle)], 
                         [-numpy.sin(angle), numpy.cos(angle)]]))

def addShape(points, c, alphaParam = 1):
    '''
    Add given shape and rotation to plot.
    '''
    origin = points[-1]
    # remove origin from list of points
    del points[-1]
    
    ots = Rotate2D(points, ar([origin])) 
    sub.add_patch(patches.Polygon(ots, fc=c, alpha=alphaParam, rasterized=True))

def quadrilateral(w, oX, oY, e = 0):
    '''
    Makes a quadrilateral with sides of length w, centered around the origin.
    '''
    p1 = [oX - w // 2, oY - w // 2]
    p2 = [oX + w // 2, oY + w // 2]
    p3 = [oX - (w - e) // 2, oY + (w - e) // 2]
    p4 = [oX + (w - e) // 2, oY - (w - e) // 2]
    return([p1, p2, p3, p4, [oX, oY]])

def octagon(w, oX, oY, e = 0):
    '''
    Makes an octagon with sides of length w, centered around the origin. 
    '''
    pts = quadrilateral(math.sqrt(2) * w, oX, oY)
    pts2 = quadrilateral(math.sqrt(2) * w - e, oX, oY)
    # remove origin before rotate
    del pts2[-1]
    ots = Rotate2D(pts2, ar([oX, oY])).tolist()
    return([pts[0], ots[0], pts[3], ots[3], pts[1], 
            ots[1], pts[2], ots[2], [oX, oY]])

def octagonTile(colours):
    '''
    Makes an octagon tiling GIF.
    '''
    global sub
    fig = plt.figure(figsize=(7, 1.75))
    plt.subplots_adjust(hspace = 0, wspace = 0)

    c1, c2, c3 = colours[:]

    originCoordinates = []
    for j in range(0, 3):
        for i in range(0, 9):
            originCoordinates.append([50*i, 50*j])

    numCoordinates = len(originCoordinates)

    ls = [28, 25, 22, 20, 17, 14, 12, 14, 17, 20, 22, 25, 28, 30]

    for x in range(0, len(ls)): # for every frame
        sub = fig.add_subplot(1, 1, 1)
        sub.set_xlim([0, 400])
        sub.set_ylim([0, 100])
        sub.axis('off')
        sub.add_patch(patches.Rectangle((0, 0), 400, 100, fc = c3, alpha = 1, 
                                        ec = 'none'))

        for n in range(0, numCoordinates // 2):
            # add alternate shapes one after another
            pts = octagon(ls[x], originCoordinates[2 * n][0], 
                          originCoordinates[2 * n][1], ls[x] - 32)
            addShape(pts, c2)
            
            pts = octagon(42 - ls[x], originCoordinates[(2 * n) + 1][0], 
                           originCoordinates[(2 * n) + 1][1], 7 - ls[x])
            addShape(pts, c1)
            
        # add the last shape (we have an add number)
        pts = octagon(ls[x], originCoordinates[numCoordinates - 1][0], 
                      originCoordinates[numCoordinates - 1][1], ls[x] - 32)
        addShape(pts, c2)

        savename = str(imageFilePrefix + repr(x) + imageFileType)
        fig.savefig(savename, bbox_inches = 'tight', pad_inches = 0, dpi = 50)
        plt.clf()

    makeTileGIF(len(ls))
    deleteImages(len(ls))
    plt.close('all')
    
def makeTileGIF(numImages):
    '''
    Make a single tile GIF from temp images, using the number of temp images.
    '''
    images = []
    for n in range(0, numImages):
        readname = str(imageFilePrefix + repr(n) + imageFileType)
        if (n+1) % 7 == 0:
            # add first, middle and last twice to add focus to end points.
            images.append(imageio.imread(readname))
        images.append(imageio.imread(readname))

    imageio.mimsave(tileFileName, images, format = 'GIF', duration = .15)
    
    
def makeWallGif():
    ''' 
    Make a wall GIF from the tile GIF.
    '''
    #read in tile GIF
    gif = imageio.get_reader(tileFileName)
    
    number_of_frames = gif.get_length()
    
    new_gif = imageio.get_writer(wallFileName)
    
    for frame_number in range(number_of_frames):
        img = gif.get_next_data()
        # two side by soide
        new_image = numpy.hstack((img, img))
        
        # stack on top of another
        for height in range(0,3):
            new_image = numpy.vstack((new_image, new_image))

        new_gif.append_data(new_image)
    
    gif.close()
    new_gif.close()

def deleteImages(numImages):
    '''
    Remove temp images made during GIF creation
    '''
    for i in range(0, numImages):
        imaeName = str(imageFilePrefix + str(i) + imageFileType)
        try:
            os.remove(imaeName)
        except OSError:
            pass

def stackImages(imageToStack):
    gif = imageio.get_reader(imageToStack)
    
    number_of_frames = gif.get_length()
    
    #Create writer object
    new_gif = imageio.get_writer('output/octagonWall.gif')
    
    for frame_number in range(number_of_frames):
        img = gif.get_next_data()
        # stack horizontally
        new_image = numpy.hstack((img, img))
        # stack vertically multiple times
        new_image = numpy.vstack((new_image, new_image))
        new_image = numpy.vstack((new_image, new_image))
        new_image = numpy.vstack((new_image, new_image))
        new_gif.append_data(new_image)
    
    gif.close()
    new_gif.close()
    

def main():
    colors = ['#ea907a', '#fbc687', '#f4f7c5']
    octagonTile(colors)
    stackImages('output/octagonTile.gif')
    

if __name__ == '__main__':
    main()