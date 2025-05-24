import pygame
import time

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.helper import seconds_to_string
from checkers_sem.gui.constants import DEFAULT_FONT, DEFAULT_FONT_SIZE, TEXT_COLOR
from checkers_sem.state import *

class Timer(Widget):
    def __init__(self, *args):
        super().__init__(*args)
        self.draw_border()
        self.font = pygame.font.Font(DEFAULT_FONT, DEFAULT_FONT_SIZE)

        self.time_left = state.TIME
        self.last_start = None
        self.time_going = False

    def time_start(self):
        if self.time_going: return
        self.last_start = time.time()
        self.time_going = True

    def time_stop(self):
        if not self.time_going: return
        self.time_left = self.get_time_left()
        self.last_start = None
        self.time_going = False

    def get_time_left(self) -> float:
        return max(0, self.time_left - (time.time() - self.last_start) if self.last_start else self.time_left)

    def time_is_over(self) -> bool:
        return self.get_time_left() == 0

    def draw(self):
        self.draw_border()
        text = self.font.render(seconds_to_string(self.get_time_left()), True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)
