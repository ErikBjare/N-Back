"""
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Created on Feb 3, 2012

@author: Erik Bjareholt
"""

import pygame

try:
    import android
except ImportError:
    android = None

from settings import Settings

from nBack import NBack


def main():
    settings = Settings.Instance()

    pygame.init()
    if settings.android:
        settings.android = True
        android.init()
        android.map_key(android.KEYCODE_SEARCH, pygame.K_ESCAPE)

    nback = NBack()
    pygame.display.set_caption('N-Back v' + settings.version)
    nback.run()


if __name__ == "__main__" or __name__ == "main":
    main()
