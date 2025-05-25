"""
This module defines a simple text widget.
"""

import pygame

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.constants import DEFAULT_FONT, BACKGROUND_COLOR, DEFAULT_TEXT_COLOR, DEFAULT_FONT_SIZE

class Text(Widget):
    """
    This class defines a simple text widget.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the text widget.
        Parameters
        ----------
        args
            for parent class
        kwargs
            for this child class
        """
        super().__init__(*args)

        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)
        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)
        self.text = str(kwargs.get('text', ''))

    def set_text(self, text : str | int | float) -> None:
        """
        Sets the text to be displayed.
        Parameters
        ----------
        text : str | int | float
            the text to be displayed.
        """
        self.text = str(text)

    def draw(self) -> None:
        """
        Draws the text on the screen.
        """
        self.surface.fill(BACKGROUND_COLOR)
        text = self.font.render(self.text, True, DEFAULT_TEXT_COLOR)
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)

    def handle_event(self, event: pygame.event) -> None:
        """
        Does nothing.
        Parameters
        ----------
        event : pygame.event.Event
            event occurred
        """
