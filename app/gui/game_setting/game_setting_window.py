"""
This module defines a windows responsible for game settings
"""

import pygame

from app.gui.widgets.window import Window
from app.gui.widgets.button import Button
from app.gui.game_setting.game_setting_widget import GameSettingWidget
from app.gui.game_setting.game_setting_ai_vs_ai import GameSettingAIVSAI
from app.gui.game_setting.game_setting_human_vs_human import GameSettingHumanVSHuman
from app.gui.game_setting.game_setting_human_vs_ai import GameSettingHumanVSAI
from app.gui.constants import START_TRAIN_BUTTON_TEXT, HUMAN_VS_HUMAN_TEXT, HUMAN_VS_PC_TEXT, PC_VS_PC_TEXT, \
    BACKGROUND_COLOR
from app.gui.widgets.pos import Pos


class GameSettingWindow(Window):
    """
    This class implements a UI for setting the game
    """

    def __init__(self, surface):
        """
        Initializes the game setting window
        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the window on
        """
        super().__init__(surface)
        self.start = False
        self.option_widget = self.option_widget_init(GameSettingHumanVSHuman)
        self.mode_buttons = self.buttons_init()
        self.start_button = self.init_start_button()

    def start_button_onclick(self) -> None:
        """
        Defines game start button click event
        """
        self.option_widget.start_game(self.surface)

    def init_start_button(self) -> Button:
        """
        Initializes game start button
        """
        button = Button(self.surface,
                        Pos((0.125, 0.075), (0.85, 0.05, 0, 0.8), center=True),
                        text=START_TRAIN_BUTTON_TEXT, onclick=self.start_button_onclick)
        button.draw()
        return button

    def option_widget_init(self, option_widget_constructor: type) -> GameSettingWidget:
        """
        Constructs option widget object. Each mode has other widgets.
        Parameters
        ----------
        option_widget_constructor : type
            The constructor for the option widget

        Returns
        -------
        game_setting_widget : GameSettingWidget
            the instance of the option widget
        """
        option_widget = option_widget_constructor(self.surface,
                                                  Pos((0.9, 0.7), (0.15, 0, 0.05, 0), center=True))
        option_widget.draw()
        return option_widget

    def buttons_init(self) -> list[Button]:
        """
        Initializes the buttons list for modes of the desired game.
        Returns
        -------
        modes_buttons : list[Button]
            buttons for modes of the desired game
        """

        # onclicks
        def human_vs_human():
            self.option_widget = self.option_widget_init(GameSettingHumanVSHuman)

        def human_vs_pc():
            self.option_widget = self.option_widget_init(GameSettingHumanVSAI)

        def pc_vs_pc():
            self.option_widget = self.option_widget_init(GameSettingAIVSAI)

        actions = [human_vs_human, human_vs_pc, pc_vs_pc]
        buttons = []

        for i, text in enumerate([HUMAN_VS_HUMAN_TEXT, HUMAN_VS_PC_TEXT, PC_VS_PC_TEXT]):
            buttons.append(Button(self.surface,
                                  Pos((0.2, 0.1), (0.05, 0.6 - i * 0.25, 0.85, 0.1 + i * 0.25), center=True),
                                  text=text, onclick=actions[i],
                                  background_color=BACKGROUND_COLOR, font_size=15))

            buttons[-1].draw()

        return buttons

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            The event to handle
        """
        super().handle_event(event)

        for button in self.mode_buttons:
            button.handle_event(event)
        self.option_widget.handle_event(event)
        self.start_button.handle_event(event)

    def refresh(self) -> None:
        """
        Redraws the window
        """
        for button in self.mode_buttons:
            button.draw()

        self.option_widget.draw()
        self.start_button.draw()
