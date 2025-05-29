"""
This module provides a parent class to different modes of game settings.
"""

from typing import Callable
from abc import abstractmethod

import pygame

from app.gui.widgets.widget import Widget
from app.gui.widgets.text import Text
from app.gui.widgets.slider import Slider
from app.gui.widgets.edit_text import EditText
from app.gui.constants import DEFAULT_FONT_SIZE, TIME_SLIDER_TEXT, TIME_SLIDER_MIN, TIME_SLIDER_MAX, \
    STAT_TEXTS, COEFICIENTS_TEXT
from app.utils.helper import seconds_to_string
from app.utils.state import state
from app.gui.widgets.pos import Pos


class GameSettingWidget(Widget):
    """
    This class provides a parent class to different modes of game settings.
    """

    def __init__(self, *args):
        """
        Initialise the game settings widget.
        Parameters
        ----------
        args
            needed for parent class (Widget)
        """
        super().__init__(*args)
        self.time_header_text, self.time_slider_val, self.time_slider = self.init_slider(
            0.025, self.time_slider_onclick, (TIME_SLIDER_TEXT, TIME_SLIDER_MIN, TIME_SLIDER_MAX, state.TIME), seconds_to_string)

    def init_slider(self, top: float, onclick: Callable[[int], None], properties: tuple[str, int, int, int], formatter : Callable[[int], str] = None) -> tuple[
        Text, Text, Slider]:
        """
        Initializes a slider.
        Parameters
        ----------
        top : float
            top margin
        onclick : Callable[[int], None]
            slider onchange function
        properties : tuple[str, int, int, int]
            slider title, min, max and initial value
        formatter : Callable[[int], str] = None
            to format displayed value

        Returns
        -------
        header, value_text, slider : tuple[Text, Text, Slider]
            the slider title text, value text and slider
        """
        text, min_val, max_val, initial_val = properties

        header_text = Text(self.surface,
                           Pos((0.4, 0.075), (top, 0, 0, 0.1)),
                           self.screen_left_top,
                           text=text)

        slider_text_val = Text(self.surface,
                               Pos((0.1, 0.075), (top, 0, 0, 0.45)),
                               self.screen_left_top,
                               text=formatter(initial_val) if formatter else initial_val)

        slider = Slider(self.surface,
                        Pos((0.3, 0.075), (top, 0, 0, 0.6)),
                        self.left_top,
                        min=min_val, max=max_val, initial=initial_val, onchange=onclick)

        return header_text, slider_text_val, slider

    def time_slider_onclick(self, value: int) -> None:
        """
        Defines slider onclick event.
        Parameters
        ----------
        value : int
            value of the slider
        """
        state.TIME = value
        self.time_slider_val.set_text(seconds_to_string(self.time_slider.get_value()))

    def init_coefs_header(self, top: float) -> Text:
        """
        Initializes the header text for AI coefficients.
        Parameters
        ----------
        top : float
            top margin

        Returns
        -------
        text : Text
            Initialized header text
        """
        header_text = COEFICIENTS_TEXT
        coefs_header = Text(self.surface,
                            Pos((0.3, 0.1), (top, 0, 0.8, 0), center=True),
                            self.left_top,
                            text=header_text)
        return coefs_header

    def init_coefs_texts(self, top: float, size_x: float) -> list[Text]:
        """
        Initializes the titles of AI coefficients.
        Parameters
        ----------
        top : float
            top margin
        size_x : float
            size in x axis

        Returns
        -------
        texts : list[Text]
            Titles of AI coefficients
        """
        coefs_texts = []
        for i, stat_name in enumerate(STAT_TEXTS):
            font_size = 4 * DEFAULT_FONT_SIZE // 5
            coefs_texts.append(Text(self.surface,
                                    Pos((size_x, 0.075), (top + i * 0.09, 0.5, 1 - top - i * 0.09, 0.1), center=True),
                                    self.left_top,
                                    text=stat_name, font_size=font_size))
        return coefs_texts

    def init_edit_texts(self, top: float, left: float, size_x: float, init_vals = list[float]) -> list[EditText]:
        """
        Initializes the edit texts of AI coefficients.
        Parameters
        ----------
        top : float
            top margin
        left : float
            left margin
        size_x : float
            size in x axis
        init_vals : float
            initial values for coefficients

        Returns
        -------
        edit_texts : list[EditText]
            Edit texts of AI coefficients
        """
        edit_texts = []
        for i in range(len(STAT_TEXTS)):
            font_size = 4 * DEFAULT_FONT_SIZE // 5
            edit_texts.append(EditText(self.surface,
                                       Pos((size_x, 0.075), (top + i * 0.09, 0.1, 1 - top - i * 0.09, left),
                                           center=True),
                                       self.left_top,

                                       text=init_vals[i], font_size=font_size))
            edit_texts[-1].draw()
        return edit_texts

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Abstract method to handle events. This method must be overridden.
        Parameters
        ----------
        event : pygame.event.Event
            The event to handle

        Raises
        ------
        error : NotImplementedError
            If the method is not overridden.
        """
        raise NotImplementedError()

    @abstractmethod
    def start_game(self, screen: pygame.Surface):
        """
        Abstract method to start a game. This method must be overridden.
        Parameters
        ----------
        screen : pygame.Surface
            To start the game on.

        Raises
        ------
        error : NotImplementedError
            If the method is not overridden.
        """
        raise NotImplementedError()

    def draw(self):
        """
        Draws the settings.
        """
        self.time_header_text.draw()
        self.time_slider_val.draw()
        self.time_slider.draw()
