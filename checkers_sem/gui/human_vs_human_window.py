from checkers_sem.gui.game_window import *
from checkers_sem.constants import *
from checkers_sem.player.player import HumanPlayer

class HumanVsHumanWindow(GameWindow):
    def __init__(self, surface: pygame.surface, players: tuple[HumanPlayer, HumanPlayer]):
        super().__init__(surface, players)
        self.move_thread = None
        self.run = True

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.move_table.handle_event(event)
            self.chessboard.handle_event(event)
            for button in self.game_control_buttons:
                button.handle_event(event)

    def show(self):

        self.chessboard.draw()
        pygame.display.update()

        while self.run:
            pygame.time.delay(10)
            for event in pygame.event.get():
                self.handle_event(event)

            self.make_move()
            self.white_timer.draw()
            self.black_timer.draw()
            pygame.display.update()