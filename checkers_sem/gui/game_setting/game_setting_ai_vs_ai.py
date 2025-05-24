import pygame

from checkers_sem.gui.game_window.ai_vs_ai_window import AIVSAIWindow
from checkers_sem.gui.game_setting.game_setting_widget import GameSettingWidget
from checkers_sem.state import state

from checkers_sem.player.player import AIPlayer
from checkers_sem.gui.constants import DEPTH_WHITE_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, DEPTH_BLACK_TEXT
from checkers_sem.genetic.constants import AI_COEFS

from checkers_sem.gui.utils.pos import Pos

class GameSettingAIVSAI(GameSettingWidget):
    def __init__(self, surface: pygame.Surface, pos: Pos):
        super().__init__(surface, pos)

        self.depth_black_header, self.depth_black_text_val, self.depth_black_slider = self.init_slider(
            0.1, self.depth_slider_black_onclick,
            (DEPTH_BLACK_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, state.DEPTH_BLACK))

        self.depth_white_header, self.depth_white_text_val, self.depth_white_slider = self.init_slider(
            0.175, self.depth_slider_white_onclick,
            (DEPTH_WHITE_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, state.DEPTH_WHITE))

        self.coefs_header = self.init_coefs_header(0.4)

        self.coefs_edit_texts_headers = self.init_coefs_texts(0.425, 0.3)

        self.coefs_white_edit_texts = self.init_edit_texts(0.425, 0.35, 0.15)
        self.coefs_black_edit_texts = self.init_edit_texts(0.425, 0.75, 0.15)

    def depth_slider_white_onclick(self, val : int):
        state.DEPTH_WHITE = val
        self.depth_white_text_val.set_string(state.DEPTH_WHITE)
        self.depth_white_text_val.draw()

    def depth_slider_black_onclick(self, val: int):
        state.DEPTH_BLACK = val
        self.depth_black_text_val.set_string(state.DEPTH_BLACK)
        self.depth_black_text_val.draw()

    def handle_event(self, event: pygame.event.Event):
        self.time_slider.handle_event(event)
        self.depth_white_slider.handle_event(event)
        self.depth_black_slider.handle_event(event)
        for edit_text in self.coefs_white_edit_texts:
            edit_text.handle_event(event)
        for edit_text in self.coefs_black_edit_texts:
            edit_text.handle_event(event)

    def get_coefs(self) -> tuple[list[float], list[float]]:
        white_coefs = []
        black_coefs = []
        for edit_text in self.coefs_white_edit_texts:
            white_coefs.append(float(edit_text.get_string()))
        for edit_text in self.coefs_black_edit_texts:
            black_coefs.append(float(edit_text.get_string()))
        return white_coefs, black_coefs

    def start_game(self, screen: pygame.Surface):
        state.COEFS_WHITE, state.COEFS_BLACK = self.get_coefs()
        AIVSAIWindow(screen, (AIPlayer(state.COEFS_WHITE), AIPlayer(state.COEFS_BLACK))).show()

    def draw(self):
        super().draw()
        self.depth_white_header.draw()
        self.depth_white_text_val.draw()
        self.depth_white_slider.draw()

        self.depth_black_header.draw()
        self.depth_black_text_val.draw()
        self.depth_black_slider.draw()

        self.coefs_header.draw()
        for i in range(len(AI_COEFS)):
            self.coefs_edit_texts_headers[i].draw()
            self.coefs_white_edit_texts[i].draw()
            self.coefs_black_edit_texts[i].draw()
