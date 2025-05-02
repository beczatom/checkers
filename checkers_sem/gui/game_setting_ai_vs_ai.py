import pygame

from checkers_sem.gui.ai_vs_ai_window import AIVSAIWindow
from checkers_sem.gui.game_setting_widget import GameSettingWidget
from checkers_sem.helper import *

from checkers_sem.player.player import AIPlayer

class GameSettingAIVSAI(GameSettingWidget):
    def __init__(self, surface: pygame.Surface, left_top: tuple[int, int]):
        super().__init__(surface, left_top)

        top = self.time_slider.get_height() + 3 * DEFAULT_FONT_SIZE // 2

        self.depth_white_header, self.depth_white_text_val, self.depth_white_slider = self.init_slider(
            top, self.depth_slider_white_onclick, (DEPTH_WHITE_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, state.DEPTH_WHITE))

        top += self.depth_white_slider.get_height() + DEFAULT_FONT_SIZE // 2

        self.depth_black_header, self.depth_black_text_val, self.depth_black_slider = self.init_slider(
            top, self.depth_slider_black_onclick,(DEPTH_BLACK_TEXT, DEPTH_SLIDER_MIN, DEPTH_SLIDER_MAX, state.DEPTH_BLACK))

        top += self.depth_black_slider.get_height() + DEFAULT_FONT_SIZE

        self.coefs_header = self.init_coefs_header(top)

        top += 2 * DEFAULT_FONT_SIZE

        coefs_text_width = 8 * self.surface.get_width() // 16

        self.coefs_edit_texts_headers = self.init_coefs_texts(top, coefs_text_width)

        coefs_edit_text_width = 4 * self.surface.get_width() // 16

        self.coefs_white_edit_texts = self.init_edit_texts(top, coefs_text_width, 8 * coefs_edit_text_width // 10)

        self.coefs_black_edit_texts = self.init_edit_texts(top, 3 * coefs_text_width // 2, 8 * coefs_edit_text_width // 10)

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
        ai_coefs = self.get_coefs()
        AIVSAIWindow(screen, (AIPlayer(ai_coefs[0]), AIPlayer(ai_coefs[1]))).show()

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
