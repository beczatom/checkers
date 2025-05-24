import pygame

from checkers_sem.gui.game_setting.game_setting_widget import GameSettingWidget
from checkers_sem.gui.game_window.human_vs_human_window import HumanVsHumanWindow
from checkers_sem.player.player import HumanPlayer
from checkers_sem.state import state
from checkers_sem.gui.constants import DEPTH_BLACK_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX
from checkers_sem.genetic.constants import AI_COEFS

from checkers_sem.gui.utils.pos import Pos

class GameSettingHumanVSHuman(GameSettingWidget):
    def __init__(self, surface: pygame.Surface, pos : Pos):
        super().__init__(surface, pos)

        self.depth_header, self.depth_text_val, self.depth_slider = self.init_slider(
            0.1, self.depth_slider_onclick,
            (DEPTH_BLACK_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, state.DEPTH_BLACK))

        self.coefs_header = self.init_coefs_header(0.25)

        self.coefs_edit_texts_headers = self.init_coefs_texts(0.325, 0.3)

        self.coefs_edit_texts = self.init_edit_texts(0.325, 0.5, 0.15)

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

    def start_game(self, screen: pygame.Surface):
        state.COEFS_BLACK = self.get_coefs()
        HumanVsHumanWindow(screen, (HumanPlayer(), HumanPlayer())).show()

    def draw(self):
        super().draw()
        self.depth_header.draw()
        self.depth_text_val.draw()
        self.depth_slider.draw()

        self.coefs_header.draw()
        for i in range(len(AI_COEFS)):
            self.coefs_edit_texts_headers[i].draw()
            self.coefs_edit_texts[i].draw()