# ----------------------------------------------------------------------------
# DiSCUS-PG
# Angel Goni-Moreno 
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



from Imports.definitions import *
from Imports.cell_class import *
from discus2 import *


def add_walls(space):
### Fuction used to place the walls in the world (walls scaled depending on screenview)
### In: the space
### Out: returns the shapes (l) of the walls
    body = pymunk.Body()
    body.static = True
    body.position = (0,0.2*screenview)    
    l1 = pymunk.Segment(body, (0, 0), (screenview,0), 5.0)
    body = pymunk.Body()
    body.position = (0,0.201*screenview)    
    l2 = pymunk.Segment(body, (0, 0), (screenview,0), 5.0)

    space.add(l1,l2)
    return l1,l2

screenview = 2000			### Scren size
screen = pygame.display.set_mode((screenview, screenview/4))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0.0, 10.0)
space.collision_slop = 1
space.collision_bias = 0
bacs = []
walls = add_walls(space)

for line in walls:
    line.elasticity = 0.0
    line.friction = 0


### Loop for the placement of recipients in the world
### considering the longitudinal shape defined by the definition add_walls
for i in range(1): # Placing initial cells in the world
    points = [(-length, -width), (-length, width), (length,width), (length, -width)]
    r_x = screenview/2
    r_y = 0.1*screenview
    r_angle = 0
    bac_shape = add_bac(space,r_x,r_y, 0, points)
    b = bacteria(bac_shape,[0,0],[0,0],[bac_shape.body.position.x, bac_shape.body.position.y], 0, False, False,1,0)
    bacs.append(b)



def main():
    discus(screenview, screen, clock, bacs, space, walls)
if __name__ == '__main__':  
    main()
