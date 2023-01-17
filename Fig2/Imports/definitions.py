# ----------------------------------------------------------------------------
# DiSCUS - definitions file
# http://code.google.com/p/discus/
# Angel Goni-Moreno - www.angelgm.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------


import pymunk
from parameters import *
import pygame
from pygame.locals import *
from pygame.color import *

def add_bac(space,x,y,angle,points):
### Function used to place a new cell in the world.
### In: the space into which a bacteria must be created, its coordinates and angle.
### Out: returns a shape with a body assigned
    mass = bac_mass
    moment = pymunk.moment_for_poly(mass, points, (0,0))
    body = pymunk.Body(mass, moment)
    body.position = x, y
    body.angle =  angle
    shape = pymunk.Poly(body, points, (0,0))
    shape.friction = bac_friction
    shape.elasticity = 0.00
    space.add(body,shape)
    return shape

def get_centres(points):
### Function used to obtain the centres of daughter cells in division
### In: four points of a rectangle
### Out: returns the middle point and the centre of the left side
    #centre = ((points[2][0]+points[7][0])/2, (points[2][1]+points[7][1])/2)
    #centre_left =  points[2]

    x_2 = points[2][0]
    y_2 = points[2][1]
    x_7 = points[7][0]
    y_7 = points[7][1]
 
    x_dif = max(points[2][0],points[7][0])-min(points[2][0],points[7][0])
    y_dif = max(points[2][1],points[7][1])-min(points[2][1],points[7][1])


    if y_2==y_7 and x_2<x_7: #1
        centre_left = (x_2+1/4.*x_dif,y_2)
        centre_right = (x_2+3/4.*x_dif,y_2)
    elif y_2==y_7 and x_2>x_7: # 2
        centre_left = (x_7+1/4.*x_dif,y_2)
        centre_right = (x_7+3/4.*x_dif,y_2)
    elif x_2==x_7 and y_2<y_7: # 3'
        centre_left = (x_2,y_2+1/4.*y_dif)
        centre_right = (x_2,y_2+3/4.*y_dif)
    elif x_2==x_7 and y_2>y_7: #3
        centre_left = (x_2,y_7+1/4.*y_dif)
        centre_right = (x_2,y_7+3/4.*y_dif)
    elif x_2<x_7 and y_2<y_7: #4
        centre_left = (x_2+1/4.*x_dif,y_2+1/4.*y_dif)
        centre_right = (x_2+3/4.*x_dif,y_2+3/4.*y_dif)
    elif x_2<x_7 and y_2>y_7: #5
        centre_left = (x_2+1/4.*x_dif,y_2-1/4.*y_dif)
        centre_right = (x_2+3/4.*x_dif,y_2-3/4.*y_dif)
    elif x_2>x_7 and y_2>y_7: #6
        centre_left = (x_2-1/4.*x_dif,y_2-1/4.*y_dif)
        centre_right = (x_2-3/4.*x_dif,y_2-3/4.*y_dif)  
    elif x_2>x_7 and y_2<y_7: #6
        centre_left = (x_2-1/4.*x_dif,y_2+1/4.*y_dif)
        centre_right = (x_2-3/4.*x_dif,y_2+3/4.*y_dif)
    else:
        print "eeeeehh??? get_centres()" 


    return (centre_left, centre_right)

def hex_to_rgb(value):
### Function used to convert an hexagonal value into a rgb value
### In: hexagonal value
### Out: RGB value
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def draw_bac(screen, bac, partner, min_partner, dif):
### Function used to draw a cell in the screen for live video
### In: the cell and the screen in which it must be draw 
### Out: popup window with live video
    body = bac.shape.body
    ps = bac.shape.get_vertices()
    color = THECOLORS["green"]
    cell_color = hex_to_rgb(calculateColor(partner, min_partner, dif))
    if len(ps) > 2:
        pygame.draw.polygon(screen, cell_color, ps)
        pygame.draw.polygon(screen, THECOLORS["black"], ps,1)

def draw_lines(screen, lines):
### Function used to draw the walls in the screen for live video
### In: the lines and the screen into which they must be drawn
### Out: popup window with live video
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        pygame.draw.lines(screen, THECOLORS["black"], False, [pv1,pv2])

def look_mate(mate_shape, bacs):
### Function used to look for a shape in a list of cells
### In: a shape and a list of cells
### Out: the cell found or None
    for bac in bacs:
        if bac.shape == mate_shape: return bac

def look_bac(body, bacs):
### Function used to look for a body in a list of cells
### In: a body and a list of cells
### Out: the cell found or None
    for bac in bacs:
        if bac.shape.body == body: return bac

def calculateGravity(bx, by):
### Function add gravity towards a specific point
### In: coordinates of the cell
### Out: new coordinates according to the gravity defined
    centre_sc = (screenview/2, screenview/2)
    if bx > centre_sc[0]:
        gr_x = -0.045
    else:
        gr_x = 0.045
    if by > centre_sc[1]:
        gr_y = -0.045
    else:
        gr_y = 0.045
    return (gr_x,gr_y)

def calculateColor(p, min_p, dif):
### Function to calculate gradual colour according to a value				
### In: the value to associate a colour
### Out: the hexadecimal green colour proportional 

    if p<(min_p+0.2*dif):
        final_color = '#110000'
    elif p<(min_p+0.4*dif):
        final_color = '#440000'
    elif p<(min_p+0.6*dif):
        final_color = '#770000'
    elif p<(min_p+0.8*dif):
        final_color = '#AA0000'
    else:
        final_color = '#DD0000'
					
#    if x in (1,2,3):				
#        final_color = '#0000FF'			
#    elif x in (4,5):								
#        final_color = '#1111FF'							
#    elif x == 6:								
#        final_color = '#2222FF'							
#    elif x == 7:								
#        final_color = '#3333FF'							
#    elif x == 8:							
#        final_color = '#4444FF'							
#    elif x in (9,10):								
#        final_color = '#5555FF'							
#    elif x in (11,12):								
#        final_color = '#6666FF'							
#    elif x in (13,14):								
#        final_color = '#7777FF'
#    elif x in (15,16):								
#        final_color = '#8888FF'							
#    elif x in (17,18):								
#        final_color = '#9999FF'							
#    elif x in (19,20):								
#        final_color = '#AAAAFF'							
#    elif x in (21,22):							
#        final_color = '#BBBBFF'							
#    elif x in (23,24):								
#        final_color = '#CCCCFF'							
#    elif x in (25,26):								
#        final_color = '#DDDDFF'							
#    elif x in (27,28):								
#        final_color = '#EEEEFF'						
#    else :									
#        final_color = '#FFFFFF'							
    return final_color
