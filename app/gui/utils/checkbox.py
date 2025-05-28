"""
This module implements a simple checkbox.
"""

import pygame

from app.gui.constants import BACKGROUND_COLOR, CHECKED_CHECKBOX_BACKGROUND
from app.gui.utils.widget import Widget


class CheckBox(Widget):
    """
    This class implements a simple checkbox.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the checkbox.
        Parameters
        ----------
        args
            to initialize the parent.
        kwargs
            to initialize this child.
        """
        super().__init__(*args)

        self.draw_borders()
        self.background_color = BACKGROUND_COLOR
        self.is_hovered = False
        self.is_checked = False

        self.on_uncheck = kwargs.get('on_uncheck', None)
        self.on_check = kwargs.get('on_check', None)

    def set_value(self, value: bool) -> None:
        """
        Sets if the checkbox is checked.
        Parameters
        ----------
        value : bool
            is the checkbox checked?
        """
        self.is_checked = value

    def get_value(self) -> bool:
        """
        Gets the checkbox value.
        Returns
        -------
        checked : bool
            if the checkbox is checked.
        """
        return self.is_checked

    def hover(self) -> None:
        """
        Does action when the checkbox is hovered.
        """
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # pylint: disable=no-member

    def unhover(self) -> None:
        """
        Does action when the checkbox is unhovered.
        """
        self.is_hovered = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # pylint: disable=no-member

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles the event.
        Parameters
        ----------
        event : pygame.event.Event
            the event that occurred
        """
        if event.type == pygame.MOUSEMOTION:    # pylint: disable=no-member
            if self.screen_rect.collidepoint(event.pos):
                self.hover()
                self.draw()
                self.is_hovered = True
            else:
                if self.is_hovered:
                    self.unhover()
                    self.draw()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # pylint: disable=no-member
            if self.screen_rect.collidepoint(event.pos):
                self.is_checked = not self.is_checked
                if self.is_checked and self.on_check is not None:
                    self.on_check()
                elif not self.is_checked and self.on_uncheck is not None:
                    self.on_uncheck()
                self.draw()

    def draw(self) -> None:
        """
        Draws the checkbox.
        """
        self.draw_borders()
        if self.is_checked:
            image = CHECKED_CHECKBOX_BACKGROUND
            image = pygame.image.load(image).convert_alpha()
            image = pygame.transform.scale(image, self.rect_without_border.size)
            self.surface.blit(image, self.rect_without_border.topleft)
