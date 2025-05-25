"""
This module implements a move table.
"""

import pygame

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.constants import DEFAULT_FONT_SIZE, DEFAULT_FONT, BACKGROUND_COLOR
from checkers_sem.game.move import Move
from checkers_sem.helper import move_to_display_string
from checkers_sem.gui.utils.pos import Pos


class MoveTable(Widget):
    """
    This class implements a move table.
    It is a scrollable widget that displays a list of moves.
    """

    def __init__(self, *args):
        """
        Initializes the moves table.
        Parameters
        ----------
        args
            that need to be passed to parent class
        """
        super().__init__(*args)

        self.draw_borders()

        self.font = pygame.font.Font(DEFAULT_FONT, 4 * DEFAULT_FONT_SIZE // 5)
        self.row_height = 0.1
        self.move_texts = []
        self.start_idx = 0
        self.end_idx = 0
        self.printed_indexes = None

    def set_move_texts(self, moves: list[Move]) -> None:
        """
        Converts a list of moves to string representation and saves them.
        Parameters
        ----------
        moves : list[Move]
            list of moves to display
        """
        self.move_texts = [str(i + 1) + '. ' + move_to_display_string(move) for i, move in enumerate(moves)]
        max_offset_top = len(self.move_texts) - 9
        max_offset_top = max(max_offset_top, 0)
        self.start_idx = min(self.start_idx, max_offset_top)
        self.draw()

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            event that occured
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.screen_rect.collidepoint(event.pos):   # pylint: disable=no-member
            if event.button == 4:  # scroll up
                self.start_idx -= 1
                self.start_idx = max(0, self.start_idx)

            if event.button == 5:  # scroll down
                self.start_idx += 1
                if self.start_idx > len(self.move_texts) - 9:
                    self.start_idx = max(0, len(self.move_texts) - 9)

            self.draw()

    def clear_indexes(self) -> None:
        """
        Clears the printed indexes.
        Useful, because when there was no change it doesn't draw itself.
        """
        self.printed_indexes = None

    def draw(self) -> None:
        """
        Draws the moves table.
        """
        self.end_idx = int(min(self.start_idx + 9, len(self.move_texts)))

        # already displayed
        if self.printed_indexes == (self.start_idx, self.end_idx):
            return

        self.printed_indexes = (self.start_idx, self.end_idx)

        self.draw_borders()
        self.surface.fill(BACKGROUND_COLOR, self.rect_without_border)

        top = 0.05

        for move_text in self.move_texts[self.start_idx: self.end_idx]:
            Text(self.surface,
                 Pos((0.9, self.row_height), (top, 0, 1 - top - self.row_height, 0), center=True),
                 self.screen_left_top,
                 text=move_text, font_size=4 * DEFAULT_FONT_SIZE // 5).draw()
            top += self.row_height
