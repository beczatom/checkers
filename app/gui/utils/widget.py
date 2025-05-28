"""
This module is probably the most important in all GUI classes.
It defines the positioning of widget, provides user-friendly way to initialize widgets,
also takes care of basic interface to interact with various widgets.
"""

from abc import abstractmethod

import pygame

from app.gui.constants import BACKGROUND_COLOR, BORDER_COLOR, FIRST_BORDER_WIDTH, BORDER_GAP, \
    SECOND_BORDER_WIDTH
from app.gui.utils.pos import Pos
from app.helper import tuple_prod, tuple_sum


class Widget:
    """
    This class represents a parent class to all the widgets.
    """

    def __init__(self, surface: pygame.Surface, rel_pos: Pos, screen_left_top: tuple[int, int] = (0, 0)):
        """
        Initializes the widget.
        Parameters
        ----------
        surface : pygame.Surface
            The surface from where we will take our drawing area.
        rel_pos : Pos
            The position and size of the widget relative to the screen.
        screen_left_top : tuple[int, int]
            Very important!
            The widgets somehow shifted from original screen startpoint (0, 0)
            can also have "child" widgets in a meaning they can create them
            and let them print to their surface.
            So it is absolutely crucial to know the shift to the origin of the screen,
            because otherwise we wouldn't know if the event happened inside our rectangle.
        """
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

    @abstractmethod
    def draw(self) -> None:
        """
        Abstract method to draw the widget.

        Raises
        ------
        error : NotImplementedError
            If the child doesn't implement this method.
        """
        raise NotImplementedError()

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """
        Abstract method to handle event.

        Parameters
        ----------
        event : pygame.event.Event
            The event to handle.

        Raises
        ------
        error : NotImplementedError
            If the child doesn't implement this method.
        """
        raise NotImplementedError()

    def draw_one_border(self, rect: pygame.Rect, border_width: int, border_gap: int) -> None:
        """
        Draws one border around the widget.
        Parameters
        ----------
        rect : pygame.Rect
            The original rectangle to which we draw the border (inside).
        border_width : int
            The border width.
        border_gap : int
            The gap from border (of the inside rectangle).
        """
        pygame.draw.rect(self.surface, BORDER_COLOR, rect)
        rect = pygame.Rect(rect.x + border_width, rect.y + border_width,
                           rect.width - 2 * border_width, rect.height - 2 * border_width)
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, rect)
        self.rect_without_border = pygame.Rect(rect.x + border_gap, rect.y + border_gap,
                                               rect.width - 2 * border_gap, rect.height - 2 * border_gap)

    def draw_borders(self) -> None:
        """
        Draws borders around the widget.
        """
        self.draw_one_border(self.surface.get_rect(), FIRST_BORDER_WIDTH, BORDER_GAP)
        self.draw_one_border(self.rect_without_border, SECOND_BORDER_WIDTH, 0)
        pygame.draw.rect(self.surface, self.background_color, self.rect_without_border)

    def get_height(self):
        """
        Gets height of the widget.
        Returns
        -------
        height : int
            The height of the widget.
        """
        return self.surface.get_height()

    def get_width(self):
        """
        Gets width of the widget.
        Returns
        -------
        width : int
            The width of the widget.
        """
        return self.surface.get_width()
