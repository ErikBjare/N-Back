"""
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Created on Feb 3, 2012

@author: Erik Bjareholt
"""

import sys

import pygame
from pygame.locals import *

import UI
from settings import Settings

try:
    import android
except ImportError:
    android = None
    

class NBack:
    def __init__(self):
        self.clock = pygame.time.Clock()
        
        self.settings = Settings.Instance()

        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode(self.settings.windowSize, pygame.FULLSCREEN, 32)
        else:
            self.screen = pygame.display.set_mode(self.settings.windowSize, 0, 32)

        self.drawMenu = True if not self.settings.standalone else False
        self.drawGame = False if not self.settings.standalone else True
        self.drawResults = False

        self.menu = UI.activities.Menu()
        self.game = UI.activities.Game()

    def run(self):
        if self.settings.standalone:
            self.game.start()

        while True:
            self.handler()
            self.draw()
            pygame.display.flip()
            
            if android:
                if android.check_pause():
                    android.wait_for_resume()
            
    def draw(self):
        if self.drawMenu:
            self.screen.blit(self.menu.draw(), (0, 0))
            
        if self.drawGame:
            self.screen.blit(self.game.draw(), (0, 0))
            
        if self.drawResults:
            self.screen.blit(self.results.draw(), (0, 0))
    
    def handler(self):
        pygame.event.pump()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.game.triggered = True

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pass

                elif event.key == K_SPACE:
                    self.game.trigger()

                elif not self.settings.standalone:
                    if event.key == K_ESCAPE:
                        self.drawMenu = False
                        self.drawGame = True
                        self.game.start()
                    elif event.key == K_F1:
                        self.drawResults = not self.drawResults
                        if self.drawResults:
                            self.results = UI.activities.Results(self.game.results)

            elif event.type == USEREVENT+1:
                self.game.showSlideSwitch()
