# ----------------------------------------------------------------------------
# DiSCUS - class file
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

class bacteria:
    def __init__(self, shape, program, elongation, position, speed, conjugating, plasmid, role, partner):
        self.shape = shape             # Shape of the cell
        self.program = program         # Molecular network defined
        self.elongation = elongation   # Longitudinal size of the cell
        self.position = position       # Position of the cell in the world
        self.speed = speed             # Velocity of the cell
        self.conjugating = conjugating # Boolean. Is the cell conjugating?
        self.plasmid = plasmid         # Boolean. Has the cell the plasmid?
        self.role = role	       # Donor, recipient or transconjugant
        self.partner = partner         # The role of its previous partner (GENERATION IN 2Dfront)
