import pygame

from checkers_sem.constants import *
from checkers_sem.gui.menu import *
from checkers_sem.gui.game_window import *
from checkers_sem.genetic.player import Player

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(MENU_TITLE)

    def show(self):
        option = Menu(self.screen).show()

        match option:
            case GameType.HUMAN_VS_HUMAN:
                pass
            case GameType.HUMAN_VS_PC:
                pass
            case GameType.PC_VS_PC:
                game = GameWindow(self.screen, (Player([3.6, 10.6, 4.4, 2.7, 5.2, 3.2]),
                                                       Player([5.5, 6, 4, 5.4, 6.4, 3.2])) )
            case _:
                pygame.quit()
                return

        game.play()
        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.show()
