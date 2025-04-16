from checkers_sem.constants import *
from checkers_sem.gui.utils.button import Button
import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen

    @property
    def buttons_init(self) -> list[Button]:
        buttons = []
        for i, text in enumerate([HUMAN_VS_HUMAN_TEXT, HUMAN_VS_PC_TEXT, PC_VS_PC_TEXT]):
            rect_center_y = SCREEN_HEIGHT // 2
            padding_x = SCREEN_WIDTH // 8
            rect_center_x = 2 * padding_x + i * (SCREEN_WIDTH - 2 * padding_x) // 3

            between_padding_x = SCREEN_WIDTH // 16

            button_width = (SCREEN_WIDTH - 2 * padding_x - between_padding_x) // 3
            button_height = SCREEN_HEIGHT // 4

            rect = pygame.Rect(rect_center_x - button_width // 2, rect_center_y - button_height // 2, button_width,
                               button_height)
            buttons.append(Button(self.screen, rect, text, (0, 0, 255), 30))
            buttons[-1].draw()

        return buttons


    def show(self) -> GameType:
        buttons = self.buttons_init

        run = True
        clicked = False
        option = 0

        while run and option == 0:
            pygame.time.delay(100)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True

            if clicked:
                for i, button in enumerate(buttons):
                    if button.clicked(mouse_pos):
                       option = i + 1

            pygame.display.update()

        return option
