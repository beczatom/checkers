import pygame

from checkers_sem.gui.game_window import GameWindow
from checkers_sem.constants import *
from checkers_sem.player.player import AIPlayer, HumanPlayer


class HumanVSAIWindow(GameWindow):
    def __init__(self, surface : pygame.surface, players : tuple[HumanPlayer, AIPlayer]):
        super().__init__(surface, players)
        self.chessboard.draw()

        self.best_move_text, self.best_move_checkbox = self.init_best_move_checkbox()

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

        self.move_table.handle_event(event)
        if self.turn == Turn.WHITE:
            self.chessboard.handle_event(event)

        if self.active_thread is None:
            self.best_move_checkbox.handle_event(event)
            for button in self.game_control_buttons:
                button.handle_event(event)

    def refresh(self):

        if self.turn == Turn.WHITE or self.evaluating:
            if self.best_move_checkbox.get_value():
                self.evaluating_thread_check()
            self.make_move()

        # print(self.turn == Turn.BLACK, self.active_thread is not None, not self.evaluating)
        if (self.turn == Turn.BLACK or self.active_thread is not None) and not self.evaluating:
            # print('move ai')
            self.move_ai()

        self.update_eval_texts()
        self.update_timers()
        self.check_game_end()

        self.best_move_text.draw()
        self.best_move_checkbox.draw()
