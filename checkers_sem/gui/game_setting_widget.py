from collections.abc import Callable

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.slider import Slider
from checkers_sem.gui.utils.edit_text import EditText
import pygame

from checkers_sem.helper import *

from checkers_sem.state import *

class GameSettingWidget(Widget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int]):
        super().__init__(surface, left_top)
        self.time_slider_val, self.time_slider = self.init_time_slider()


    def init_time_slider(self) -> tuple[Text, Slider]:
        left = 0
        top = DEFAULT_FONT_SIZE

        size_x = self.surface.get_rect().width
        size_y = 3 * DEFAULT_FONT_SIZE // 2

        text, min_val, max_val, initial_val = TIME_SLIDER_PROPERTIES
        padding_x = size_x // 10

        text_rect = pygame.Rect(left, top, 4 * (size_x - 2 * padding_x) // 16, size_y)
        Text(self.surface.subsurface(text_rect),
             tuple_sum(self.left_top, (left, top)), text).draw()

        left += text_rect.width + padding_x

        slider_text_rect = pygame.Rect(left, top, 3 * (size_x - 2 * padding_x) // 16, size_y)
        slider_text_val = Text(self.surface.subsurface(slider_text_rect),
                               tuple_sum(self.left_top, (left, top)),
                               seconds_to_min_sec(initial_val))
        slider_text_val.draw()

        left += slider_text_rect.width + padding_x

        slider_rect = pygame.Rect(left, top, 9 * (size_x - 2 * padding_x) // 16, size_y)
        slider = Slider(self.surface.subsurface(slider_rect),
                        tuple_sum(self.left_top, (left, top)), min_val, max_val, initial_val,
                              self.time_slider_onclick)

        slider.draw()

        return slider_text_val, slider

    def time_slider_onclick(self, value : int):
        state.TIME = value
        self.time_slider_val.set_string(seconds_to_min_sec(self.time_slider.get_value()))
        self.time_slider_val.draw()

    def init_coefs_header(self, top : int):
        text_rect = pygame.Rect(0, top, self.surface.get_width(), DEFAULT_FONT_SIZE)
        header_text = COEFICIENTS_TEXT
        coefs_header = Text(self.surface.subsurface(text_rect), tuple_sum(self.screen_left_top, (0, top)),
                            header_text)
        coefs_header.draw()

    def init_coefs_texts(self, top : int, size_x : int):
        for stat_name in STAT_TEXTS:
            font_size = 4 * DEFAULT_FONT_SIZE // 5
            size_y = 2 * font_size
            text_rect = pygame.Rect(0, top, size_x, size_y)
            Text(self.surface.subsurface(text_rect),
                 tuple_sum(self.screen_left_top, (0, top)), stat_name, font_size=font_size).draw()
            top += size_y + size_y // 4

    def init_edit_texts(self, top : int, left : int, size_x : int) -> list[EditText]:
        edit_texts = []
        for i in range(len(STAT_TEXTS)):
            font_size = 4 * DEFAULT_FONT_SIZE // 5
            size_y = 8 * DEFAULT_FONT_SIZE // 5

            option_value_text_rect = pygame.Rect(left, top, size_x, size_y)
            edit_texts.append(EditText(self.surface.subsurface(option_value_text_rect),
                                       tuple_sum(self.screen_left_top, (left, top)),
                         AI_COEFS[i], font_size=font_size))

            top += size_y + size_y // 4
            edit_texts[-1].draw()
        return edit_texts


    def init_depth_slider(self, top : int, onclick : Callable[[int], [None]]) -> tuple[Text, Slider]:
        left = 0

        size_x = self.surface.get_rect().width
        size_y = 3 * DEFAULT_FONT_SIZE // 2

        text, min_val, max_val, initial_val = DEPTH_SLIDER_PROPERTIES
        padding_x = size_x // 10

        text_rect = pygame.Rect(left, top, 4 * (size_x - 2 * padding_x) // 16, size_y)
        Text(self.surface.subsurface(text_rect),
             tuple_sum(self.screen_left_top, (left, top)), text).draw()

        left += text_rect.width + padding_x

        slider_text_rect = pygame.Rect(left, top, 3 * (size_x - 2 * padding_x) // 16, size_y)
        slider_text_val = Text(self.surface.subsurface(slider_text_rect),
                               tuple_sum(self.screen_left_top, (left, top)), initial_val)
        slider_text_val.draw()

        left += slider_text_rect.width + padding_x

        slider_rect = pygame.Rect(left, top, 9 * (size_x - 2 * padding_x) // 16, size_y)
        slider = Slider(self.surface.subsurface(slider_rect),
                        tuple_sum(self.screen_left_top, (left, top)), min_val, max_val, initial_val,
                        onclick)

        slider.draw()

        return slider_text_val, slider


    def handle_event(self, event : pygame.event.Event):
        raise NotImplementedError()

    def start_game(self, screen : pygame.Surface):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()