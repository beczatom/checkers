"""
This module implements a simple progress bar.
"""

from typing import Any

import pygame

from app.gui.constants import BACKGROUND_COLOR, BAR_IMAGE
from app.gui.utils.widget import Widget


class ProgressBar(Widget):
    """
    Simple progress bar.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """
        Initialize bar.
        Parameters
        ----------
        args : Any
            Area of the bar (surface and pos)
        kwargs : Any
            possible value to represent
        """
        super().__init__(*args)
        self.value = kwargs.get('value', 0)
        self.draw_borders()
        self.background_color = BACKGROUND_COLOR
        self.bar_image = BAR_IMAGE
        self.bar_image = pygame.image.load(BAR_IMAGE).convert_alpha()

    def set_value(self, value: float) -> None:
        """
        Sets the bar value.
        Parameters
        ----------
        value : float
            from 0 to 1
        """
        self.value = value

    def draw(self) -> None:
        """
        Draws the bar.
        """
        self.draw_borders()
        top, left = self.rect_without_border.topleft
        size_y = self.rect_without_border.height
        size_x = int(self.rect_without_border.width * self.value)
        img_rect = pygame.Rect(left, top, size_x, size_y)
        self.surface.blit(self.bar_image, img_rect, area=img_rect)

    def handle_event(self, event: pygame.event) -> None:
        """
        Does nothing.
        Parameters
        ----------
        event : pygame.event.Event
            event occurred
        """
