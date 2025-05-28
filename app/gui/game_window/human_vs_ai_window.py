"""
This module defines an Human vs AI game.
"""

import pygame

from app.gui.game_window.game_window import GameWindow
from app.game.constants import Color
from app.player.player import AIPlayer, HumanPlayer


class HumanVSAIWindow(GameWindow):
    """
    This class is a child of GameWindow for handling Human vs AI game.
    """

    def __init__(self, surface: pygame.surface, players: tuple[HumanPlayer, AIPlayer]):
        """
        Initialize the Human vs AI game.
        Parameters
        ----------
        surface : pygame.surface
            to print the game to
        players : tuple[HumanPlayer, AIPlayer]
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

        if self.res_window is not None:
            return

        self.move_table.handle_event(event)
        if self.turn == Color.WHITE and self.game_display.active_thread is None:
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

        if self.game_display.turn == Color.WHITE and self.game_display.active_thread is None:
            if self.best_move_checkbox.get_value():
                self.game_display.eval_helper.update_best_move()
            if self.game_display.make_move():
                self.move_table.set_move_texts(self.game_display.chessboard.game.get_move_history())
            self.game_display.eval_helper.update_eval()

        if (self.game_display.turn == Color.BLACK or self.game_display.active_thread is not None) and self.game_display.eval_helper.active_thread is not None:
            if self.game_display.move_ai():
                self.move_table.set_move_texts(self.game_display.chessboard.game.get_move_history())
                self.game_display.eval_helper.best_move = None
                self.game_display.eval_helper.evaluation_start_hash = hash(None)

        self.game_display.timers[Color.WHITE].draw()
        self.game_display.timers[Color.BLACK].draw()
        self.check_game_end()

        self.best_move_text.draw()
        self.best_move_checkbox.draw()

    def reset(self) -> None:
        """
        Resets the window.
        """
        super().__init__(self.surface, self.players)
        self.game_display.chessboard.draw()
        self.best_move_text, self.best_move_checkbox = self.init_best_move_checkbox()
