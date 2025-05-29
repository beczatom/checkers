"""
This module takes care of Human vs AI game settings.
"""

import pygame
from app.gui.game_window.human_vs_ai_window import HumanVSAIWindow
from app.player.player import HumanPlayer, AIPlayer
from app.utils.state import state
from app.gui.game_setting.game_setting_widget import GameSettingWidget
from app.gui.constants import DEPTH_BLACK_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX
from app.genetic.constants import AI_COEFS
from app.gui.widgets.pos import Pos

class GameSettingHumanVSAI(GameSettingWidget):
    """
    This class takes care of Human vs AI game settings.
    """
    def __init__(self, surface : pygame.Surface, pos : Pos):
        """
        Initialize the human vs AI game settings.
        Parameters
        ----------
        surface : pygame.Surface
            to draw the settings to
        pos : Pos
            position on the surface
        """

        super().__init__(surface, pos)

        self.depth_header, self.depth_text_val, self.depth_slider = self.init_slider(
            0.1, self.depth_slider_onclick,
            (DEPTH_BLACK_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, state.DEPTH_BLACK))

        self.coefs_header = self.init_coefs_header(0.25)

        self.coefs_edit_texts_headers = self.init_coefs_texts(0.325, 0.3)

        self.coefs_edit_texts = self.init_edit_texts(0.325, 0.5, 0.15, state.COEFS_BLACK)


    def depth_slider_onclick(self, val : int) -> None:
        """
        Defines depth slider on click function.
        Parameters
        ----------
        val : int
            slider value
        """
        state.DEPTH_BLACK = val
        self.depth_text_val.set_text(state.DEPTH_BLACK)
        self.depth_text_val.draw()


    def handle_event(self, event : pygame.event.Event) -> None:
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            event to handle
        """
        self.time_slider.handle_event(event)
        self.depth_slider.handle_event(event)
        self.depth_text_val.set_text(state.DEPTH_BLACK)
        for edit_text in self.coefs_edit_texts:
            edit_text.handle_event(event)

    def get_coefs(self) -> list[float]:
        """
        Gets AI coefficients from edit texts.
        Returns
        -------
        coefs : list[float]
            AI coefficients
        """
        coefs = []
        for edit_text in self.coefs_edit_texts:
            coefs.append(float(edit_text.get_string()))
        return coefs

    def start_game(self, screen : pygame.Surface) -> None:
        """
        Starts the game.
        Parameters
        ----------
        screen : pygame.Surface
            to draw the game to
        """
        state.COEFS_BLACK = self.get_coefs()
        state.DEPTH_BLACK = self.depth_slider.get_value()
        HumanVSAIWindow(screen, (HumanPlayer(), AIPlayer(state.COEFS_BLACK))).show()

    def draw(self) -> None:
        """
        Draws the widget
        """
        super().draw()
        self.depth_header.draw()
        self.depth_text_val.draw()
        self.depth_slider.draw()

        self.coefs_header.draw()
        for i in range(len(AI_COEFS)):
            self.coefs_edit_texts_headers[i].draw()
            self.coefs_edit_texts[i].draw()
