"""
This module defines an AI vs AI game.
"""

import pygame


from checkers_sem.gui.game_window.game_window import GameWindow
from checkers_sem.player.player import AIPlayer
from checkers_sem.game.constants import Color

class AIVSAIWindow(GameWindow):
    """
    This class is a child of GameWindow for handling AI vs AI game.
    """

    def __init__(self, surface: pygame.surface, players: tuple[AIPlayer, AIPlayer]):
        """
        Initialize the AI vs AI game.
        Parameters
        ----------
        surface : pygame.surface
            to print the game to
        players : tuple[AIPlayer, AIPlayer]
            white and black
        """
        super().__init__(surface, players)
        self.game_display.chessboard.draw()

    def handle_event(self, event: pygame.event.Event) -> None:
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

        if event.type == pygame.MOUSEBUTTONDOWN:    # pylint: disable=no-member
            self.move_table.handle_event(event)
            for button in self.game_control_buttons:
                button.handle_event(event)

    def refresh(self) -> None:
        """
        Redraws the window.
        """
        if self.game_display.move_ai():
            self.move_table.set_move_texts(self.game_display.chessboard.game.get_move_history())
        self.game_display.eval_helper.update_eval()
        self.game_display.timers[Color.BLACK].draw()
        self.game_display.timers[Color.WHITE].draw()
        self.check_game_end()

    def reset(self) -> None:
        """
        Resets the window.
        """
        super().__init__(self.surface, self.players)
        self.game_display.chessboard.draw()
