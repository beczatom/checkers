from checkers_sem.gui.menu import *
from checkers_sem.gui.game_window import *
from checkers_sem.player.player import AIPlayer, HumanPlayer

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(MENU_TITLE)

    def show(self):
        option = Menu(self.screen).show()

        match option:
            case GameType.HUMAN_VS_HUMAN:
                game = GameWindow(self.screen, (HumanPlayer(), HumanPlayer()))
            case GameType.HUMAN_VS_PC:
                game = GameWindow(self.screen, (HumanPlayer(), AIPlayer()))

            case GameType.PC_VS_PC:
                game = GameWindow(self.screen, (AIPlayer(), AIPlayer()))
            case _:
                pygame.quit()
                return

        game.play()
        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.show()
