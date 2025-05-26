"""
This module takes care of AI vs AI game settings.
"""

import pygame

from checkers_sem.gui.game_window.ai_vs_ai_window import AIVSAIWindow
from checkers_sem.gui.game_setting.game_setting_widget import GameSettingWidget
from checkers_sem.state import state
from checkers_sem.player.player import AIPlayer
from checkers_sem.gui.constants import DEPTH_WHITE_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, DEPTH_BLACK_TEXT
from checkers_sem.genetic.constants import AI_COEFS
from checkers_sem.gui.utils.pos import Pos


class GameSettingAIVSAI(GameSettingWidget):
    """
    This class takes care of AI vs AI game settings.
    """

    def __init__(self, surface: pygame.Surface, pos: Pos):
        """
        Initialize the human vs human game settings.
        Parameters
        ----------
        surface : pygame.Surface
            to draw the settings to
        pos : Pos
            position on the surface
        """
        super().__init__(surface, pos)

        self.depth_black_slider = self.init_slider(
            0.1, self.depth_slider_black_onclick,
            (DEPTH_BLACK_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, state.DEPTH_BLACK))

        self.depth_white_slider = self.init_slider(
            0.175, self.depth_slider_white_onclick,
            (DEPTH_WHITE_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, state.DEPTH_WHITE))

        self.coefs_header = self.init_coefs_header(0.4)

        self.coefs_edit_texts_headers = self.init_coefs_texts(0.425, 0.3)

        self.coefs_white_edit_texts = self.init_edit_texts(0.425, 0.35, 0.15)
        self.coefs_black_edit_texts = self.init_edit_texts(0.425, 0.75, 0.15)

    def depth_slider_white_onclick(self, val: int):
        """
        Defines white depth slider on click function.
        Parameters
        ----------
        val : int
            slider value
        """
        state.DEPTH_WHITE = val
        self.depth_white_slider[1].set_text(state.DEPTH_WHITE)
        self.depth_white_slider[1].draw()

    def depth_slider_black_onclick(self, val: int):
        """
        Defines black slider on click function.
        Parameters
        ----------
        val : int
            slider value
        """
        state.DEPTH_BLACK = val
        self.depth_black_slider[1].set_text(state.DEPTH_BLACK)
        self.depth_black_slider[1].draw()

    def handle_event(self, event: pygame.event.Event):
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            event to handle
        """
        self.time_slider.handle_event(event)
        self.depth_white_slider[2].handle_event(event)
        self.depth_black_slider[2].handle_event(event)
        for edit_text in self.coefs_white_edit_texts:
            edit_text.handle_event(event)
        for edit_text in self.coefs_black_edit_texts:
            edit_text.handle_event(event)

    def get_coefs(self) -> tuple[list[float], list[float]]:
        """
        Gets AI coefficients from edit texts.
        Returns
        -------
        coefs : list[float]
            AI coefficients
        """
        white_coefs = []
        black_coefs = []
        for edit_text in self.coefs_white_edit_texts:
            white_coefs.append(float(edit_text.get_string()))
        for edit_text in self.coefs_black_edit_texts:
            black_coefs.append(float(edit_text.get_string()))
        return white_coefs, black_coefs

    def start_game(self, screen: pygame.Surface) -> None:
        """
        Starts the game.
        Parameters
        ----------
        screen : pygame.Surface
            to draw the game to
        """
        state.COEFS_WHITE, state.COEFS_BLACK = self.get_coefs()
        AIVSAIWindow(screen, (AIPlayer(state.COEFS_WHITE), AIPlayer(state.COEFS_BLACK))).show()

    def draw(self) -> None:
        """
        Draws the widget
        """
        super().draw()
        self.depth_white_slider[0].draw()
        self.depth_white_slider[1].draw()
        self.depth_white_slider[2].draw()

        self.depth_black_slider[0].draw()
        self.depth_black_slider[1].draw()
        self.depth_black_slider[2].draw()

        self.coefs_header.draw()
        for i in range(len(AI_COEFS)):
            self.coefs_edit_texts_headers[i].draw()
            self.coefs_white_edit_texts[i].draw()
            self.coefs_black_edit_texts[i].draw()
