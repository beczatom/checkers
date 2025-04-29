import pygame

from checkers_sem.game.move import Move
from checkers_sem.gui.utils.widget import *
from checkers_sem.gui.utils.text import Text
from checkers_sem.helper import *

class MoveTable(Widget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int]):
        super().__init__(surface, left_top)

        self.draw_border()

        self.font = pygame.font.Font(DEFAULT_FONT, 4 * DEFAULT_FONT_SIZE // 5)
        self.row_height = DEFAULT_FONT_SIZE
        self.row_padding_top = DEFAULT_FONT_SIZE // 2
        self.move_texts = []
        self.offset_top = 0
        self.printing_rect_height = 0

    def set_move_texts(self, moves : list[Move]):
        self.move_texts = [str(i + 1) + '. ' + move_to_display_string(move) for i, move in enumerate(moves)]
        self.draw()

    def handle_event(self, event : pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.screen_rect.collidepoint(event.pos):
            if event.button == 4: # scroll up
                self.offset_top -= 10

                if self.offset_top < 0:
                    self.offset_top = 0


            if event.button == 5: # scroll down
                self.offset_top += 10
                if self.offset_top > self.printing_rect_height - self.rect_without_border.height:
                    self.offset_top = self.printing_rect_height - self.rect_without_border.height

            self.draw()

    def draw(self):
        self.draw_border()
        self.surface.fill(BACKGROUND_COLOR, self.rect_without_border)

        long_surface = pygame.Surface((self.rect_without_border.width, 10000))
        long_surface.fill(BACKGROUND_COLOR)

        top, left = self.rect_without_border.topleft[0], 0
        size_x = self.rect_without_border.width

        for move_text in self.move_texts:
            top += self.row_padding_top
            text_rect = pygame.Rect(left, top, size_x, self.row_height)
            Text(long_surface.subsurface(text_rect),
                 tuple_sum(self.screen_left_top, (left, top)),
                 move_text, font_size = 4 * DEFAULT_FONT_SIZE // 5).draw()
            top += self.row_height

        self.printing_rect_height = top

        to_show_rect = self.rect_without_border.copy()
        to_show_rect.top += self.offset_top
        self.surface.blit(long_surface, self.rect_without_border, area=to_show_rect)