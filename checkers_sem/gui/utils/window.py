"""
This module defines Window.
Pretty much like Widget, but doesn't have any offset.
Also here is the main cycle for event checking and drawing for a particular window.
"""

from abc import abstractmethod

import pygame

from checkers_sem.gui.constants import BACKGROUND_COLOR, LEFT_ARROW_IMAGE, REFRESH_RATE_MS
from checkers_sem.gui.utils.button import ImageButton
from checkers_sem.gui.utils.pos import Pos


class Window:
    """
    Defines parent class for all windows.
    """

    def __init__(self, surface: pygame.surface):
        """
        Initializes the window.
        Parameters
        ----------
        surface : pygame.surface
            area we will print on, needs to be in size of application.
        """
        self.surface = surface
        self.surface.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        self.run = True
        self.menu_button = self.init_menu_button()

        self.active_thread = None

    def init_menu_button(self) -> ImageButton:
        """
        Initializes the menu button.
        Returns
        -------
        menu_button: ImageButton
            The menu button on top left.
        """

        def menu_button_onclick():
            if self.active_thread is not None:
                self.active_thread.join()
            self.run = False

        menu_button = ImageButton(self.surface,
                                  Pos((0.05, 0.05), (0.025, 0, 0, 0.025)),
                                  background_image=LEFT_ARROW_IMAGE, onclick=menu_button_onclick)
        menu_button.draw()
        return menu_button

    def handle_event(self, event: pygame.event.Event):
        """
        Handles events.
        The children always calls this method,
        which only check if quit happened and back button was pressed.
        Parameters
        ----------
        event : pygame.event.Event
            event to handle
        """
        if event.type == pygame.QUIT: # pylint: disable=no-member
            raise StopIteration()
        self.menu_button.handle_event(event)

    @abstractmethod
    def refresh(self) -> None:
        """
        Abstract method to refresh the window,
        the particular windows can define their logic here
        """
        raise NotImplementedError()

    def show(self) -> None:
        """
        Main cycle of the GUI.
        """

        while self.run:
            pygame.time.delay(REFRESH_RATE_MS)

            self.menu_button.draw()

            for event in pygame.event.get():
                self.handle_event(event)

            if self.run:
                self.refresh()

            pygame.display.update()

        self.surface.fill(BACKGROUND_COLOR)
