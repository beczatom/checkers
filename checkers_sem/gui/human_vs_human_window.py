from checkers_sem.gui.game_window import *
from checkers_sem.constants import *
from checkers_sem.player.player import HumanPlayer

class HumanVsHumanWindow(GameWindow):
    def __init__(self, surface: pygame.surface, players: tuple[HumanPlayer, HumanPlayer]):
        super().__init__(surface, players)
        self.run = True
        self.chessboard.draw()

        self.best_move_text, self.best_move_checkbox = self.init_best_move_checkbox()

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
        self.move_table.handle_event(event)
        self.chessboard.handle_event(event)
        if self.active_thread is None:
            self.best_move_checkbox.handle_event(event)
            for button in self.game_control_buttons:
                button.handle_event(event)

    def refresh(self):
        self.best_move_text.draw()
        self.best_move_checkbox.draw()
        self.update_eval_texts()
        self.make_move()
        self.update_timers()
        self.check_game_end()
        if self.best_move_checkbox.get_value():
            self.evaluating_thread_check()