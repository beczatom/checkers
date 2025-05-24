import pygame

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.constants import DEFAULT_FONT, BACKGROUND_COLOR, DEFAULT_TEXT_COLOR, DEFAULT_FONT_SIZE

class Text(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)
        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)
        self.text = str(kwargs.get('text', ''))

    def set_string(self, string : str | int | float):
        self.text = str(string)

    def draw(self):
        self.surface.fill(BACKGROUND_COLOR)
        text = self.font.render(self.text, True, DEFAULT_TEXT_COLOR)
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)