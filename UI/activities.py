'''
You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.

Created on Mar 11, 2012

@author: Erik Bjareholt
'''

import random

import pygame
from pygame.locals import *

import widgets

class Activity:
    def __init__(self, windowSize, android):
        self.surface = pygame.Surface(windowSize).convert()
        self.windowSize = windowSize
        self.android = android
        
        
class Menu(Activity):
    def __init__(self, windowSize, android, version):
        Activity.__init__(self, windowSize, android)
        self.version = version
        
        self.titleFont = pygame.font.Font("fonts/freesansbold.ttf", 50)
        self.menuFont = pygame.font.Font("fonts/freesansbold.ttf", 20)
        self.smallFont = pygame.font.Font("fonts/freesansbold.ttf", 15)
        
        if self.android:
            newgameKey = "Search"
            triggerKey = "Touch"
        else:
            newgameKey = "Escape"
            triggerKey = "Space"
        
        titleText = self.titleFont.render("Welcome to N-Back!", True, (255,255,0))
        titleVersion = self.smallFont.render("Version " + self.version, True, (255,255,0))
        self.title = pygame.Surface((650,200)).convert()
        self.title.blit(titleText, ( (self.title.get_width()/2-titleText.get_width()/2), (self.title.get_height()/2-titleText.get_height()/2) ))
        self.title.blit(titleVersion, ( (self.title.get_width()/2-titleVersion.get_width()/2), (self.title.get_height()/2-titleVersion.get_height()/2)+40 ))
        
        self.controlsBox = widgets.TextBox("Controls\n  New Game - {0}\n  Trigger N-Back - {1}".format(newgameKey, triggerKey), self.menuFont, (270,100), color=(0,0,50), textColor=(255,255,0), radius=10)
        
    def draw(self):
        self.surface.blit(self.title, ( (self.surface.get_width()/2-self.title.get_width()/2), (self.surface.get_height()/2-self.title.get_height()/2)-100 ))
        #self.surface.blit(self.controls, ( 25, (self.windowSize[1]-self.controls.get_height())-25 ))
        self.surface.blit(self.controlsBox.draw(), ( 25, (self.windowSize[1]-self.controlsBox.draw().get_height())-25 ))
        
        return self.surface
    
    
