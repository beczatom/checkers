from checkers_sem.gui.utils.button import Button
from checkers_sem.gui.game_setting_window import GameSettingWindow
from checkers_sem.gui.genetic_setting_window import GeneticSettingWindow
from checkers_sem.constants import BACKGROUND_COLOR, PLAY_BUTTON_TEXT, GENETIC_TEXT, REFRESH_RATE_MS
import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill(BACKGROUND_COLOR, self.screen.get_rect())
        pygame.display.flip()
        self.buttons = self.buttons_init()
        self.next_window = None

    def buttons_init(self) -> list[Button]:

        def game_onclick():
            self.next_window = GameSettingWindow(self.screen)

        def genetic_onclick():
            self.next_window = GeneticSettingWindow(self.screen)

        actions = [game_onclick, genetic_onclick]

        buttons = []

        margin_x = self.screen.get_width() // 8
        margin_y_up =  self.screen.get_height() // 2
        padding_y = self.screen.get_height() // 24

        button_width = (self.screen.get_width() - 2 * margin_x)
        button_height = (self.screen.get_height() - margin_y_up - padding_y) // 4

        for i, text in enumerate([PLAY_BUTTON_TEXT, GENETIC_TEXT]):
            top = margin_y_up + i * button_height + i * padding_y
            left = margin_x

            rect = pygame.Rect(left, top, button_width,button_height)

            buttons.append(Button(self.screen.subsurface(rect), (left, top), text, actions[i],
                                  background_color=BACKGROUND_COLOR, first_border=True, second_border=True, font_size= 25))

            buttons[-1].draw()

        return buttons

    def show(self):
        while True:
            while self.next_window is None:
                pygame.time.delay(REFRESH_RATE_MS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                    for button in self.buttons:
                        button.handle_event(event)

                pygame.display.update()

            self.screen.fill(BACKGROUND_COLOR)
            pygame.display.flip()
            try:
                self.next_window.show()
                self.__init__(self.screen)
            except StopIteration:
                break

