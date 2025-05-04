from collections.abc import Callable

import pygame

from checkers_sem.gui.utils.window import Window
from checkers_sem.gui.genetic_window import GeneticWindow
from checkers_sem.gui.utils.slider import Slider
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.button import Button
from checkers_sem.constants import SLIDER_PROPERTIES
from checkers_sem.helper import *

from checkers_sem.state import *

class GeneticSettingWindow(Window):
    def __init__(self, surface):
        super().__init__(surface)
        self.genetic_settings = [SLIDER_PROPERTIES[i][3] if i < 3 else SLIDER_PROPERTIES[i][3] / 100 for i in range(5)]
        self.slider_headers, self.slider_text_vals, self.sliders = self.init_sliders()
        self.awaited_time_header, self.awaited_time = self.init_awaited_time()
        self.start_button = self.init_start_button()

    def start_button_onclick(self) -> None:
        self.set_global_genetic_settings()
        GeneticWindow(self.surface).show()

    def get_setting_function(self, i : int) -> Callable[[int], None]:
        def set_genetic_setting(value : int) -> None:
            if i in range(3, 5):
                value /= 100
            self.genetic_settings[i] = value

        return set_genetic_setting

    def set_global_genetic_settings(self):
        state.POPULATION_SIZE = self.genetic_settings[0]
        state.GENERATIONS = self.genetic_settings[1]
        state.MAX_TRAIN_DEPTH = self.genetic_settings[2]
        state.CROSSOVER_PCT = self.genetic_settings[3]
        state.MUTATION_PCT = self.genetic_settings[4]

    def init_start_button(self):
        margin_x = 6 * self.surface.get_rect().width // 8

        space_y = self.surface.get_rect().height - self.awaited_time.get_screen_bottom()
        margin_y = self.awaited_time.get_screen_bottom() + space_y // 4
        size_y = space_y // 3
        size_x = margin_x // 6

        button_rect = pygame.Rect(margin_x, margin_y, size_x, size_y)

        button = Button(self.surface.subsurface(button_rect), (margin_x, margin_y),
                        START_TRAIN_BUTTON_TEXT, self.start_button_onclick)
        return button

    def get_time_text_from_sliders(self):
        values = self.get_slider_values()[0:3]
        seconds = get_awaited_train_time(*values)
        return time_to_text(seconds)

    def get_slider_values(self):
        return [slider.get_value() for slider in self.sliders]

    def init_awaited_time(self) -> tuple[Text, Text]:
        margin_x = self.surface.get_rect().width // 8
        padding_x = self.surface.get_rect().width // 14

        space_y = self.surface.get_rect().height - self.sliders[-1].get_screen_bottom()
        margin_y = self.sliders[-1].get_screen_bottom() + space_y // 4
        size_y = space_y // 6
        size_x = (self.surface.get_rect().width - 2 * margin_x - padding_x) // 2

        text_rect = pygame.Rect(margin_x, margin_y, size_x, size_y)
        header = Text(self.surface.subsurface(text_rect), (margin_x, margin_y), AWAITED_TIME_TRAIN_TEXT)

        margin_x += size_x + padding_x

        text_rect = pygame.Rect(margin_x, margin_y, size_x, size_y)

        text = Text(self.surface.subsurface(text_rect), (margin_x, margin_y), self.get_time_text_from_sliders())
        return header, text

    def init_sliders(self) -> tuple[list[Text], list[Text], list[Slider]]:
        sliders = []
        slider_text_vals = []
        slider_headers = []

        margin_x = self.surface.get_rect().width // 8
        margin_y_top = self.surface.get_rect().height // 5
        margin_y_bottom = self.surface.get_rect().height // 3

        padding_between = (self.surface.get_rect().height - margin_y_top - margin_y_bottom) // 10

        size_x = self.surface.get_rect().width - 2 * margin_x
        size_y = (self.surface.get_rect().height -  margin_y_top - margin_y_bottom - 4 * padding_between) // 5

        for i in range(5):
            text, min_val, max_val, initial_val = SLIDER_PROPERTIES[i]
            top = margin_y_top + i * padding_between + i * size_y
            padding_x = size_x // 10

            left = margin_x

            text_rect = pygame.Rect(margin_x, top, 6 * (size_x - 2 * padding_x) // 16, size_y)
            slider_headers.append(Text(self.surface.subsurface(text_rect), (margin_x, top), text))

            left += text_rect.width + padding_x

            slider_text_rect = pygame.Rect(left, top, (size_x - 2 * padding_x) // 16, size_y)
            slider_text_vals.append(Text(self.surface.subsurface(slider_text_rect), (left, top), initial_val))

            left += slider_text_rect.width + padding_x

            slider_rect = pygame.Rect(left, top, 9 * (size_x - 2 * padding_x) // 16, size_y)
            sliders.append(Slider(self.surface.subsurface(slider_rect), (left, top), min_val, max_val, initial_val,
                                  self.get_setting_function(i)))

        return slider_headers, slider_text_vals, sliders


    def handle_event(self, event : pygame.event.Event):
        super().handle_event(event)

        self.start_button.handle_event(event)

        for i, slider in enumerate(self.sliders):
            slider.handle_event(event)
            self.slider_text_vals[i].set_string(slider.get_value())

        self.awaited_time.set_string(self.get_time_text_from_sliders())

    def refresh(self):
        for i in range(len(self.genetic_settings)):
            self.slider_headers[i].draw()
            self.slider_text_vals[i].draw()
            self.sliders[i].draw()
        self.awaited_time.draw()
        self.start_button.draw()