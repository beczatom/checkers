import pygame

from checkers_sem.constants import BACKGROUND_COLOR, BORDER_COLOR, FIRST_BORDER_WIDTH, BORDER_GAP, SECOND_BORDER_WIDTH

class Widget:
    def __init__(self, surface : pygame.Surface, screen_left_top : tuple[int, int]):
        self.screen_left_top = screen_left_top
        self.left_top = screen_left_top
        self.screen_rect = pygame.Rect(*screen_left_top, *surface.get_rect().size)
        self.surface = surface
        self.surface.fill(BACKGROUND_COLOR)
        self.rect_without_border = surface.get_rect()
        self.background_color = BACKGROUND_COLOR

    def draw(self):
        raise Exception('Pure virtual method')

    def clicked(self, mouse_pos : tuple[int, int]):
        return self.screen_rect.collidepoint(mouse_pos)

    def draw_border(self):
        self.__draw_borders()

    def draw_one_border(self, rect: pygame.Rect, border_width: int, border_gap: int):
        pygame.draw.rect(self.surface, BORDER_COLOR, rect)
        rect = pygame.Rect(rect.x + border_width, rect.y + border_width,
                           rect.width - 2 * border_width, rect.height - 2 * border_width)
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, rect)
        self.rect_without_border = pygame.Rect(rect.x + border_gap, rect.y + border_gap,
                           rect.width - 2 * border_gap, rect.height - 2 * border_gap)

    def __draw_borders(self):
        self.draw_one_border(self.surface.get_rect(), FIRST_BORDER_WIDTH, BORDER_GAP)
        self.draw_one_border(self.rect_without_border, SECOND_BORDER_WIDTH, 0)
        pygame.draw.rect(self.surface, self.background_color, self.rect_without_border)

    def get_height(self):
        return self.surface.get_height()

    def get_width(self):
        return self.surface.get_width()

    def get_screen_top(self):
        return self.screen_left_top[1]

    def get_screen_left(self):
        return self.screen_left_top[0]

    def get_screen_bottom(self):
        return self.get_screen_top() + self.get_height()

    def handle_event(self, event : pygame.event.Event):
        pass