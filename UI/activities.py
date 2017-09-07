"""
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Created on Mar 11, 2012

@author: Erik Bjareholt
"""

import random

import pygame
from pygame.locals import *
from settings import Settings

from . import widgets


class Activity:
    def __init__(self):
        settings = Settings.Instance()
        self.surface = pygame.Surface(settings.windowSize).convert()
        self.windowSize = settings.windowSize
        self.android = settings.android


class Menu(Activity):
    def __init__(self):
        Activity.__init__(self)
        self.version = Settings.Instance().version

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
        self.title.blit(titleText, (self.title.get_width()/2-titleText.get_width()/2, self.title.get_height()/2-titleText.get_height()/2))
        self.title.blit(titleVersion, (self.title.get_width()/2-titleVersion.get_width()/2, (self.title.get_height()/2-titleVersion.get_height()/2)+40))

        self.controlsBox = widgets.TextBox("Controls\n  New Game - {0}\n  Trigger N-Back - {1}".format(newgameKey, triggerKey), self.menuFont, (270,100), color=(0,0,50), textColor=(255,255,0), radius=10)

    def draw(self):
        self.surface.blit(self.title, ( (self.surface.get_width()/2-self.title.get_width()/2), (self.surface.get_height()/2-self.title.get_height()/2)-100 ))
        #self.surface.blit(self.controls, ( 25, (self.windowSize[1]-self.controls.get_height())-25 ))
        self.surface.blit(self.controlsBox.draw(), ( 25, (self.windowSize[1]-self.controlsBox.draw().get_height())-25 ))

        return self.surface


class Game(Activity):
    corner_radius = 10

    board_surface_size = (300+corner_radius*2, 300+corner_radius*2)
    board_surface_color = (200, 200, 200)
    cell_surface_size = (100, 100)
    cell_surface_color = (50, 50, 50)
    background_color = (255, 255, 255)

    def __init__(self):
        Activity.__init__(self)
        self.settings = Settings.Instance()

        self.results = {}
        self.history = []
        self.reset()

        self.positions = {i+1: (self.corner_radius + 100*(i % 3),
                                self.corner_radius + 100*(int(i/3)))
                          for i in range(9)}

        self.normalFont = pygame.font.Font("fonts/freesansbold.ttf", 20)
        self.smallFont = pygame.font.Font("fonts/freesansbold.ttf", 15)
        self.cellFont = pygame.font.Font("fonts/freesansbold.ttf", 70)

        self.show_answer = False
        self.triggered = False

    def draw(self):
        self.surface.fill(self.background_color)

        board_surface_base = widgets.Box(self.board_surface_size, self.board_surface_color, self.corner_radius).draw()
        board_surface = pygame.Surface.copy(board_surface_base)

        if not self.show_answer or not self.early_slide():
            cell_surface_base = widgets.Box(self.cell_surface_size, self.cell_surface_color, self.corner_radius).draw()
            cell_surface = pygame.Surface.copy(cell_surface_base)

            if self.settings.drawNumber:
                cell_number = self.cellFont.render(str(self.history[-1]), True, (255, 255, 255))
                cell_surface.blit(cell_number, (50-cell_number.get_width()/2, 50-cell_number.get_height()/2))
            board_surface.blit(cell_surface, (self.positionX, self.positionY, 100, 100))

        self.surface.blit(board_surface, ((self.windowSize[0]-board_surface.get_width())/2,
                                          (self.windowSize[1]-board_surface.get_height())/2))

        return self.surface

    def reset(self):
        self.results = {"correct": 0, "avoid": 0, "miss": 0, "wrong": 0}
        self.history = []

    def start(self):
        self.reset()
        self.nextSlide()

        pygame.time.set_timer(USEREVENT+1, int(self.settings.slideTime))

    def pause(self):
        if self.activeGame:
            pygame.time.set_timer(USEREVENT+1, 0)
        else:
            pygame.time.set_timer(USEREVENT+1, self.slideTime)
        self.activeGame = not self.activeGame
        self.drawMenu = not self.drawMenu

    def stop(self):
        self.save()
        print("Correct: {correct}\nWrong: {wrong}\nAvoided: {avoid}\nMissed: {miss}".format(**self.results))
        pygame.time.set_timer(USEREVENT+1, 0)
        pygame.time.set_timer(QUIT, self.settings.slideTime)

    def save(self):
        """Saves result to CSV"""
        print("Saving results to CSV...")
        with open("./output.csv", "w+") as f:
            f.read()
            write_data = "\n{correct},{wrong},{avoid},{miss}".format(**self.results)
            f.write(write_data)

    def setNoAnswer(self):
        self.cell_surface_color = (50, 50, 50)

    def setCorrectAnswer(self):
        self.cell_surface_color = (25, 200, 25)

    def setWrongAnswer(self):
        self.cell_surface_color = (200, 25, 25)

    def early_slide(self):
        return len(self.history) < 1+self.settings.nBack

    def trigger(self):
        if self.early_slide():
            print("Too early!")
            return

        if not self.triggered:
            self.triggered = True
            self.checkAnswer()
        else:
            print("Already triggered")

    def checkAnswer(self):
        if self.early_slide():
            return

        nBackPos = self.history[-(1+self.settings.nBack)]
        pos = self.currentPosition()

        if self.triggered:
            if nBackPos == pos:
                self.results["correct"] += 1
                self.setCorrectAnswer()
                print("Correct, {0} is equal to {1} with nBack={2}.".format(nBackPos, pos, self.settings.nBack))
            elif nBackPos != pos:
                self.results["wrong"] += 1
                self.setWrongAnswer()
                print("Wrong, {0} is not equal to {1} with nBack={2}.".format(nBackPos, pos, self.settings.nBack))
        else:
            if nBackPos != pos:
                self.results["avoid"] += 1
                self.setCorrectAnswer()
                print("Avoided it, {0} is not equal to {1} with nBack={2}.".format(nBackPos, pos, self.settings.nBack))
            elif nBackPos == pos:
                self.results["miss"] += 1
                self.setWrongAnswer()
                print("Missed it, {0} is equal to {1} with nBack={2}.".format(nBackPos, pos, self.settings.nBack))

    def nextSlide(self):
        if random.random() < self.settings.repeatProbability and not self.early_slide():
            '''This needs to be remade so that any of the last (self.nBack) numbers could be the next one.'''
            position = self.history[random.randint(-(1+self.settings.nBack), -1)]
        else:
            position = random.randint(1, 9)
        self.history.append(position)

        if self.settings.debug:
            print("Slide number {0} generated with value: {1}".format(len(self.history), self.history[-1]))

        self.triggered = False
        self.positionX = self.positions[self.currentPosition()][0]
        self.positionY = self.positions[self.currentPosition()][1]

    def currentPosition(self):
        return self.history[-1]

    def showSlideSwitch(self):
        self.show_answer = not self.show_answer

        if not self.show_answer:
            self.setNoAnswer()
            pygame.time.set_timer(USEREVENT+1, self.settings.slideTime)
            self.nextSlide()
        else:
            self.checkAnswer()
            pygame.time.set_timer(USEREVENT+1, int(self.settings.slideTime/3))
            if len(self.history) >= self.settings.numOfSlides:
                # If enough slides have passed
                self.stop()

