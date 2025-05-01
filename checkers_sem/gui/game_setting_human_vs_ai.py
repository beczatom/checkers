from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.slider import Slider
from checkers_sem.gui.utils.edit_text import EditText
from checkers_sem.gui.human_vs_ai_window import HumanVSAIWindow
from checkers_sem.player.player import HumanPlayer, AIPlayer
import pygame

from checkers_sem.helper import *

from checkers_sem.state import *
from checkers_sem.gui.game_setting_widget import GameSettingWidget


class GameSettingHumanVSAI(GameSettingWidget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int]):
        super().__init__(surface, left_top)

        top = self.time_slider.get_height() + 3 * DEFAULT_FONT_SIZE // 2

        self.depth_text_val, self.depth_slider = self.init_depth_slider(
            top, self.depth_slider_onclick)

        top += self.depth_slider.get_height() + DEFAULT_FONT_SIZE // 2

        self.init_coefs_header(top)

        top += 2 * DEFAULT_FONT_SIZE

        coefs_text_width = 10 * self.surface.get_width() // 16

        self.init_coefs_texts(top, coefs_text_width)

        coefs_edit_text_width = 6 * self.surface.get_width() // 16

        self.coefs_edit_texts = self.init_edit_texts(top, coefs_text_width, coefs_edit_text_width)


    def depth_slider_onclick(self, val : int):
        state.DEPTH_BLACK = val
        self.depth_text_val.set_string(state.DEPTH_BLACK)
        self.depth_text_val.draw()


    def handle_event(self, event : pygame.event.Event):
        self.time_slider.handle_event(event)
        self.depth_slider.handle_event(event)
        self.depth_text_val.set_string(state.DEPTH_BLACK)
        for edit_text in self.coefs_edit_texts:
            edit_text.handle_event(event)

    def get_coefs(self) -> list[float]:
        coefs = []
        for edit_text in self.coefs_edit_texts:
            coefs.append(float(edit_text.get_string()))
        return coefs

    def start_game(self, screen : pygame.Surface):
        ai_coefs = self.get_coefs()
        state.DEPTH_BLACK = self.depth_slider.get_value()
        HumanVSAIWindow(screen, (HumanPlayer(), AIPlayer(ai_coefs))).show()

    def draw(self):
        pass