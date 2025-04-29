from checkers_sem.constants import *
from checkers_sem.gui.utils.button import Button
from checkers_sem.gui.game_window import GameWindow
from checkers_sem.gui.genetic_setting_window import GeneticSettingWindow
from checkers_sem.player.player import *
import pygame
from checkers_sem.gui.utils.checkbox import CheckBox


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill(BACKGROUND_COLOR)
        self.buttons = self.buttons_init()
        self.next_window = None
        self.checkbox = self.checkbox_init()

    def checkbox_init(self) -> CheckBox:
        left = self.screen.get_width() // 8
        top = self.screen.get_height() // 8
        checkbox_rect = pygame.Rect(left, top, 40, 40)
        checkbox = CheckBox(self.screen.subsurface(checkbox_rect), (left, top))

        return checkbox

    def buttons_init(self) -> list[Button]:

        def human_vs_human():
            self.next_window = GameWindow(self.screen, (HumanPlayer(), HumanPlayer()))

        def human_vs_pc():
            self.next_window = GameWindow(self.screen, (HumanPlayer(), AIPlayer()))

        def pc_vs_pc():
            self.next_window = GameWindow(self.screen, (AIPlayer(), AIPlayer()))

        def genetic():
            self.next_window = GeneticSettingWindow(self.screen)

        actions = [human_vs_human, human_vs_pc, pc_vs_pc, genetic]

        buttons = []

        margin_x = self.screen.get_width() // 8
        margin_y_up =  self.screen.get_height() // 2
        padding_y = self.screen.get_height() // 24

        button_width = (self.screen.get_width() - 2 * margin_x)
        button_height = (self.screen.get_height() - margin_y_up - 3 * padding_y) // 4

        for i, text in enumerate([HUMAN_VS_HUMAN_TEXT, HUMAN_VS_PC_TEXT, PC_VS_PC_TEXT, GENETIC_TEXT]):
            top = margin_y_up + i * button_height + i * padding_y
            left = margin_x

            rect = pygame.Rect(left, top, button_width,button_height)

            buttons.append(Button(self.screen.subsurface(rect), (left, top), text, actions[i],
                                  background_color=BACKGROUND_COLOR, first_border=True, second_border=True, font_size= 25))

            buttons[-1].draw()

        return buttons

    def show(self):
        while self.next_window is None:
            pygame.time.delay(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                for button in self.buttons:
                    button.handle_event(event)

                self.checkbox.handle_event(event)

            pygame.display.update()

        self.next_window.show()

