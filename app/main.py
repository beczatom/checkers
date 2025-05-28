"""
This module contains the main function, initializes pygame and runs menu
"""

import pygame

from app.gui.menu import Menu
from app.gui.utils.loader import loader
from app.gui.constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_TITLE, MENU_IMAGE

class Main:
    """
    This class initializes pygame and runs menu
    """

    def __init__(self):
        """
        Initializes pygame and loads images
        """
        pygame.init()   # pylint: disable=no-member
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(MENU_TITLE)
        loader.load_images()
        pygame.display.set_icon(loader.LOADED_IMAGES[MENU_IMAGE])

    def show(self) -> None:
        """
        Shows menu, as the class responsible for all windows.
        When quit was hit, the Menu.show ends, and we quit pygame and the whole program.
        """
        Menu(self.screen).show()
        pygame.quit()   # pylint: disable=no-member

    def useless(self) -> None:
        """
        Absolutely useless, because can be directly accessed,
        but pylint wouldn't survive if there wasn't two public methods.
        """
        print('I\'m useless')


if __name__ == '__main__':
    main = Main()
    main.show()
