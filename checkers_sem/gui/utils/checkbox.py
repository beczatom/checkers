import pygame

from checkers_sem.constants import BACKGROUND_COLOR, CHECKED_CHECKBOX_BACKGROUND
from checkers_sem.gui.utils.widget import Widget

class CheckBox(Widget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int], **kwargs):
        super().__init__(surface, left_top)

        self.draw_border()
        self.background_color = BACKGROUND_COLOR
        self.is_hovered = False
        self.is_checked = False

        self.on_uncheck = kwargs.get('on_uncheck', None)
        self.on_check = kwargs.get('on_check', None)

    def set_value(self, value : bool):
        self.is_checked = value

    def get_value(self):
        return self.is_checked

    def hover(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def unhover(self):
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
                self.is_checked = not self.is_checked
                if self.is_checked and self.on_check is not None:
                    self.on_check()
                elif not self.is_checked and self.on_uncheck is not None:
                    self.on_uncheck()
                self.draw()

    def draw(self):
        self.draw_border()
        if self.is_checked:
            image = CHECKED_CHECKBOX_BACKGROUND
            image = pygame.image.load(image).convert_alpha()
            image = pygame.transform.scale(image, self.rect_without_border.size)
            self.surface.blit(image, self.rect_without_border.topleft)
