"""
This module sets the parameters for genetic training
"""

from typing import Callable
import pygame

from app.gui.utils.window import Window
from app.gui.genetic_window.genetic_window import GeneticWindow
from app.gui.utils.slider import Slider
from app.gui.utils.text import Text
from app.gui.utils.button import Button
from app.gui.constants import SLIDER_PROPERTIES, AWAITED_TIME_TRAIN_TEXT, START_TRAIN_BUTTON_TEXT
from app.helper import get_awaited_train_time, time_to_text
from app.gui.utils.pos import Pos
from app.state import state

class GeneticSettingWindow(Window):
    """
    This window lets the user choose genetic training settings
    """
    def __init__(self, surface : pygame.Surface):
        """
        Initialize the window
        Parameters
        ----------
        surface : pygame.Surface
            The surface where the window will be displayed
        """
        super().__init__(surface)
        self.genetic_settings = [SLIDER_PROPERTIES[i][3] if i < 3 else SLIDER_PROPERTIES[i][3] / 100 for i in range(5)]
        self.slider_headers, self.slider_text_vals, self.sliders = self.init_sliders()
        self.awaited_time_header, self.awaited_time = self.init_awaited_time()
        self.start_button = self.init_start_button()

    def start_button_onclick(self) -> None:
        """
        Defines the start button click event
        """
        self.set_global_genetic_settings()
        GeneticWindow(self.surface).show()

    def get_setting_function(self, i : int) -> Callable[[int], None]:
        """
        Gets slider onchange behaviour.
        Parameters
        ----------
        i : int
            which slider

        Returns
        -------
        onchange : Callable[[int], None]
            slider onchange function
        """
        def set_genetic_setting(value : int) -> None:
            if i in range(3, 5):
                value /= 100
            self.genetic_settings[i] = value

        return set_genetic_setting

    def set_global_genetic_settings(self) -> None:
        """
        Sets genetic settings to global state
        """
        state.POPULATION_SIZE = self.genetic_settings[0]
        state.GENERATIONS = self.genetic_settings[1]
        state.MAX_TRAIN_DEPTH = self.genetic_settings[2]
        state.CROSSOVER_PCT = self.genetic_settings[3]
        state.MUTATION_PCT = self.genetic_settings[4]

    def init_start_button(self) -> Button:
        """
        Initializes the training start button
        Returns
        -------
        start_button : Button
            the genetic starting button
        """
        button = Button(self.surface,
                        Pos((0.125, 0.075), (0.8, 0.05, 0.05, 0.8), center=True),
                        text=START_TRAIN_BUTTON_TEXT, onclick=self.start_button_onclick)
        return button

    def get_time_text_from_sliders(self) -> str:
        """
        Gets estimated time in string from sliders
        Returns
        -------
        estimated_time : str
            estimated time in string from sliders
        """
        values = self.get_slider_values()[0:3]
        seconds = get_awaited_train_time(*values)
        return time_to_text(seconds)

    def get_slider_values(self) -> list[int]:
        """
        Gets values from sliders
        Returns
        -------
        values : list[int]
            values from sliders
        """
        return [slider.get_value() for slider in self.sliders]

    def init_awaited_time(self) -> tuple[Text, Text]:
        """
        Initializes awaited time header and value text.
        Returns
        -------
        header, text : tuple[Text, Text]
            header and value text for awaited time
        """
        header = Text(self.surface,
                      Pos((0.3, 0.1), (0.75, 0.5, 0.15, 0.1), center=True),
                      text = AWAITED_TIME_TRAIN_TEXT)

        text = Text(self.surface,
                    Pos((0.3, 0.1), (0.75, 0.2, 0.15, 0.6), center=True),
                    text = self.get_time_text_from_sliders())
        return header, text

    def init_sliders(self) -> tuple[list[Text], list[Text], list[Slider]]:
        """
        Initializes header, value text and sliders.
        Returns
        -------
        headers, value_texts, sliders : tuple[list[Text], list[Text], list[Slider]]
            headers, value_texts and sliders for each setting
        """
        sliders = []
        slider_text_vals = []
        slider_headers = []

        for i in range(5):
            text, min_val, max_val, initial_val = SLIDER_PROPERTIES[i]

            slider_headers.append(Text(self.surface,
                                       Pos((0.3, 0.05), (0.2 + i * 0.1, 0.5, 0.75 - i * 0.1, 0.1)),
                                       text = text))

            slider_text_vals.append(Text(self.surface,
                                         Pos((0.1, 0.05), (0.2 + i * 0.1, 0.5, 0.75 - i * 0.1, 0.4)),
                                         text = initial_val))

            sliders.append(Slider(self.surface,
                                  Pos((0.3, 0.05), (0.2 + i * 0.1, 0.5, 0.75 - i * 0.1, 0.6)),
                                  min = min_val, max = max_val, initial = initial_val, onchange = self.get_setting_function(i)))

        return slider_headers, slider_text_vals, sliders


    def handle_event(self, event : pygame.event.Event) -> None:
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            event to handle
        """
        super().handle_event(event)

        self.start_button.handle_event(event)

        for i, slider in enumerate(self.sliders):
            slider.handle_event(event)
            self.slider_text_vals[i].set_text(slider.get_value())

        self.awaited_time.set_text(self.get_time_text_from_sliders())

    def refresh(self) -> None:
        """
        Redraws the window
        """
        for i in range(len(self.genetic_settings)):
            self.slider_headers[i].draw()
            self.slider_text_vals[i].draw()
            self.sliders[i].draw()
        self.awaited_time_header.draw()
        self.awaited_time.draw()
        self.start_button.draw()
