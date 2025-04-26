import pygame

from checkers_sem.constants import *

class Button:
    def __init__(self, screen, rect : pygame.Rect, text : str, **kwargs):
        self.screen = screen
        self.rect = rect
        self.text = text
        self.background_color = kwargs.get('background_color', BACKGROUND_COLOR)

        self.first_border = kwargs.get('first_border', False)
        self.second_border = kwargs.get('second_border', False)

        if not self.first_border and self.second_border:
            raise Exception('second_border cannot be True if first_border is False')

        if self.first_border:
            self.draw_borders()


        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)

        self.font = pygame.font.Font('assets/SpecialElite-Regular.ttf', self.font_size)


    def draw_border(self, rect : pygame.Rect, border_width : int, border_gap : int):
        pygame.draw.rect(self.screen, BORDER_COLOR, rect)
        rect = pygame.Rect(rect.left + border_width, rect.top + border_width,
                           rect.width - 2 * border_width, rect.height - 2 * border_width)
        pygame.draw.rect(self.screen, self.background_color, rect)
        return pygame.Rect(rect.left + border_gap, rect.top + border_gap,
                           rect.width - 2 * border_gap, rect.height - 2 * border_gap)

    def draw_borders(self):
        available_rect = self.rect
        if self.first_border:
            available_rect = self.draw_border(available_rect, FIRST_BORDER_WIDTH, BORDER_GAP)
            if self.second_border:
                available_rect = self.draw_border(available_rect, SECOND_BORDER_WIDTH, 0)

        self.rect = available_rect


    def draw(self, mouse_pos):
        background_color = HOVER_BACKGROUND_COLOR if self.rect.collidepoint(mouse_pos) else self.background_color
        text_color = HOVER_TEXT_COLOR if self.rect.collidepoint(mouse_pos) else TEXT_COLOR

        pygame.draw.rect(self.screen, background_color, self.rect)
        text = self.font.render(self.text, True, text_color)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)


    def clicked(self, mouse_pos : tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)


class ImageButton:
    def __init__(self, surface : pygame.Surface, rect : pygame.Rect, background_image):
        self.surface = surface
        self.rect = rect
        self.background_image = background_image
        self.background_image = pygame.image.load(self.background_image).convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, self.surface.get_rect().size)


    def draw(self, mouse_pos : tuple[int, int] = (0, 0)):
        # pygame.draw.rect(self.screen, BACKGROUND_COLOR, self.rect)
        self.surface.fill(BACKGROUND_COLOR)
        self.surface.blit(self.background_image, self.surface.get_rect().topleft)

    def clicked(self, mouse_pos : tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
