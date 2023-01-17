# ----------------------------------------------------------------------------
# DiSCUS - parameters file
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


max_overlap = 4			### Value above which the cell stops growing till the pressure decreases
width = 5				### Half cell width
length = 8				### Initial cell length
growth_speed = 10			### Iterations between elongation processes (time to resolve forces, define bigger for big simulations)
Gt = length * growth_speed 		### Generation time of the simulation in Iterations
real_Gt = 100 				### Real generation time in Minutes
minute = float(Gt)/float(real_Gt) 	### Iterations per minute
p_d = 0.001 				### Probability of conjugation event in donors
p_t1 = 0.02 				### Probability of conjugation event in transconjugant (converted from donor)
p_t2 = 0.05 				### Probability of conjugation event in transconjugant (converted from trans)
c_time = 10 				### Conjugation time in iterations
network_steps = 18 			### Number of steps of the ODEs per Gt
i_time = float(network_steps)/float(Gt) ### Number of integration steps in each call to the program
number_recipients = 20			### Initial number of recipients
number_donors = 20			### Initial number of donors
spring_bias_coeficient = 10		### Spring bias coeficient
spring_rest_length = 10			### Spring rest length
spring_stiffness = 10			### Spring stiffness
spring_damping = 100			### Spring damping
cell_infancy = 0.20			### (Percentage) Time in which the cell is too young to conjugate
pymunk_steps = 1/5.0			### Pymunk steps.
pymunk_clock_ticks = 1500.0		### Pymunk clock ticks.
bac_mass = 1.     			### Cell's mass
bac_friction = 4			### Cell's friction




