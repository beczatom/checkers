from checkers_sem.gui.utils.button import Button
from checkers_sem.gui.game_setting.game_setting_window import GameSettingWindow
from checkers_sem.gui.genetic_window.genetic_setting_window import GeneticSettingWindow
from checkers_sem.gui.constants import BACKGROUND_COLOR, PLAY_BUTTON_TEXT, GENETIC_TEXT, REFRESH_RATE_MS
import pygame

from checkers_sem.gui.utils.pos import Pos

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

        for i, text in enumerate([PLAY_BUTTON_TEXT, GENETIC_TEXT]):

            buttons.append(Button(self.screen,
                                  Pos((0.6, 0.1), (i * 0.3, 0, 0, 0), center=True),
                                  text=text, onclick=actions[i],background_color=BACKGROUND_COLOR,
                                  first_border=True, second_border=True, font_size= 25))

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