class Results(Activity):
    def __init__(self, results):
        Activity.__init__(self)

        self.surface.convert_alpha()
        #self.surface.fill((255,255,255,100))

        self.normalFont = pygame.font.Font("fonts/freesansbold.ttf", 20)
        self.smallFont = pygame.font.Font("fonts/freesansbold.ttf", 15)

        self.panelSurfaceBase = pygame.Surface((150, self.windowSize[1]))
        self.panelSurfaceBase.fill((50, 50, 50))

        self.panelSurfaceLeft = pygame.Surface.copy(self.panelSurfaceBase)
        self.panelSurfaceRight = pygame.Surface.copy(self.panelSurfaceBase)

        self.panelSurfaceLeft = pygame.Surface.copy(self.panelSurfaceBase)
        self.panelSurfaceRight = pygame.Surface.copy(self.panelSurfaceBase)

        resultsHeader = self.normalFont.render("Results", True, (255, 255, 0))
        resultsCorrect = self.smallFont.render("Correct: {0}".format(results["correct"]), True, (255, 255, 0))
        resultsWrong = self.smallFont.render("Wrong: {0}".format(results["wrong"]), True, (255, 255, 0))
        resultsAvoid = self.smallFont.render("Avoided: {0}".format(results["avoid"]), True, (255, 255, 0))
        resultsMiss = self.smallFont.render("Missed: {0}".format(results["miss"]), True, (255, 255, 0))
        self.panelSurfaceRight.blit(resultsHeader, (10, 10))
        self.panelSurfaceRight.blit(resultsCorrect, (10, 40))
        self.panelSurfaceRight.blit(resultsWrong, (10, 60))
        self.panelSurfaceRight.blit(resultsAvoid, (10, 80))
        self.panelSurfaceRight.blit(resultsMiss, (10, 100))

        self.surface.blit(self.panelSurfaceLeft, (0, 0))
        self.surface.blit(self.panelSurfaceRight, ((self.windowSize[0]-self.panelSurfaceRight.get_width()), 0))

    def draw(self):
        return self.surface
