from checkers_sem.gui.menu import Menu
from checkers_sem.gui.utils.loader import *
from checkers_sem.gui.constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_TITLE

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(MENU_TITLE)
        loader.load_images()

    def show(self):
        Menu(self.screen).show()
        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.show()
