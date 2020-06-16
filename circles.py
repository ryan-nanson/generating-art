#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import division
import imageio, os
import matplotlib.pyplot as plt 
from matplotlib import patches

def circles(colors):
    fig = plt.figure(figsize=(10, 10))
    plt.subplots_adjust(hspace=0, wspace=0)

    for j in range(0, len(colors)):
        sub = fig.add_subplot(1,1,1)
        sub.set_xlim([0, 60])
        sub.set_ylim([0, 60])
        sub.axis('off')
        sub.add_patch(patches.Rectangle((0, 0), 100, 100, fc='#f5f2d0', 
                                        alpha=1, ec='none'))
    
        for i in range(0, len(colors)+1):
            x = 1
            for a in range(0, len(colors)):
                sub.add_patch(patches.Circle((5*x, 5+2*5*(i-1)), 5, 
                                             fc=colors[(a+j)%len(colors)], 
                                             alpha=1, ec='none'))
                x += 2  
        savename = str('tempImage' + str(j) + '.png')
        fig.savefig(savename, bbox_inches='tight')
        plt.clf()
        
    images = []
    for n in range(0, len(colors)):
        readname = str('tempImage' + repr(n) + '.png')
        images.append(imageio.imread(readname))

    imageio.mimsave('output/circles.gif', images, format='GIF', duration=.5)
    plt.close('all')

def deleteImages(numImages):
    '''Remove temp images made during GIF creation'''
    for i in range(0, numImages):
        imaeName = str('tempImage' + str(i) + '.png')
        try:
            os.remove(imaeName)
        except OSError:
            pass

def main():
    colors = ['#FF6663', '#FEB144', '#FFE868', '#9EE09E', '#9EC1CF', '#CC99C9']
    circles(colors)
    deleteImages(len(colors))

if __name__ == '__main__':
    main()