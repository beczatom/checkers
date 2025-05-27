"""
This module implements a chessboard timer.
"""

import time

import pygame


from checkers_sem.gui.utils.widget import Widget
from checkers_sem.helper import seconds_to_string
from checkers_sem.gui.constants import DEFAULT_FONT, DEFAULT_FONT_SIZE, TEXT_COLOR
from checkers_sem.state import state


class Timer(Widget):
    """
    This class implements a chessboard timer.
    """

    def __init__(self, *args):
        """
        Initializes the timer.
        Parameters
        ----------
        args
            for parent class
        """
        super().__init__(*args)
        self.draw_borders()
        self.font = pygame.font.Font(DEFAULT_FONT, DEFAULT_FONT_SIZE)

        self.time_left = state.TIME
        self.last_start = None
        self.time_going = False

    def time_start(self) -> None:
        """
        Starts the timer.
        """
        if self.time_going:
            return
        self.last_start = time.time()
        self.time_going = True

    def time_stop(self) -> None:
        """
        Stops the timer.
        """
        if not self.time_going:
            return
        self.time_left = self.get_time_left()
        self.last_start = None
        self.time_going = False

    def get_time_left(self) -> float:
        """
        Gets the time left.
        Returns
        -------
        time : float
            The time left in seconds.
        """
        if self.last_start is None:
            return self.time_left
        return max(0, self.time_left - (time.time() - self.last_start) if self.last_start else self.time_left)

    def time_is_over(self) -> bool:
        """
        Checks if the time is over.
        Returns
        -------
        is_over : bool
            whether the time is over or not.
        """
        return self.get_time_left() == 0

    def draw(self) -> None:
        """
        Draws timer on the screen.
        """
        self.draw_borders()
        text = self.font.render(seconds_to_string(self.get_time_left()), True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)

    def handle_event(self, event : pygame.event) -> None:
        """
        Does nothing.
        Parameters
        ----------
        event : pygame.event.Event
            event occurred
        """
