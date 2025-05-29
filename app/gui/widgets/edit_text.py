"""
This module implements a simple edit text.
"""

import pygame

from app.gui.widgets.widget import Widget
from app.gui.constants import (DEFAULT_FONT, FIRST_BORDER_WIDTH, BACKGROUND_COLOR, BORDER_GAP,
                               DEFAULT_TEXT_COLOR,
                               DEFAULT_FONT_SIZE)


class EditText(Widget):
    """
    This class implements a simple edit text.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the edit text.
        Parameters
        ----------
        args
            what needs to be passed to parent class
        kwargs
            what will be used in this class
        """
        super().__init__(*args)

        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)
        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)
        self.text = str(kwargs.get('text', ''))

        self.editing = False

    def set_string(self, text: str | int | float) -> None:
        """
        Sets value to display
        Parameters
        ----------
        text : str | int | float
            to display
        """
        self.text = str(text)

    def get_string(self) -> str:
        """
        Returns displayed value.
        Returns
        -------
        displayed_value : str
            the displayed value
        """
        return self.text

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles event.
        Parameters
        ----------
        event : pygame.event.Event
            event to handle
        """

        # click -> editing | clicked away -> not editing
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # pylint: disable=no-member
            self.editing = self.screen_rect.collidepoint(event.pos)

        # change the value if editing
        if event.type == pygame.KEYDOWN and self.editing:   # pylint: disable=no-member
            if event.key == pygame.K_BACKSPACE and len(self.text) > 0:  # pylint: disable=no-member
                self.text = self.text[:-1]

            if event.unicode.isdigit():
                self.text = self.text + str(event.unicode)

            if len(self.text) < 2:
                self.text = '0.'

            if len(self.text) > 5:
                self.text = self.text[:5]

            self.draw()

    def draw(self) -> None:
        """
        Draws the edit text.
        """
        self.draw_one_border(self.surface.get_rect(), FIRST_BORDER_WIDTH, BORDER_GAP)
        self.surface.fill(BACKGROUND_COLOR, self.rect_without_border)
        text = self.font.render(self.text, True, DEFAULT_TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect_without_border.center)
        self.surface.blit(text, text_rect)
