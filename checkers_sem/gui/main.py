from checkers_sem.gui.menu import *
from checkers_sem.gui.game_window import *

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(MENU_TITLE)

    def show(self):
        Menu(self.screen).show()
        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.show()
