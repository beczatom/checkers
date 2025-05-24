import pygame

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.constants import (DEFAULT_FONT, FIRST_BORDER_WIDTH, BACKGROUND_COLOR, BORDER_GAP, DEFAULT_TEXT_COLOR,
                                    DEFAULT_FONT_SIZE)

class EditText(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)
        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)
        self.text = str(kwargs.get('text', ''))

        self.editing = False

    def set_string(self, text : str | int | float):
        self.text = str(text)

    def get_string(self) -> str:
        return self.text

    def handle_event(self, event : pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.editing = self.screen_rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.editing:
            if event.key == pygame.K_BACKSPACE and len(self.text) > 0:
                self.text = self.text[:-1]

            if event.unicode.isdigit():
                self.text = self.text + str(event.unicode)

            if len(self.text) < 2:
                self.text = '0.'

            if len(self.text) > 5:
                self.text = self.text[:5]

            self.draw()

    def draw(self):
        self.draw_one_border(self.surface.get_rect(), FIRST_BORDER_WIDTH, BORDER_GAP)
        self.surface.fill(BACKGROUND_COLOR, self.rect_without_border)
        text = self.font.render(self.text, True, DEFAULT_TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect_without_border.center)
        self.surface.blit(text, text_rect)