class Game(Activity):
    cornerRadius = 10
    
    boardSurfaceSize = (300+cornerRadius*2, 300+cornerRadius*2)
    boardSurfaceColor = (200, 200, 200)
    cellSurfaceSize = (100, 100)
    cellSurfaceColor = (50, 50, 150)
    
    positions = {1:(0+cornerRadius, 0+cornerRadius),   2:(100+cornerRadius, 0+cornerRadius),   3:(200+cornerRadius, 0+cornerRadius), 
                 4:(0+cornerRadius, 100+cornerRadius), 5:(100+cornerRadius, 100+cornerRadius), 6:(200+cornerRadius, 100+cornerRadius),
                 7:(0+cornerRadius, 200+cornerRadius), 8:(100+cornerRadius, 200+cornerRadius), 9:(200+cornerRadius, 200+cornerRadius)}
    
    def __init__(self, windowSize, android):
        Activity.__init__(self, windowSize, android)
        
        self.normalFont = pygame.font.Font("fonts/freesansbold.ttf", 20)
        self.smallFont = pygame.font.Font("fonts/freesansbold.ttf", 15)
        self.cellFont = pygame.font.Font("fonts/freesansbold.ttf", 70)
        
        self.showSlide = False
        self.identified = False
        
        self.boardSurfaceBase = widgets.Box(self.boardSurfaceSize, self.boardSurfaceColor, self.cornerRadius).draw()
        self.cellSurfaceBase = widgets.Box(self.cellSurfaceSize, self.cellSurfaceColor, self.cornerRadius).draw()
        
    def draw(self):
        self.surface.fill((255,255,255))
        self.boardSurface = pygame.Surface.copy(self.boardSurfaceBase)
        self.cellSurface = pygame.Surface.copy(self.cellSurfaceBase)
        
        if self.showSlide:
            if self.settings.drawNumber:
                cellNumber = self.cellFont.render(str(self.history[-1]), True, (255,255,0))
                self.cellSurface.blit(cellNumber, (50-cellNumber.get_width()/2,50-cellNumber.get_height()/2))
            self.boardSurface.blit(self.cellSurface, (self.positionX, self.positionY, 100, 100))
        
        self.surface.blit(self.boardSurface, ((self.windowSize[0]-self.boardSurface.get_width())/2, (self.windowSize[1]-self.boardSurface.get_height())/2))
        
        return self.surface
        
    def start(self, settings):
        self.settings = settings
        
        self.results = [0,0,0,0] # Correct, Avoid, Miss, Wrong
        
        self.history = []
        self.nextSlide()
        
        pygame.time.set_timer(USEREVENT+1, self.settings.slideTime)
        
    def pause(self):
        if self.activeGame:
            pygame.time.set_timer(USEREVENT+1, 0)
        else:
            pygame.time.set_timer(USEREVENT+1, self.slideTime)
        self.activeGame = not self.activeGame
        self.drawMenu = not self.drawMenu
        
    def stop(self):
        print("Correct: {0}\nWrong: {1}\nAvoided: {2}\nMissed: {3}".format(self.results[0], self.results[3], self.results[1], self.results[2]))
        pygame.time.set_timer(USEREVENT+1, 0)
    
    def nextSlide(self):
        if self.settings.debug and len(self.history) >= self.settings.nBack+1:
            if self.identified and self.history[-(1+self.settings.nBack)] == self.history[-1]:
                self.results[0] += 1
                print("Correct, {0} is equal to {1} with nBack={2}.".format(self.history[-(1+self.settings.nBack)], self.history[-1], self.settings.nBack))
            elif self.identified and self.history[-(1+self.settings.nBack)] != self.history[-1]:
                self.results[3]
                print("Wrong, {0} is not equal to {1} with nBack={2}.".format(self.history[-(1+self.settings.nBack)], self.history[-1], self.settings.nBack))
            elif self.history[-(1+self.settings.nBack)] != self.history[-1]:
                self.results[1] += 1
                print("Avoided it, {0} is not equal to {1} with nBack={2}.".format(self.history[-(1+self.settings.nBack)], self.history[-1], self.settings.nBack))
            elif self.history[-(1+self.settings.nBack)] == self.history[-1]:
                print("Missed it, {0} is equal to {1} with nBack={2}.".format(self.history[-(1+self.settings.nBack)], self.history[-1], self.settings.nBack))
                self.results[2] += 1
                
        if random.randint(1,self.settings.repeatProbability) == 1 and len(self.history) > 1:
            '''This needs to be remade so that any of the last (self.nBack) numbers could be the next one.'''
            self.history.append(self.history[-1])
        else: 
            self.position = random.randint(1,9)
            self.history.append(self.position)
        if self.settings.debug:
            print("Slide number {0} generated with value: {1}".format(len(self.history), self.history[-1]))
        self.identified = False
        self.positionX = self.positions[self.position][0]
        self.positionY = self.positions[self.position][1]
        
        if len(self.history) < self.settings.numOfSlides:
            pass
        else:
            self.stop()
            
            
    def showSlideSwitch(self):
        self.showSlide = not self.showSlide
        if self.showSlide == True:
                self.nextSlide()
                   
    def getResults(self):
        return self.results

class Results(Activity):
    def __init__(self, windowSize, android, results):
        Activity.__init__(self, windowSize, android)
        
        self.surface.convert_alpha()
        #self.surface.fill((255,255,255,100))
        
        self.normalFont = pygame.font.Font("fonts/freesansbold.ttf", 20)
        self.smallFont = pygame.font.Font("fonts/freesansbold.ttf", 15)
        
        self.panelSurfaceBase = pygame.Surface((150,self.windowSize[1]))
        self.panelSurfaceBase.fill((50,50,50))
        
        self.panelSurfaceLeft = pygame.Surface.copy(self.panelSurfaceBase)
        self.panelSurfaceRight = pygame.Surface.copy(self.panelSurfaceBase)
        
        self.panelSurfaceLeft = pygame.Surface.copy(self.panelSurfaceBase)
        self.panelSurfaceRight = pygame.Surface.copy(self.panelSurfaceBase)
        
        resultsHeader = self.normalFont.render("Results", True, (255,255,0))
        resultsCorrect = self.smallFont.render("Correct: {0}".format(results[0]), True, (255,255,0))
        resultsWrong = self.smallFont.render("Wrong: {0}".format(results[3]), True, (255,255,0))
        resultsAvoid = self.smallFont.render("Avoided: {0}".format(results[1]), True, (255,255,0))
        resultsMiss = self.smallFont.render("Missed: {0}".format(results[2]), True, (255,255,0))
        self.panelSurfaceRight.blit(resultsHeader, (10,10))
        self.panelSurfaceRight.blit(resultsCorrect, (10,40))
        self.panelSurfaceRight.blit(resultsWrong, (10,60))
        self.panelSurfaceRight.blit(resultsAvoid, (10,80))
        self.panelSurfaceRight.blit(resultsMiss, (10,100))
        
        self.surface.blit(self.panelSurfaceLeft, (0, 0))
        self.surface.blit(self.panelSurfaceRight, ((self.windowSize[0]-self.panelSurfaceRight.get_width()), 0))
        
    def draw(self):
        return self.surface
