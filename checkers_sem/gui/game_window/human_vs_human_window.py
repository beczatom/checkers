"""
This module defines an Human vs Human game.
"""

import pygame

from checkers_sem.gui.game_window.game_window import GameWindow
from checkers_sem.player.player import HumanPlayer
from checkers_sem.game.constants import Color

class HumanVsHumanWindow(GameWindow):
    """
    This class is a child of GameWindow for handling Human vs Human game.
    """

    def __init__(self, surface: pygame.surface, players: tuple[HumanPlayer, HumanPlayer]):
        """
        Initialize the Human vs Human game.
        Parameters
        ----------
        surface : pygame.surface
            to print the game to
        players : tuple[HumanPlayer, HumanPlayer]
            white and black
        """
        super().__init__(surface, players)
        self.best_move_text, self.best_move_checkbox = self.init_best_move_checkbox()

    def handle_event(self, event: pygame.event.Event):
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            event to handle
        """
        super().handle_event(event)
        self.move_table.handle_event(event)
        self.game_display.chessboard.handle_event(event)
        if self.active_thread is None:
            self.best_move_checkbox.handle_event(event)
            for button in self.game_control_buttons:
                button.handle_event(event)

    def refresh(self):
        """
        Redraws the window.
        """
        if self.res_window is not None:
            return
        self.best_move_text.draw()
        self.best_move_checkbox.draw()
        self.game_display.eval_helper.update_eval()
        if self.game_display.make_move():
            self.move_table.set_move_texts(self.game_display.chessboard.game.get_move_history())
        self.game_display.timers[Color.WHITE].draw()
        self.game_display.timers[Color.BLACK].draw()
        self.game_display.check_game_end()
        self.check_game_end()
        if self.best_move_checkbox.get_value():
            self.game_display.eval_helper.update_best_move()

    def reset(self) -> None:
        """
        Resets the window.
        """
        super().__init__(self.surface, self.players)
        self.game_display.chessboard.draw()
        self.best_move_text, self.best_move_checkbox = self.init_best_move_checkbox()
