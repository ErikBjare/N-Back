'''
You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.

Created on Feb 3, 2012

@author: Erik Bjareholt
'''

import sys

import pygame
from pygame.locals import *

import UI

try:
    import android
except ImportError:
    android = None
    

class NBack:
    def __init__(self, settings):
        self.clock = pygame.time.Clock()
        
        #Game settings
        self.settings = settings
        self.nBack = 2
    
    def run(self):
        self.screen = pygame.display.set_mode(self.settings.windowSize,0,32)
        
        self.drawMenu = True
        self.drawGame = False
        self.drawResults = False

        self.menu = UI.activities.Menu(self.settings.windowSize, self.settings.android, self.settings.version)
        self.game = UI.activities.Game(self.settings.windowSize, self.settings.android)
        
        while True:
            self.handler()
            self.draw()
            pygame.display.flip()
            
            if android:
                if android.check_pause():
                    android.wait_for_resume()
            
    def draw(self):
        if self.drawMenu:
            self.screen.blit(self.menu.draw(), (0,0))
            
        if self.drawGame:
            self.screen.blit(self.game.draw(), (0,0))    
            
        if self.drawResults:
            self.screen.blit(self.results.draw(), (0,0))
    
    def handler(self):
        pygame.event.pump()
        
        #keys = pygame.key.get_pressed()
        #if keys[K_w]: 
        #    print("W pressed")
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.game.identified = True
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pass
                elif event.key == K_SPACE:
                    self.game.identified = True
                elif event.key == K_ESCAPE:
                    self.drawMenu = False
                    self.drawGame = True
                    self.game.start(self.settings)
                elif event.key == K_F1:
                    if self.drawResults:
                        self.drawResults = False
                    else:
                        self.results = UI.activities.Results(self.settings.windowSize, self.settings.android, self.game.getResults())
                        self.drawResults = True
            elif event.type == USEREVENT+1:
                self.game.showSlideSwitch()
