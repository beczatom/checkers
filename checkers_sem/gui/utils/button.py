
from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.utils.loader import loader
from checkers_sem.gui.constants import (DEFAULT_FONT_SIZE, DEFAULT_FONT, BACKGROUND_COLOR, TEXT_COLOR, HOVER_TEXT_COLOR,
                                    HOVER_BACKGROUND_COLOR)
import pygame

class Button(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.first_border = kwargs.get('first_border', False)
        self.second_border = kwargs.get('second_border', False)

        if not self.first_border and self.second_border:
            raise Exception('second_border cannot be True if first_border is False')

        if self.first_border:
            self.draw_border()


        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)
        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)
        self.text = kwargs.get('text', '')
        self.onclick = kwargs.get('onclick', None)

        self.background_color = BACKGROUND_COLOR
        self.text_color = TEXT_COLOR
        self.is_hovered = False

    def hover(self):
        self.background_color = HOVER_BACKGROUND_COLOR
        self.text_color = HOVER_TEXT_COLOR
        self.is_hovered = True
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def unhover(self):
        self.background_color = BACKGROUND_COLOR
        self.text_color = TEXT_COLOR
        self.is_hovered = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_event(self, event : pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            if self.screen_rect.collidepoint(event.pos):
                self.hover()
                self.draw()
            else:
                if self.is_hovered:
                    self.unhover()
                    self.draw()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.screen_rect.collidepoint(event.pos):
                self.onclick()

    def draw(self):
        self.draw_border()

        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)

class ImageButton(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.onclick = kwargs.get('onclick', None)

        self.background_image = kwargs.get('background_image', '')
        self.background_image = loader.LOADED_IMAGES[self.background_image]
        self.background_image = pygame.transform.scale(self.background_image, self.surface.get_rect().size)

        self.is_hovered = False

    def set_background_image(self, name : str):
        self.background_image = loader.LOADED_IMAGES[name]
        self.background_image = pygame.transform.scale(self.background_image, self.surface.get_rect().size)

    def draw(self):
        self.surface.fill(BACKGROUND_COLOR)
        self.surface.blit(self.background_image, self.surface.get_rect().topleft)

    def handle_event(self, event : pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            if self.screen_rect.collidepoint(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.is_hovered = True
            else:
                if self.is_hovered:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.is_hovered = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                and self.screen_rect.collidepoint(event.pos):
            self.onclick()
