from checkers_sem.gui.game_window import *
from checkers_sem.constants import *
from checkers_sem.player.player import HumanPlayer

class HumanVsHumanWindow(GameWindow):
    def __init__(self, surface: pygame.surface, players: tuple[HumanPlayer, HumanPlayer]):
        super().__init__(surface, players)
        self.run = True
        self.chessboard.draw()

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.move_table.handle_event(event)
            self.chessboard.handle_event(event)
            for button in self.game_control_buttons:
                button.handle_event(event)

    def refresh(self):
        self.make_move()
        self.update_timers()
        self.check_game_end()

    # def show(self):
    #
    #
    #     pygame.display.update()
    #
    #     while self.run:
    #         pygame.time.delay(100)
    #         for event in pygame.event.get():
    #             self.handle_event(event)
    #
    #
    #         pygame.display.update()