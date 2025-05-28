"""
This module defines the menu window
"""

import pygame

from checkers_sem.gui.utils.button import Button, ImageButton
from checkers_sem.gui.game_setting.game_setting_window import GameSettingWindow
from checkers_sem.gui.genetic_window.genetic_setting_window import GeneticSettingWindow
from checkers_sem.gui.constants import BACKGROUND_COLOR, PLAY_BUTTON_TEXT, GENETIC_TEXT, REFRESH_RATE_MS, MENU_IMAGE
from checkers_sem.gui.utils.pos import Pos

class Menu:
    """
    This class defines the menu window
    """
    def __init__(self, screen : pygame.Surface):
        """
        Initialize the menu window
        Parameters
        ----------
        screen : pygame.Surface
            The screen surface
        """
        self.screen = screen
        self.screen.fill(BACKGROUND_COLOR, self.screen.get_rect())
        pygame.display.flip()
        self.buttons = self.buttons_init()
        self.next_window = None
        self.image = self.image_init()

    def reset(self) -> None:
        """
        Reset the menu window
        """
        self.screen.fill(BACKGROUND_COLOR, self.screen.get_rect())
        pygame.display.flip()
        self.buttons = self.buttons_init()
        self.next_window = None
        self.image.draw()

    def image_init(self) -> ImageButton:
        """
        Initialize menu main image.
        """
        pos = Pos((0.35, 0.5), (0.1, 0, 0.4, 0), center=True)
        image = ImageButton(self.screen, pos, background_image=MENU_IMAGE)
        image.draw()
        return image

    def buttons_init(self) -> list[Button]:
        """
        Initialize the menu window buttons (game and genetic)
        Returns
        -------
        buttons : list[Button]
            The buttons list
        """

        # onclicks
        def game_onclick():
            self.next_window = GameSettingWindow(self.screen)

        def genetic_onclick():
            self.next_window = GeneticSettingWindow(self.screen)

        actions = [game_onclick, genetic_onclick]
        buttons = []

        for i, text in enumerate([PLAY_BUTTON_TEXT, GENETIC_TEXT]):
            buttons.append(Button(self.screen,
                                  Pos((0.6, 0.1), (0.5 + i * 0.25, 0, 0, 0), center=True),
                                  text=text, onclick=actions[i], background_color=BACKGROUND_COLOR,
                                  font_size= 25))
            buttons[-1].draw()

        return buttons

    def show(self) -> None:
        """
        Show the menu window.
        """
        while True:
            while self.next_window is None:
                pygame.time.delay(REFRESH_RATE_MS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:   # pylint: disable=no-member
                        return

                    for button in self.buttons:
                        button.handle_event(event)

                pygame.display.update()

            self.screen.fill(BACKGROUND_COLOR)
            pygame.display.flip()

            # next window cycle, till the quit is pressed,
            # or if the back button was pressed, we continue the cycle
            try:
                self.next_window.show()
                self.reset()
            except StopIteration:
                break
