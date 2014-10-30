#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-3-21

@author: kaka
'''
from __future__ import division
from PIL import Image
from pprint import pprint
import math

color_table = {'w':(255, 255, 255),  #White
               'y':(255, 255,   0),  #Yellow
               'b':(  0,   0, 255),  #Blue
               'g':(  0, 255,   0),  #Green
               'r':(255,   0,   0),  #Red
               'o':(255, 128,   0)}  #Orange

def euc_distance(p1, p2):
    '''
    calculate distance between p1 and p2
    '''
    distance = 0
    for i in range(len(p1)):
        distance += pow(p1[i]-p2[i], 2)
    distance = math.sqrt(distance)
    return distance

def changePixelColor(rgb):
    '''
    find the nearest color of rgb in color table
    '''
    min_distance = float("inf")
    for color in color_table.values():
        if euc_distance(rgb, color) < min_distance:
            min_distance = euc_distance(rgb, color)
            new_rgb = color
    return new_rgb

def getPixels(img, size):
    '''
    Get thumbnail of img according to size
    Then crop thumbnail to make sure the size is multiple of 3
    '''
    im = Image.open(img)
    im.thumbnail(size)
    new_size = im.size
    bl = 0
    bu = 0
    br = 3*math.floor(new_size[0]/3)
    bd = 3*math.floor(new_size[1]/3)
    im.crop([bl, bu, br, bd])
    pixels = list(im.getdata())
    return pixels,br,bd

def genPuzzle(pixels):
    '''
    Change the color of each pixel in pixels
    '''
    puzzle = []
    for i in range(len(pixels)):
        puzzle.append(changePixelColor(pixels[i]))
    return puzzle

def getPuzzleSize(img_size, cube_num):
    '''
    Get the size of thumbnail according to cube_num
    '''
    ratio = img_size[1]/img_size[0]
    x_num = math.floor(math.sqrt(cube_num/ratio))
    x = x_num*3
    y = math.floor(x*ratio)
    return [x,y]

def img2Puzzle(img, cube_num, outimg):
    '''
    Convert image to cube puzzle
    img: input image
    cube_num: max number of cube available
    outimg: output image(cube puzzle)
    '''
    im = Image.open(img)
    size = im.size
    p_size = getPuzzleSize(size, cube_num)
    pixels,width,height = getPixels(img, p_size)
    puzzle = genPuzzle(pixels)
    new_im = im.crop([0,0,int(width),int(height)])
    new_im.putdata(puzzle)
    new_im.save(outimg)
    return puzzle, width, height, width*height/9

if __name__ == "__main__":
    inImg = r'arsenal.jpg'
    outImg = r'pixel.jpg' 
    num = 200
    p, w, h, n = img2Puzzle(inImg, num, outImg)
    print "cube required: %d, %dx%d" % (n, w/3, h/3)
