import itertools

from checkers_sem.game.move import *

class Board:
    def __init__(self):
        self.white = INITIAL_WHITE
        self.black = INITIAL_BLACK
        self.pawns = self.white | self.black
        self.turn = Turn.WHITE


    def is_promotion(self, mask : BitBoard, target_mask : BitBoard) -> bool:
        if mask & self.pawns == 0:
            return False

        return target_mask & PROMOTION_ROW_WHITE if self.turn == Turn.WHITE else target_mask & PROMOTION_ROW_BLACK



    def is_oponent(self, mask : BitBoard, oponent : BitBoard, not_file_mask: BitBoard = ALL_FILES):
        return mask & not_file_mask & oponent


    def is_free(self, mask : BitBoard, not_file_mask: BitBoard = ALL_FILES):
        return mask & not_file_mask & ~(self.black | self.white)


    def get_fig_type(self, mask : BitBoard):
        return Piece.PAWN if mask & self.pawns else Piece.KING
