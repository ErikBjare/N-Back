'''
You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.

Created on Feb 3, 2012

@author: Erik Bjareholt
'''

import pygame
from pygame.locals import *

try:
    import android
except ImportError:
    android = None
    
from nBack import NBack


class Main():
    def run(self):
        pygame.init()
    
        if android:
            self.androidInit()
            self.isAndroid = True
        else:
            self.isAndroid = False
            
        settings = Settings(self.isAndroid)
        nBack = NBack(settings)
        pygame.display.set_caption('N-Back V' + settings.version)
        nBack.run()
        
    def androidInit(self):
        android.init()
        android.map_key(android.KEYCODE_SEARCH, pygame.K_ESCAPE)
    
    
class Settings():
    version = "0.2.1"
    
    nBack = 3
    repeatProbability = 3
    slideTime = 500
    numOfSlides = 30
    drawNumber = True
    
    debug = False
    
    def __init__(self, android):
        if android:
            self.android = True
            self.windowSize = (800, 480)
        else:
            self.android = False
            self.windowSize = (800, 480)
    
    
if __name__ == "__main__" or __name__ == "main":
    main = Main()
    main.run()
