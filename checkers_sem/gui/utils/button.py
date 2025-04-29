from collections.abc import Callable

import pygame

from checkers_sem.constants import *
from checkers_sem.gui.utils.widget import Widget

class Button(Widget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int], text : str,
                 onclick : Callable[[], None], **kwargs):
        super().__init__(surface, left_top)

        self.text = text

        self.first_border = kwargs.get('first_border', False)
        self.second_border = kwargs.get('second_border', False)

        if not self.first_border and self.second_border:
            raise Exception('second_border cannot be True if first_border is False')

        if self.first_border:
            self.draw_border()


        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)

        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)

        self.background_color = BACKGROUND_COLOR
        self.text_color = TEXT_COLOR
        self.onclick = onclick
        self.is_hovered = False

    def hover(self):
        self.background_color = HOVER_BACKGROUND_COLOR
        self.text_color = HOVER_TEXT_COLOR
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
                self.is_hovered = True
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
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int], background_image : str, onclick : Callable[[], None] = None):
        super().__init__(surface, left_top)
        self.background_image = background_image
        self.background_image = pygame.image.load(self.background_image).convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, self.surface.get_rect().size)
        self.onclick = onclick
        self.is_hovered = False


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

    # def clicked(self, mouse_pos : tuple[int, int]) -> bool:
    #     if self.screen_rect.collidepoint(mouse_pos) and self.onclick:
    #         self.onclick()
    #         return True
    #     return self.screen_rect.collidepoint(mouse_pos)
