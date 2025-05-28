"""
This module defines a simple slider.
"""

import pygame

from app.gui.utils.widget import Widget
from app.gui.utils.loader import loader
from app.helper import tuple_sum
from app.gui.constants import BORDER_COLOR, BACKGROUND_COLOR, SLIDER_CIRCLE


class Slider(Widget):
    """
    This class defines a simple slider.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the slider.
        Parameters
        ----------
        args
            for parent class
        kwargs
            for this child class
        """
        super().__init__(*args)

        self.min = kwargs.get('min', 0)
        self.max = kwargs.get('max', 100)
        self.value = kwargs.get('initial', 50)
        self.onchange = kwargs.get('onchange', None)

        self.circle_rect = self.get_circle_rect()

        self.mouse_drag = False

    def handle_event(self, event: pygame.event.Event):
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            event to handle
        """

        # was clicked on circle? -> drag
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # pylint: disable=no-member
            left_top = tuple_sum(self.screen_left_top, (self.circle_rect.x, self.circle_rect.y))
            circle_screen_rect = pygame.Rect(*left_top, *self.circle_rect.size)
            if circle_screen_rect.collidepoint(event.pos):
                self.mouse_drag = True

        # dragging
        if event.type == pygame.MOUSEMOTION and self.mouse_drag:    # pylint: disable=no-member
            pos_x = event.pos[0]
            pos_on_line = pos_x - self.screen_left_top[0] - self.circle_rect.width // 2

            pos_on_line = max(0, pos_on_line)
            pos_on_line = min(pos_on_line, self.surface.get_width() - self.circle_rect.width)

            self.value = int(
                (pos_on_line / (self.surface.get_width() - self.circle_rect.width)) * (self.max - self.min) + self.min)
            self.onchange(self.value)
            self.draw()

        # stop dragging
        if event.type == pygame.MOUSEBUTTONUP:  # pylint: disable=no-member
            self.mouse_drag = False

    def get_circle_rect(self) -> pygame.Rect:
        """
        Computes the circle rectangle in respect to value.
        Returns
        -------
        circle_rect : pygame.Rect
            the desired circle rectangle.
        """

        line_width = self.get_height() // 8
        top = self.get_height() // 2 - line_width // 2
        circle_size = 3 * self.get_height() // 5
        circle_left = (self.value - self.min) / (self.max - self.min) * (self.screen_rect.width - circle_size)
        circle_top = top - circle_size // 2

        return pygame.Rect(circle_left, circle_top, circle_size, circle_size)

    def draw(self) -> None:
        """
        Draws the slider.
        """
        self.surface.fill(BACKGROUND_COLOR)

        # line
        line_width = self.get_height() // 8
        top = self.get_height() // 2 - line_width // 2
        line_rect = pygame.Rect(0, top, self.surface.get_width(), line_width)
        pygame.draw.rect(self.surface, BORDER_COLOR, line_rect)

        # circle
        self.circle_rect = self.get_circle_rect()
        circle = loader.LOADED_IMAGES[SLIDER_CIRCLE]
        circle = pygame.transform.scale(circle, self.circle_rect.size)
        self.surface.blit(circle, self.circle_rect)

    def get_value(self) -> int:
        """
        Gets the current value.
        Returns
        -------
        value : int
            the current value.
        """
        return int(self.value)
