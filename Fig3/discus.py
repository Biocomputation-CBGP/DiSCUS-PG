# ----------------------------------------------------------------------------
# DiSCUS - main discus file
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


import random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import math

from Imports.parameters import *
from Imports.definitions import *
#from oscillator import *
from Imports.cell_class import *


def discus(screenview, screen, clock, cells, space, lines):
### Main function

    ### Initialisation of the experiment:
    pygame.init()
    running = True
    ### Two following lines can help avoid the 3D positioning (big colonies)
    #space._set_iterations(100)
    #space._set_collision_bias(pow(1.0 - 0.08, 10.0))
    
    bacs = cells
    springs = []

    ite = 0
    ### Main loop:
    while running:

        ite += 1
        screen.fill(THECOLORS["white"])

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        #########################################################################################
        ### Spring update. Update time of spring and remove it if time is out ###################
        springs_to_remove = []
        for spring in springs:
            o1 = spring[0].a; bac_o1 = look_bac(o1, bacs)
            o2 = spring[0].b; bac_o2 = look_bac(o2, bacs)
            centre_o1 = get_centres(bac_o1.shape.get_vertices())[1]
            centre_o2 = get_centres(bac_o2.shape.get_vertices())[1]
            centre_relative_o1 = pymunk.Vec2d((centre_o1[0] - bac_o1.shape.body.position.x), (centre_o1[1] - bac_o1.shape.body.position.y))
            centre_relative_o2 = pymunk.Vec2d((centre_o2[0] - bac_o2.shape.body.position.x), (centre_o2[1] - bac_o2.shape.body.position.y))
            spring[0].anchr1 = centre_relative_o1
            spring[0].anchr2 = centre_relative_o2
            spring[1] -= 1
            if spring[1] < 1:
                springs_to_remove.append(spring)
                bac_o1.conjugating = False
                bac_o2.conjugating = False
        for spring in springs_to_remove:
            space.remove(spring[0])
            springs.remove(spring)	

        #########################################################################################
        ### Division. loop that checks whether the cells must divide (if 2*length reached) or not
        new_generation = []
        for bac in bacs:
            if bac.plasmid==True: [x_new,y_new] = calculateOsc(bac.program[0],bac.program[1])
            elif bac.plasmid==False:[x_new,y_new] = [0,0]	
            if bac.program != None: (bac.program[0],bac.program[1]) = [x_new,y_new]    
            if bac.elongation[0]+bac.elongation[1] > length-1 and not(bac.conjugating):
                points = bac.shape.get_vertices()
                [centre1, centre2] = get_centres(points)
                points = [(4, -width), (1/4, -3*width/4), (0, -width/1000), (1/4, 3*width/4),\
                         (4, width), (length-4,width), (length-1/4,3*width/4), (length,-width/10000),\
                         (length-1/4, -3*width/4), (length-4, -width)]
                angle1 = math.radians(math.degrees(bac.shape.body.angle) + random.randint(-4,4))
                angle2 = math.radians(math.degrees(bac.shape.body.angle) + random.randint(-4,4))
                bac_shape1 = add_bac(space, centre1[0], centre1[1], angle1, points)
                bac_shape2 = add_bac(space, centre2[0], centre2[1], angle2, points)
                if bac.program != None:
                    b1 = bacteria(bac_shape1,[bac.program[0],bac.program[1]],[0,0],[bac_shape1.body.position.x,\
                         bac_shape1.body.position.y],bac.speed,bac.conjugating,bac.plasmid,bac.role,bac.partner+1)
                    b2 = bacteria(bac_shape2,[bac.program[0],bac.program[1]],[0,0],[bac_shape2.body.position.x,\
                         bac_shape2.body.position.y],bac.speed,bac.conjugating,bac.plasmid,bac.role,bac.partner+1)
                else:
                    b1 = bacteria(bac_shape1,None,[0,0],[bac_shape1.body.position.x,\
                         bac_shape1.body.position.y],bac.speed,bac.conjugating,bac.plasmid,bac.role,bac.partner+1)
                    b2 = bacteria(bac_shape2,None,[0,0],[bac_shape2.body.position.x,\
                         bac_shape2.body.position.y],bac.speed,bac.conjugating,bac.plasmid,bac.role,bac.partner+1)			
                new_generation.append(b1)
                new_generation.append(b2)
                space.remove(bac.shape, bac.shape.body)
            else:
                new_generation.append(bac)
        bacs = new_generation

        #########################################################################################
        ### Speed. Update de velocity of the cells (monitoring purposes) every minute ###########
        if ite%minute == 0:
            for bac in bacs:
                new_pos_x = bac.shape.body.position.x
                new_pos_y = bac.shape.body.position.y
                old_pos_x = bac.position[0]
                old_pos_y = bac.position[1]
                distance = math.sqrt( (new_pos_x - old_pos_x)**2 + (new_pos_y - old_pos_y)**2 )
                bac.position[0] = new_pos_x
                bac.position[1] = new_pos_y
                bac.distance = (distance/minute)		

        #########################################################################################
        ### Elongation. Called each growth_speed iterations #######################################
        bacs_grow = []
        if ite%growth_speed==0:
            for bac in bacs:

                bb = pymunk.BB(bac.shape.body.position.x-22,bac.shape.body.position.y-22,\
                               bac.shape.body.position.x+22,bac.shape.body.position.y+22)
                bac.role = len(space.bb_query(bb))

                query = space.shape_query(bac.shape)
                if len(query)<max_overlap:
                    r = random.randint(0,1)
                    if r == 0:
                        bac.elongation[0] += 1.
                    else:
                        bac.elongation[1] += 1.
                    centre_x = bac.shape.body.position.x
                    centre_y = bac.shape.body.position.y
                    old_angle = bac.shape.body.angle	
                    space.remove(bac.shape, bac.shape.body)
                    points = [(4-bac.elongation[0], -width), (1/4-bac.elongation[0], -3*width/4),\
                        (0-bac.elongation[0], -width/1000), (1/4-bac.elongation[0], 3*width/4),\
                        (4-bac.elongation[0], width), (length+bac.elongation[1]-4,width),\
                        (length+bac.elongation[1]-1/4,3*width/4), (length+bac.elongation[1], -width/1000),\
                        (length+bac.elongation[1]-1/4,-3*width/4), (length+bac.elongation[1]-4,-width)]
                    bac_shape = add_bac(space, centre_x, centre_y, old_angle, points)
                    b = bacteria(bac_shape,bac.program,bac.elongation, [bac_shape.body.position.x,\
                        bac_shape.body.position.y], bac.speed, bac.conjugating, bac.plasmid, bac.role, bac.partner)
                    bacs_grow.append(b)

                    if bac.conjugating:
                        for spring in springs:
                            if (spring[0].a == bac.shape.body) or (spring[0].b == bac.shape.body):
                                if spring[0].a == bac.shape.body:
                                    o1 = bac_shape.body; o2 = spring[0].b
                                else: 
                                    o1 = spring[0].a; o2 = bac_shape.body
                                an1 = spring[0].anchr1
                                an2 = spring[0].anchr2
                                space.remove(spring[0])
                                rest_length = spring_rest_length
                                newspring = pymunk.DampedSpring(o1, o2, an1, an2, rest_length, 10, 100)
                                newspring.bias_coef = spring_bias_coeficient
                                springs.append([newspring, spring[1]])
                                space.add(newspring)
                                springs.remove(spring)
                                break			
                else:
                    bacs_grow.append(bac)
            bacs = bacs_grow

        #########################################################################################
        ### Conjugation #########################################################################
        for bac in bacs:
            if not(bac.conjugating) and bac.plasmid and (bac.elongation[0]+bac.elongation[1]>cell_infancy*length):
                query = space.shape_query(bac.shape)
                if bac.role == 0: r = random.randint(0,1/p_d)
                elif bac.role == 2 and bac.partner == 0: r = random.randint(0,1/p_t1)
                elif bac.role == 2 and bac.partner == 2: r = random.randint(0,1/p_t2)
                r_signal = random.randint(0,1/p_t2)
                if r == r_signal and len(query)>0: 
                    mate_shape = random.choice(query)
                    mate = look_mate(mate_shape, bacs)
                    if (mate!=None) and not(mate.conjugating) and not(mate.plasmid):
                        o1 = bac; o2 = mate
                        centre_o1 = get_centres(o1.shape.get_vertices())[1]
                        centre_o2 = get_centres(o2.shape.get_vertices())[1]
                        rest_length = spring_rest_length
                        centre_relative_o1 = pymunk.Vec2d((centre_o1[0] - o1.shape.body.position.x), (centre_o1[1] - o1.shape.body.position.y))
                        centre_relative_o2 = pymunk.Vec2d((centre_o2[0] - o2.shape.body.position.x), (centre_o2[1] - o2.shape.body.position.y))
                        newspring = pymunk.DampedSpring(o1.shape.body, o2.shape.body, centre_relative_o1, centre_relative_o2, rest_length, spring_stiffness, spring_damping)
                        newspring.bias_coef = spring_bias_coeficient
                        springs.append([newspring,c_time])
                        space.add(newspring)
                        bac.conjugating = True; mate.conjugating = True
                        mate.plasmid = True; mate.role = 2; mate.partner = bac.role


        #########################################################################################
        ### Remove cells that are outside the screen (and draw the ones inside) #################
        max_partner = max([b.partner for b in bacs]) # generation from start (=partner; start 0)
        min_partner = min([b.partner for b in bacs]) # generation from start (=partner; start 0)
        max_role = max([b.role for b in bacs]) # role = bb query 
        min_role = min([b.role for b in bacs])
        bacs_to_remove = []
        for bac in bacs:
        ### loop to identify the cells outside the screenview
            if ((bac.shape.body.position.y < 10 or bac.shape.body.position.y > screenview-10) or (bac.shape.body.position.x < 10 or bac.shape.body.position.x > screenview-10)) and (not(bac.conjugating)):
                bacs_to_remove.append(bac)
            ## Next two lines can be used to calculate gravity if needed.
            #g = calculateGravity(bac[0].body.position.x, bac[0].body.position.y)
            #bac[0].body.update_velocity(bac[0].body,g,0.9,0.9)
            #draw_bac2(screen, bac, bac.role, min_role, max_role-min_role)
            draw_bac(screen, bac, bac.partner, min_partner, max_partner-min_partner) # Live video. Comment this line if video not wanted
        if lines != None: draw_lines(screen, lines) 
        for bac in bacs_to_remove:
            space.remove(bac.shape, bac.shape.body) 
            bacs.remove(bac)

        #########################################################################################
        ### Draw the springs ####################################################################
        for spring in springs:
            pv1 = spring[0].a.position + spring[0].anchr1
            pv2 = spring[0].b.position + spring[0].anchr2
            pygame.draw.line(screen, [0, 255, 0], pv1, pv2, 3)

	if ite%50 == 0:
            f = open('file'+str(ite)+'.txt', 'w')
            #pygame.image.save(screen, 'pics5/pic' + str(ite) + '.png')
            xlist = []
            ylist = []
            zagelist = [] # age due to generations
            zdenlist = [] # density of its bb area
            for bac in bacs:
                xlist.append(bac.shape.body.position.x)
                ylist.append(bac.shape.body.position.y)
                zagelist.append(bac.partner)
                zdenlist.append(bac.role)
            f.write(str(xlist) + '\n')
            f.write(str(ylist) + '\n')
            f.write(str(zagelist) + '\n')
            f.write(str(zdenlist) + '\n')
            f.close()
            



        space.step(pymunk_steps)
        pygame.display.flip()
        clock.tick(pymunk_clock_ticks)

