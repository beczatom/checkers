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


    def move_mask(self, mask: BitBoard, moves: list, target_mask: BitBoard, not_file_mask: BitBoard = ALL_FILES):
        if target_mask and target_mask & not_file_mask and (target_mask & (self.white | self.black)) == 0:
            if self.is_promotion(mask, target_mask):
                moves.append(Move(mask, target_mask, MoveType() | PROMOTION))
            else:
                moves.append(Move(mask, target_mask, MoveType()))


    def is_oponent(self, mask : BitBoard, oponent : BitBoard, not_file_mask: BitBoard = ALL_FILES):
        return mask & not_file_mask & oponent


    def is_free(self, mask : BitBoard, not_file_mask: BitBoard = ALL_FILES):
        return mask & not_file_mask & ~(self.black | self.white)


    def get_fig_type(self, mask : BitBoard):
        return Piece.PAWN if mask & self.pawns else Piece.KING

    # Move = (from, to, move_type, took_mask)
    def attacking(self, possible_move : Move, take_not_file : BitBoard, target_not_file : BitBoard, oponent : BitBoard):
        if (self.is_oponent(possible_move.took_mask, oponent, take_not_file)
                and self.is_free(possible_move.to_mask, target_not_file)):

            possible_move.move_type = TAKE | self.get_fig_type(possible_move.took_mask)

            if self.is_promotion(possible_move.from_mask, possible_move.to_mask):
                possible_move.move_type |= PROMOTION
            # possible_move is legal
            return possible_move

        # possible_move is illegal
        return None


    def attacking_moves_from_pos(self, mask: BitBoard):
        moves = []

        oponent_color = BitBoard(self.black) if self.white & mask else BitBoard(self.white)

        # white pieces or black king
        if self.white & mask or ((self.pawns & mask) == 0 and self.black & mask):
            # even row
            if mask & EVEN_ROW:
                # right take
                possible_move = self.attacking(Move(mask, BitBoard(mask << 7), MoveType(), BitBoard(mask << 4)), ALL_FILES, NOT_B_FILE, oponent_color)
                if possible_move is not None:
                    moves.append(possible_move)

                # left take
                possible_move = self.attacking(Move(mask, BitBoard(mask << 9), MoveType(), BitBoard(mask << 5)),
                                               NOT_G_FILE, ALL_FILES, oponent_color)
                if possible_move is not None:
                    moves.append(possible_move)
            else:
                # left take
                possible_move = self.attacking(Move(mask, BitBoard(mask << 9), MoveType(), BitBoard(mask << 4)),
                                               ALL_FILES, NOT_G_FILE, oponent_color)
                if possible_move is not None:
                    moves.append(possible_move)

                possible_move = self.attacking(Move(mask, BitBoard(mask << 7), MoveType(), BitBoard(mask << 3)),
                                               NOT_B_FILE, ALL_FILES, oponent_color)

                if possible_move is not None:
                    moves.append(possible_move)

        # black pieces or white king
        if self.black & mask or ((self.pawns & mask) == 0 and self.white & mask):
            # even row
            if mask & EVEN_ROW:

                # left take
                possible_move = self.attacking(Move(mask, BitBoard(mask >> 9), MoveType(), BitBoard(mask >> 4)),
                                               ALL_FILES, NOT_B_FILE, oponent_color)
                if possible_move is not None:
                    moves.append(possible_move)

                possible_move = self.attacking(Move(mask, BitBoard(mask >> 7), MoveType(), BitBoard(mask >> 3)),
                                               NOT_G_FILE, ALL_FILES, oponent_color)

                if possible_move is not None:
                    moves.append(possible_move)

            else:

                # right take
                possible_move = self.attacking(Move(mask, BitBoard(mask >> 7), MoveType(), BitBoard(mask >> 4)),
                                               ALL_FILES, NOT_G_FILE, oponent_color)
                if possible_move is not None:
                    moves.append(possible_move)

                # left take
                possible_move = self.attacking(Move(mask, BitBoard(mask >> 9), MoveType(), BitBoard(mask >> 5)),
                                               NOT_B_FILE, ALL_FILES, oponent_color)
                if possible_move is not None:
                    moves.append(possible_move)

        return moves


    def not_attacking_moves_from_pos(self, mask: BitBoard):
        moves = []
        # white pieces or black kings
        if self.white & mask or ((self.pawns & mask == 0) and self.black & mask):
            self.move_mask(mask, moves, BitBoard(mask << 4))

            if mask & EVEN_ROW:
                self.move_mask(mask, moves, BitBoard(mask << 5), NOT_G_FILE)
            else:
                self.move_mask(mask, moves, BitBoard(mask << 3), NOT_B_FILE)

        # black pieces or white kings
        if self.black & mask or ((self.pawns & mask == 0) and self.white & mask):
            self.move_mask(mask, moves, BitBoard(mask >> 4))

            if mask & EVEN_ROW:
                self.move_mask(mask, moves, BitBoard(mask >> 3), NOT_G_FILE)

            else:
                self.move_mask(mask, moves, BitBoard(mask >> 5), NOT_B_FILE)

        return moves

