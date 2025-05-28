"""
This module implements a simple button and an image button.
"""

import pygame

from app.gui.utils.widget import Widget
from app.gui.utils.loader import loader
from app.gui.constants import (DEFAULT_FONT_SIZE, DEFAULT_FONT, BACKGROUND_COLOR, TEXT_COLOR, HOVER_TEXT_COLOR,
                               HOVER_BACKGROUND_COLOR)

class Button(Widget):
    """
    This class implements a simple button.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the button.
        Raises
        ------
        error : AttributeError
            if second border is defined but first not
        Parameters
        ----------
        args
            for constructing parent
        kwargs
            for constructing this child
        """
        super().__init__(*args)

        # borders
        self.draw_borders()

        # text
        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)
        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)
        self.text = kwargs.get('text', '')
        self.text_color = TEXT_COLOR

        # action
        self.onclick = kwargs.get('onclick', None)
        self.is_hovered = False

        self.background_color = BACKGROUND_COLOR

    def hover(self) -> None:
        """
        Actions to do when the button is hovered.
        """

        self.background_color = HOVER_BACKGROUND_COLOR
        self.text_color = HOVER_TEXT_COLOR
        self.is_hovered = True
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # pylint: disable=no-member

    def unhover(self) -> None:
        """
        Actions to do when the button is unhovered.
        """
        self.background_color = BACKGROUND_COLOR
        self.text_color = TEXT_COLOR
        self.is_hovered = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # pylint: disable=no-member

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            event occurred
        """
        if event.type == pygame.MOUSEMOTION:    # pylint: disable=no-member
            if self.screen_rect.collidepoint(event.pos):
                self.hover()
                self.draw()
            else:
                if self.is_hovered:
                    self.unhover()
                    self.draw()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # pylint: disable=no-member
            if self.screen_rect.collidepoint(event.pos):
                self.onclick()

    def draw(self) -> None:
        """
        Draws the button.
        """
        self.draw_borders()

        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)


class ImageButton(Widget):
    """
    This class implements an image button, where there is no text only an image.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the button.
        Parameters
        ----------
        args
            for constructing parent
        kwargs
            for constructing this child
        """
        super().__init__(*args)
        self.onclick = kwargs.get('onclick', None)

        self.background_image = kwargs.get('background_image', '')
        self.background_image = loader.LOADED_IMAGES[self.background_image]
        self.background_image = pygame.transform.scale(self.background_image, self.surface.get_rect().size)

        self.is_hovered = False

    def set_background_image(self, name: str) -> None:
        """
        Sets the background image.
        Parameters
        ----------
        name : string
            name of the background image
        """
        self.background_image = loader.LOADED_IMAGES[name]
        self.background_image = pygame.transform.scale(self.background_image, self.surface.get_rect().size)

    def draw(self) -> None:
        """
        Draws the button.
        """
        self.surface.fill(BACKGROUND_COLOR)
        self.surface.blit(self.background_image, self.surface.get_rect().topleft)

    def handle_event(self, event: pygame.event.Event):
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            event occurred
        """
        if event.type == pygame.MOUSEMOTION:    # pylint: disable=no-member
            if self.screen_rect.collidepoint(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # pylint: disable=no-member
                self.is_hovered = True
            else:
                if self.is_hovered:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # pylint: disable=no-member
                    self.is_hovered = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                and self.screen_rect.collidepoint(event.pos):   # pylint: disable=no-member
            self.onclick()
