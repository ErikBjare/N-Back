"""
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Created on Mar 11, 2012

@author: Erik Bjareholt
"""

import pygame.surface
import pygame.draw

class Widget:
    def __init__(self, size):
        self.size = size
        self.surface = pygame.Surface(self.size).convert_alpha()
        self.surface.fill((0,0,0,0))
    
    
class Box(Widget):
    def __init__(self, size, color, radius=0):
        Widget.__init__(self, size)
        self.color = color
        self.radius = radius
        
        if self.radius != 0:
            '''Rounded corners code goes here'''
            corners = [[0+self.radius, 0+self.radius], 
                       [self.size[0]-self.radius, 0+self.radius], 
                       [0+self.radius, self.size[1]-self.radius], 
                       [self.size[0]-self.radius, self.size[1]-self.radius]]
            for quadrant in range(4):
                pygame.draw.circle(self.surface, self.color, corners[quadrant], self.radius)
            pygame.draw.rect(self.surface, self.color, (0, self.radius, self.size[0], self.size[1]-self.radius*2))
            pygame.draw.rect(self.surface, self.color, (self.radius, 0, self.size[0]-self.radius*2, self.size[1]))
        else:
            pygame.draw.rect(self.surface, self.color, (self.radius, 0, self.size[0]-self.radius*2, self.size[1]))
            
    def draw(self):
        return self.surface
    
    
class TextBox(Box):
    ''' 
        Needs a LOT of refurbishing, I made this code quick N' dirty just as a test.
        If use is planned, a bit of work should be dedicated to make this code better
        and complete
    '''
    def __init__(self, text, font, size, color=(255,255,255), textColor=(50,50,50), margin=0, radius=0):
        text = text.splitlines()
        textSurface = pygame.Surface((size[0]-radius*2, size[1]-radius*2)).convert()
        textSurface.fill(color)
        lineNum = 0
        for line in text:
            textSurface.blit(font.render(line, True, textColor), (0, lineNum*font.get_height()*1.25))
            lineNum += 1
            
        Box.__init__(self, size, color, radius)
        
        self.surface.blit(textSurface, (margin+radius, margin+radius))
            
    def draw(self):
        return self.surface
