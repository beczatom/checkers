"""
This module defines a widget for game result.
"""

import pygame

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.utils.button import Button
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.constants import DEFAULT_FONT_SIZE, WIN_TEXT, GAME_END_TYPE_TEXT, OK_TEXT
from checkers_sem.gui.utils.pos import Pos


class Result(Widget):
    """
    This class defines a widget for game result.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the result widget.
        Parameters
        ----------
        args
            for parent
        kwargs
            for this child
        """
        super().__init__(*args)

        self.draw_borders()

        self.res, self.game_end_type = kwargs.get('res')
        self.onclick = kwargs.get('onclick', None)

        self.init_res_text()
        self.init_game_end_type_text()

        self.ok_button = self.init_ok_button()

    def init_res_text(self) -> None:
        """
        Initialize the result text.
        """
        text = WIN_TEXT[self.res]

        Text(self.surface,
             Pos((0.8, 0.2), (0.15, 0, 0.65, 0), center=True),
             self.screen_left_top,
             text=text, font_size=2 * DEFAULT_FONT_SIZE).draw()

    def init_game_end_type_text(self) -> None:
        """
        Initializes the game end type text.
        """

        text = GAME_END_TYPE_TEXT[self.game_end_type]
        Text(self.surface,
             Pos((0.8, 0.2), (0.3, 0, 0.5, 0), center=True),
             self.screen_left_top,
             text=text).draw()

    def init_ok_button(self) -> Button:
        """
        Initialize the ok button.
        """
        button = Button(self.surface,
                        Pos((0.3, 0.2), (0.7, 0, 0.1, 0), center=True),
                        self.screen_left_top,
                        text=OK_TEXT, onclick=self.onclick)

        button.draw()
        return button

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles events
        Parameters
        ----------
        event : pygame.event.Event
            event to handle
        """
        self.ok_button.handle_event(event)

    def draw(self):
        pass
