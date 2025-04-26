from checkers_sem.constants import *
from checkers_sem.gui.utils.button import Button
import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill(BACKGROUND_COLOR)
        self.buttons = self.buttons_init()

    def buttons_init(self) -> list[Button]:
        buttons = []

        margin_x = SCREEN_WIDTH // 8
        margin_y_up = 3 * SCREEN_HEIGHT // 5
        padding_y = SCREEN_HEIGHT // 16

        button_width = (SCREEN_WIDTH - 2 * margin_x)
        button_height = (SCREEN_HEIGHT - margin_y_up - 2 * padding_y) // 3

        for i, text in enumerate([HUMAN_VS_HUMAN_TEXT, HUMAN_VS_PC_TEXT, PC_VS_PC_TEXT]):
            rect_center_x = SCREEN_WIDTH // 2
            rect_center_y = margin_y_up + i * button_height + i * padding_y

            rect = pygame.Rect(rect_center_x - button_width // 2, rect_center_y - button_height // 2, button_width,
                               button_height)

            buttons.append(Button(self.screen, rect, text, background_color=BACKGROUND_COLOR,
                                  first_border=True, second_border=True, font_size= 25))
            buttons[-1].draw(pygame.mouse.get_pos())

        return buttons

    def show(self) -> GameType:
        run = True
        option = 0

        while run and option == 0:
            pygame.time.delay(10)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button.draw(mouse_pos)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, button in enumerate(self.buttons):
                        if button.clicked(mouse_pos):
                            option = i + 1

            pygame.display.update()

        return option
