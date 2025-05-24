from collections.abc import Callable

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.slider import Slider
from checkers_sem.gui.utils.edit_text import EditText
import pygame

from checkers_sem.gui.constants import DEFAULT_FONT_SIZE, TIME_SLIDER_TEXT, TIME_SLIDER_MIN, TIME_SLIDER_MAX, STAT_TEXTS, COEFICIENTS_TEXT
from checkers_sem.genetic.constants import AI_COEFS

from checkers_sem.helper import seconds_to_min_sec

from checkers_sem.state import state

from checkers_sem.gui.utils.pos import Pos

from abc import abstractmethod

class GameSettingWidget(Widget):
    def __init__(self, *args):
        super().__init__(*args)
        print('game setting widget left_top', self.left_top)
        self.time_header_text, self.time_slider_val, self.time_slider = self.init_slider(
            0.025, self.time_slider_onclick, (TIME_SLIDER_TEXT, TIME_SLIDER_MIN, TIME_SLIDER_MAX, state.TIME))

    def init_slider(self, top : float, onclick : Callable[[int], None], properties : tuple[str, int, int, int]) -> tuple[Text, Text, Slider]:
        text, min_val, max_val, initial_val = properties

        header_text = Text(self.surface,
                           Pos((0.4, 0.075), (top, 0, 0, 0.1)),
                           self.screen_left_top,
                           text=text)

        slider_text_val= Text(self.surface,
                                Pos((0.1, 0.075), (top, 0, 0, 0.45)),
                                self.screen_left_top,
                                text=initial_val)

        slider = Slider(self.surface,
                        Pos((0.3, 0.075), (top, 0, 0, 0.6)),
                        self.left_top,
                        min=min_val, max=max_val, initial=initial_val, onchange=onclick)

        return header_text, slider_text_val, slider

    def time_slider_onclick(self, value : int):
        state.TIME = value
        self.time_slider_val.set_string(seconds_to_min_sec(self.time_slider.get_value()))

    def init_coefs_header(self, top : float) -> Text:
        header_text = COEFICIENTS_TEXT
        coefs_header = Text(self.surface,
                            Pos((0.3, 0.1), (top, 0, 0.8, 0), center = True),
                            self.left_top,
                            text = header_text)
        return coefs_header

    def init_coefs_texts(self, top : float, size_x : float) -> list[Text]:
        coefs_texts = []
        for i, stat_name in enumerate(STAT_TEXTS):
            font_size = 4 * DEFAULT_FONT_SIZE // 5
            coefs_texts.append(Text(self.surface,
                                    Pos((size_x, 0.075), (top + i * 0.09, 0.5, 1 - top - i * 0.09, 0.1), center=True),
                                    self.left_top,
                                    text=stat_name, font_size=font_size))
        return coefs_texts

    def init_edit_texts(self, top : float, left : float, size_x : float) -> list[EditText]:
        edit_texts = []
        for i in range(len(STAT_TEXTS)):
            font_size = 4 * DEFAULT_FONT_SIZE // 5
            edit_texts.append(EditText(self.surface,
                                       Pos((size_x, 0.075), (top + i * 0.09, 0.1, 1 - top - i * 0.09, left), center=True),
                                       self.left_top,

                         text=AI_COEFS[i], font_size=font_size))
            edit_texts[-1].draw()
        return edit_texts

    @abstractmethod
    def handle_event(self, event : pygame.event.Event):
        raise NotImplementedError()

    @abstractmethod
    def start_game(self, screen : pygame.Surface):
        raise NotImplementedError()

    def draw(self):
        self.time_header_text.draw()
        self.time_slider_val.draw()
        self.time_slider.draw()