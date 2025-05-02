
from checkers_sem.gui.utils.window import Window
from checkers_sem.gui.utils.button import Button

from checkers_sem.gui.game_setting_widget import GameSettingWidget
from checkers_sem.gui.game_setting_ai_vs_ai import GameSettingAIVSAI
from checkers_sem.gui.game_setting_human_vs_human import GameSettingHumanVSHuman
from checkers_sem.gui.game_setting_human_vs_ai import GameSettingHumanVSAI

from checkers_sem.helper import *

import pygame

class GameSettingWindow(Window):
    def __init__(self, surface):
        super().__init__(surface)
        self.start = False
        self.option_widget = self.option_widget_init(GameSettingHumanVSHuman)
        self.mode_buttons = self.buttons_init()
        self.start_button = self.init_start_button()

    def start_button_onclick(self):
        self.option_widget.start_game(self.surface)

    def init_start_button(self):
        margin_x = 6 * self.surface.get_rect().width // 8

        space_y = self.surface.get_rect().height - self.option_widget.get_screen_bottom()
        margin_y = self.option_widget.get_screen_bottom() + space_y // 4
        size_y = space_y // 2
        size_x = margin_x // 6

        button_rect = pygame.Rect(margin_x, margin_y, size_x, size_y)

        button = Button(self.surface.subsurface(button_rect), (margin_x, margin_y),
                        START_TRAIN_BUTTON_TEXT, self.start_button_onclick)
        button.draw()
        return button

    def option_widget_init(self, option_widget_constructor : type) -> GameSettingWidget:
        margin_top = 8 * self.surface.get_height() // 32
        margin_bottom = self.surface.get_height() // 8
        margin_left = self.surface.get_width() // 8

        size_x = self.surface.get_width() - 2 * margin_left
        size_y = self.surface.get_height() - margin_top - margin_bottom

        option_widget_rect = pygame.Rect(margin_left, margin_top, size_x, size_y)
        option_widget = option_widget_constructor(self.surface.subsurface(option_widget_rect), (margin_left, margin_top))
        option_widget.draw()
        return option_widget

    def buttons_init(self) -> list[Button]:

        def human_vs_human():
            self.option_widget = self.option_widget_init(GameSettingHumanVSHuman)
        def human_vs_pc():
            self.option_widget = self.option_widget_init(GameSettingHumanVSAI)
        def pc_vs_pc():
            self.option_widget = self.option_widget_init(GameSettingAIVSAI)

        actions = [human_vs_human, human_vs_pc, pc_vs_pc]

        buttons = []

        left = self.surface.get_width() // 8
        margin_y_up =  self.surface.get_height() // 6
        padding_x = self.surface.get_width() // 24

        button_width = (self.surface.get_width() - 2 * left - 2 * padding_x) // 3
        button_height = self.surface.get_height() // 12

        for i, text in enumerate([HUMAN_VS_HUMAN_TEXT, HUMAN_VS_PC_TEXT, PC_VS_PC_TEXT]):
            top = margin_y_up

            rect = pygame.Rect(left, top, button_width, button_height)

            buttons.append(Button(self.surface.subsurface(rect), (left, top), text, actions[i],
                                  background_color=BACKGROUND_COLOR, first_border=True, second_border=True, font_size= 15))

            buttons[-1].draw()
            left += button_width + padding_x

        return buttons

    def handle_event(self, event : pygame.event.Event):
        super().handle_event(event)

        for button in self.mode_buttons:
            button.handle_event(event)
        self.option_widget.handle_event(event)
        self.start_button.handle_event(event)

    def refresh(self):
        for button in self.mode_buttons:
            button.draw()

        self.option_widget.draw()
        self.start_button.draw()