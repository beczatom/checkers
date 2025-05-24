import pygame

from checkers_sem.gui.constants import BACKGROUND_COLOR, BORDER_COLOR, FIRST_BORDER_WIDTH, BORDER_GAP, SECOND_BORDER_WIDTH
from checkers_sem.gui.utils.pos import Pos
from checkers_sem.helper import tuple_prod, tuple_sum


class Widget:
    def __init__(self, surface : pygame.Surface, rel_pos : Pos, screen_left_top : tuple[int, int] = (0, 0)):

        # rectangle of the surface from which we will get the subsurface, parent surface
        surface_rect = surface.get_rect()

        # left top shift from parent surface
        self.left_top = tuple_prod(rel_pos.left_top, surface_rect.size)

        # size relative to parent surface size
        self.size = tuple_prod(rel_pos.size, surface_rect.size)

        # our part of the parents surface
        self.surface = surface.subsurface(pygame.Rect(*self.left_top, *self.size))

        # there can be many parents, and we need to track the shift in respect to original left_top = (0,0)
        self.screen_left_top = tuple_sum(screen_left_top, self.left_top)

        # rectangle with shift to root (screen), used for actions only
        self.screen_rect = pygame.Rect(*self.screen_left_top, *self.size)

        self.surface.fill(BACKGROUND_COLOR)
        self.rect_without_border = surface.get_rect()
        self.background_color = BACKGROUND_COLOR

    def draw(self):
        raise Exception('Pure virtual method')

    def colliding_event(self, event_pos : tuple[int, int]):
        return self.screen_rect.collidepoint(event_pos)

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