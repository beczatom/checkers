import pygame

from checkers_sem.constants import *

def seconds_to_string(seconds : float) -> str:
    return f'{int(seconds) // 60:02} : {int(seconds) % 60:02}'

class Timer:
    def __init__(self, surface, **kwargs):
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.background_color = kwargs.get('background_color', BACKGROUND_COLOR)

        self.first_border = kwargs.get('first_border', False)
        self.second_border = kwargs.get('second_border', False)

        if not self.first_border and self.second_border:
            raise Exception('second_border cannot be True if first_border is False')

        if self.first_border:
            self.draw_borders()

        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)

        self.font = pygame.font.Font('assets/SpecialElite-Regular.ttf', self.font_size)

    def draw_border(self, rect: pygame.Rect, border_width: int, border_gap: int):
        pygame.draw.rect(self.surface, BORDER_COLOR, rect)
        rect = pygame.Rect(rect.left + border_width, rect.top + border_width,
                           rect.width - 2 * border_width, rect.height - 2 * border_width)
        pygame.draw.rect(self.surface, self.background_color, rect)
        return pygame.Rect(rect.left + border_gap, rect.top + border_gap,
                           rect.width - 2 * border_gap, rect.height - 2 * border_gap)

    def draw_borders(self):
        available_rect = self.rect
        if self.first_border:
            available_rect = self.draw_border(available_rect, FIRST_BORDER_WIDTH, BORDER_GAP)
            if self.second_border:
                available_rect = self.draw_border(available_rect, SECOND_BORDER_WIDTH, 0)

        self.rect = available_rect

    def draw(self, seconds : float):
        pygame.draw.rect(self.surface, self.background_color, self.rect)
        text = self.font.render(seconds_to_string(seconds), True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect.center)
        self.surface.blit(text, text_rect)
