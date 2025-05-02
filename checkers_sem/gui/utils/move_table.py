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
        self.row_height = 3 * DEFAULT_FONT_SIZE // 2
        self.move_texts = []
        self.offset_top = 0
        self.max_offset_top = 0

        self.printed_indexes = None

    def set_move_texts(self, moves : list[Move]):
        self.move_texts = [str(i + 1) + '. ' + move_to_display_string(move) for i, move in enumerate(moves)]
        self.max_offset_top = (len(self.move_texts) + 1) * self.row_height - self.rect_without_border.height
        self.max_offset_top = max(self.max_offset_top, 0)
        if self.offset_top > self.max_offset_top:
            self.offset_top = self.max_offset_top
        self.draw()

    def handle_event(self, event : pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.screen_rect.collidepoint(event.pos):
            if event.button == 4: # scroll up
                self.offset_top -= self.row_height

                if self.offset_top <= 0:
                    self.offset_top = 0


            if event.button == 5: # scroll down
                self.offset_top += self.row_height
                if self.offset_top > self.max_offset_top:
                    self.offset_top = self.max_offset_top

            self.draw()

    def clear_indexes(self):
        self.printed_indexes = None

    def draw(self):


        start_idx = self.offset_top // self.row_height
        end_idx = min(start_idx + self.rect_without_border.height // self.row_height, len(self.move_texts))

        if self.printed_indexes == (start_idx, end_idx):
            return

        self.printed_indexes = (start_idx, end_idx)

        self.draw_border()
        self.surface.fill(BACKGROUND_COLOR, self.rect_without_border)



        top, left = self.rect_without_border.topleft
        size_x = self.rect_without_border.width

        for move_text in self.move_texts[start_idx : end_idx]:
            text_rect = pygame.Rect(left, top, size_x, self.row_height)
            Text(self.surface.subsurface(text_rect),
                 tuple_sum(self.screen_left_top, (left, top)),
                 move_text, font_size = 4 * DEFAULT_FONT_SIZE // 5).draw()
            top += self.row_height