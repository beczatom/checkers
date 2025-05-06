"""
This module cares about the board.
For training genetics it is crucial to be as fast as possible.
So almost every procedure is only simple if-else or bitwise operations.
"""

from itertools import chain
from collections.abc import Iterable, Callable, Iterator
import numpy as np

from checkers_sem.game.move import Move
from checkers_sem.constants import BitBoard, INITIAL_WHITE, INITIAL_BLACK, Color, TAKE, PROMOTION, \
    PROMOTION_ROW_WHITE, PROMOTION_ROW_BLACK, MoveType, Piece, EVEN_ROW, TOP_NEXT_PROM_EDGE, \
    BOTTOM_NEXT_PROM_EDGE, HORIZONTAL_EDGE, TOP_ROW, BOTTOM_ROW, CENTER, BOARD_LEFT_TOP


def make_gen(iterable: Iterable[int], color: BitBoard, func: Callable[[BitBoard], list[Move]]) -> Iterator[Move]:
    """
    Yields func output if 1 left shifted by values of iterable and color is not None.

    Parameters
    ----------
    iterable : Iterable[int]
        iterable to get values from
    color : BitBoard
        to escape some func calls
    func : Callable[[BitBoard], list[Move]]
        function to get output

    Yields
    -------
    res : list[Move]
        output of func when the criteria are met
    """
    for i in iterable:
        if ~color & (1 << i):
            continue

        res = func(BitBoard(1 << i))
        if len(res) > 0:
            yield from res


def is_color(mask: BitBoard, color: BitBoard) -> bool:
    """
    Checks if on the mask is a piece of color, file_mask is used for filtering some positions.

    Parameters
    ----------
    mask : BitBoard
        position we are checking
    color : BitBoard
        positions where are the color pieces

    Returns
    -------
    is_color : BitBoard
        if there is a piece of color
    """
    return bool(mask & color)


class Board:
    """
    This class represents the heart of a game - the board.
    Because it's the main component, it needs to be fast and efficient.
    On representing the board state we use 3 x 32-bit unsigned integers.
    Two of them represent the positions of different colored pieces.
    The third represents the pawns positions.
    And also important is to remember the current turn.
    """

    def __init__(self):
        self.white = INITIAL_WHITE
        self.black = INITIAL_BLACK
        self.pawns = self.white | self.black
        self.turn = Color.WHITE

    def is_promotion(self, mask: BitBoard, target_mask: BitBoard) -> bool:
        """
        Checks if moving from mask to target_mask is promotion.

        Parameters
        ----------
        mask : BitBoard
            from where we move
        target_mask : BitBoard
            to where we move

        Returns
        -------
        is_promotion : bool
            if the possible move is considered as promotion
        """

        if mask & self.pawns == 0:
            return BitBoard(0)

        return bool(target_mask & PROMOTION_ROW_WHITE) if self.turn == Color.WHITE else bool(target_mask & PROMOTION_ROW_BLACK)

    def is_free(self, mask: BitBoard) -> bool:
        """
        Checks if the mask is free.

        Parameters
        ----------
        mask : BitBoard
            position where we are checking

        Returns
        -------
        is_free : BitBoard
            if there is empty space
        """
        return bool(mask & ~(self.black | self.white))

    def get_fig_type(self, mask: BitBoard) -> np.uint8:
        """
        Returns figure type of the mask.

        Parameters
        ----------
        mask : BitBoard
            position where we are checking

        Returns
        -------
        fig_type : np.uint8
            type of figure

        Warns
        -----
            Must be used on non-empty mask, otherwise the output would be king.
        """
        return Piece.PAWN if mask & self.pawns else Piece.KING

    def is_valid_attacking_move(self, possible_move: Move, oponent: BitBoard, current_row_parity: BitBoard) -> bool:
        """
        Checks possible attacking move if it is valid.

        Parameters
        ----------
        possible_move : Move
            move to check
        oponent : BitBoard
            positions of oponent
        current_row_parity : BitBoard
            attacking move CAN be valid if we take a figure on opposite parity row and jump to same parity row

        Returns
        -------
        is_valid : bool
            if the possible move is valid

        Warns
        -----
            Does not care about from where the move begins
            We also don't care about multiple line jumps, it is time-consuming and won't happen in move generation
        """

        return (bool(current_row_parity & possible_move.to_mask) and bool(~current_row_parity & possible_move.took_mask)
                and is_color(possible_move.took_mask, oponent)
                and self.is_free(possible_move.to_mask))

    def validate_attacking_move(self, possible_move: Move, oponent: BitBoard, current_row_parity: BitBoard):
        """
        If the move is valid attacking, it sets it to possible move and returns it.

        Parameters
        ----------
        possible_move : Move
            move to check
        oponent : BitBoard
            positions of oponent
        current_row_parity : BitBoard
            used for checking the move validity

        Returns
        -------
        valid attacking move : Move | None
            when possible_move is invalid we return None, else we set it to valid
        """

        # checking if is valid
        if self.is_valid_attacking_move(possible_move, oponent, current_row_parity):

            # setting to move that is taking and the oponent's piece type
            possible_move.move_type = TAKE | self.get_fig_type(possible_move.took_mask)

            # if it is also promoting, we set that
            if self.is_promotion(possible_move.from_mask, possible_move.to_mask):
                possible_move.move_type |= PROMOTION

            # return legal possible_move
            return possible_move

        # possible_move is illegal
        return None

    def attacking_moves_in_direction(self, mask: BitBoard, moves: list[Move], oponent: BitBoard, up: bool):
        """
        Makes attacking moves in direction.

        Parameters
        ----------
        mask : BitBoard
            from position
        moves : list[Move]
            where to append move
        oponent : BitBoard
            positions of oponent
        up : bool
            direction of attacking (to top of board or to bottom)
        """

        # setting the operator to use
        op = BitBoard.__lshift__ if up else BitBoard.__rshift__

        # parity of the current row
        # (crucially important, because the moves in this resized 32-bit uint differ from real moves)
        current_row_parity = EVEN_ROW if mask & EVEN_ROW else ~EVEN_ROW

        to_masks, take_masks = [], []
        if bool(mask & EVEN_ROW) == up:
            # (left on even row, right on even row)
            to_masks = [BitBoard(op(mask, 7)), BitBoard(op(mask, 9))]
            take_masks = [BitBoard(op(mask, 4)), BitBoard(op(mask, 5))]
        else:
            # (left on odd row, right on odd row)
            to_masks = [BitBoard(op(mask, 9)), BitBoard(op(mask, 7))]
            take_masks = [BitBoard(op(mask, 4)), BitBoard(op(mask, 3))]

        # append to moves if possible moves meets criteria
        for i, _ in enumerate(take_masks):
            possible_move = Move(self.turn, (mask, to_masks[i]), MoveType(), take_masks[i])
            if (move := self.validate_attacking_move(possible_move, oponent, current_row_parity)) is not None:
                moves.append(move)

    def attacking_moves_from_pos(self, mask: BitBoard) -> list[Move]:
        """
        Returns all attacking moves from a position.

        Parameters
        ----------
        mask : BitBoard
            from mask

        Returns
        -------
        moves : list[Move]
            list of valid moves from mask
        """
        moves = []

        oponent_color = BitBoard(self.black) if self.white & mask else BitBoard(self.white)

        # white pieces or black king
        if self.white & mask | (~(self.pawns & mask) & self.black & mask):
            self.attacking_moves_in_direction(mask, moves, oponent_color, True)

        # black pieces or white king
        if self.black & mask | (~(self.pawns & mask) & self.white & mask):
            self.attacking_moves_in_direction(mask, moves, oponent_color, False)

        return moves

    def is_valid_not_attacking_move(self, possible_move: Move, current_row_parity: BitBoard) -> bool:
        """
        Checks possible not attacking move if it is valid.

        Parameters
        ----------
        possible_move : Move
            move to check
        current_row_parity : BitBoard
            not attacking move is valid if go to opposite parity row

        Returns
        -------
        is_valid : bool
            if the possible move is valid

        Warns
        -----
            Does not care about from where the move begins
        """

        return bool(~current_row_parity & possible_move.to_mask) and self.is_free(possible_move.to_mask)

    def validate_not_attacking_move(self, possible_move: Move, current_row_parity: BitBoard) -> Move | None:
        """
        If the move is valid not attacking, it sets it to possible move and returns it.

        Parameters
        ----------
        possible_move : Move
            move to check
        current_row_parity : BitBoard
            used for checking the move validity

        Returns
        -------
        valid not attacking move : Move | None
            when possible_move is invalid we return None, else we set it to valid
        """

        # checking if is valid
        if self.is_valid_not_attacking_move(possible_move, current_row_parity):

            # if it is promoting, we set that
            if self.is_promotion(possible_move.from_mask, possible_move.to_mask):
                possible_move.move_type |= PROMOTION

            # return legal possible_move
            return possible_move

        # possible_move is illegal
        return None

    def not_attacking_moves_in_direction(self, mask: BitBoard, moves: list[Move], up: bool):
        """
        Makes not attacking moves in direction.

        Parameters
        ----------
        mask : BitBoard
            from position
        moves : list[Move]
            where to append move
        up : bool
            direction of move (to top of board or to bottom)
        """

        # setting the operator to use
        op = BitBoard.__lshift__ if up else BitBoard.__rshift__

        # parity of the current row
        # (crucially important, because the moves in this resized 32-bit uint differ from real moves)
        current_row_parity = EVEN_ROW if mask & EVEN_ROW else ~EVEN_ROW

        to_masks = [BitBoard(op(mask, 4))]
        if bool(mask & EVEN_ROW) == up:
            # (left on even row, right on even row)
            to_masks.append(BitBoard(op(mask, 5)))
        else:
            # (left on odd row, right on odd row)
            to_masks.append(BitBoard(op(mask, 3)))

        # append to moves if possible moves meets criteria
        for i, _ in enumerate(to_masks):
            possible_move = Move(self.turn, (mask, to_masks[i]), MoveType())
            if (move := self.validate_not_attacking_move(possible_move, current_row_parity)) is not None:
                moves.append(move)

    def not_attacking_moves_from_pos(self, mask: BitBoard) -> list[Move]:
        """
        Returns all not attacking moves from a position.

        Parameters
        ----------
        mask : BitBoard
            from mask

        Returns
        -------
        moves : list[Move]
            list of valid moves from mask
        """

        moves = []

        # white pieces or black kings
        if self.white & mask | (~(self.pawns & mask) & self.black & mask):
            self.not_attacking_moves_in_direction(mask, moves, True)

        # black pieces or white kings
        if self.black & mask | (~(self.pawns & mask) & self.white & mask):
            self.not_attacking_moves_in_direction(mask, moves, False)

        return moves

    def get_legal_moves(self) -> Iterator[Move]:
        """
        Returns all legal moves for current position and turn.

        Returns
        -------
        legal_moves : Iterator[Move]
            the possible legal moves
        """

        my_color = self.white if self.turn == Color.WHITE else self.black

        # check all the 32 positions if we find at least one attacking move
        attacking = (make_gen(range(32), my_color, self.attacking_moves_from_pos))

        try:
            # try to pick the first
            first = next(attacking)

            # we have attacking moves, so we return just them
            # in checkers the player MUST take if he can
            return chain([first], attacking)
        except StopIteration:
            # we have no attacking moves, so returning not attacking
            return make_gen(range(32), my_color, self.not_attacking_moves_from_pos)

    def make_move_changes(self, move: Move, my_color: BitBoard, oponent_color: BitBoard) -> tuple[BitBoard, BitBoard]:
        """
        Changes the board according to the move.

        Parameters
        ----------
        move : Move
            the desired move
        my_color : BitBoard
            figure positions of the one, who made the move
        oponent_color : BitBoard
            figure positions of the one, who didn't make the move
        Returns
        -------
        my_color, oponent_color : tuple[BitBoard, BitBoard]
            updated board according to the move
        """

        # make changes in my color
        my_color |= move.to_mask
        my_color &= ~move.from_mask

        # make changes in pawns
        if move.from_mask & self.pawns:
            self.pawns &= ~move.from_mask
            self.pawns |= move.to_mask

        # if took, then delete the figure
        # note that if no take was performed, the ~move.took_mask is full of 1,
        # so the statement effectively does nothing
        oponent_color &= ~move.took_mask

        # if took pawn, then delete the took_pos from pawns
        # note that if a king was taken, then the pawns mask is 0
        self.pawns &= ~move.took_mask

        # if promotion, then delete the to_pos from pawns
        if move.move_type & PROMOTION:
            self.pawns &= ~move.to_mask

        return my_color, oponent_color

    def make_move(self, move: Move) -> None:
        """
        Makes move and updates current turn.

        Parameters
        ----------
        move : Move
            the desired move
        """

        if self.turn == Color.WHITE:
            self.white, self.black = self.make_move_changes(move, self.white, self.black)
        else:
            self.black, self.white = self.make_move_changes(move, self.black, self.white)

        # if can't attack or was promoted, the turn changes
        if move.move_type & PROMOTION or move.move_type & TAKE == 0 or len(
                self.attacking_moves_from_pos(move.to_mask)) == 0:
            self.turn = not self.turn

    def undo_take(self, move: Move, oponent: BitBoard) -> BitBoard:
        """
        Puts back the figure that was taken.

        Parameters
        ----------
        move : Move
            the move from where we want to put back the taken piece
        oponent : BitBoard
            who suffered the loss of figure

        Returns
        -------
        oponent : BitBoard
            oponent positions with taken back figure
        """

        # note: if move.took_mask is zero (no take), we do nothing
        oponent |= move.took_mask
        if move.move_type & Piece.PAWN:
            self.pawns |= move.took_mask

        return oponent

    def undo_move(self, move: Move) -> None:
        """
        Undoes the move.
        Puts back the figure which was moved and, if something was taken, puts back that also.

        Parameters
        ----------
        move : Move
            move we want to undo
        """

        move_without_take = Move(None, (move.to_mask, move.from_mask), move.move_type & ~TAKE)

        # undo promotion
        if move.move_type & PROMOTION:
            self.pawns |= move.from_mask
            move_without_take.move_type = ~PROMOTION

        # put back the moved piece, put back the possibly taken piece, and set the turn to one, who made it
        if move.to_mask & self.white:
            self.white, self.black = self.make_move_changes(move_without_take, self.white, self.black)
            self.black = self.undo_take(move, self.black)
            self.turn = Color.WHITE
        else:
            self.black, self.white = self.make_move_changes(move_without_take, self.black, self.white)
            self.white = self.undo_take(move, self.white)
            self.turn = Color.BLACK

    def stats(self) -> np.array:
        """
        Computes some statistics about the board.
        Used for training coefficients in genetic algorithm.

        Returns
        -------
        stats : np.array[np.int16]
            stats from table
        """
        pawn_diff = (self.pawns & self.white).bit_count() - (self.pawns & self.black).bit_count()
        king_diff = (~self.pawns & self.white).bit_count() - (~self.pawns & self.black).bit_count()

        next_prom_rows_diff = (self.white & self.pawns & TOP_NEXT_PROM_EDGE).bit_count() - \
                              (self.black & self.pawns & BOTTOM_NEXT_PROM_EDGE).bit_count()

        horizontal_edge_diff = (self.white & HORIZONTAL_EDGE).bit_count() - (self.black & HORIZONTAL_EDGE).bit_count()

        base_diff = (self.white & BOTTOM_ROW).bit_count() - (self.black & TOP_ROW).bit_count()

        center_diff = (self.white & CENTER).bit_count() - (self.black & CENTER).bit_count()

        return np.array([pawn_diff, king_diff, next_prom_rows_diff,
                         horizontal_edge_diff, base_diff, center_diff], dtype=np.int16)

    def print_pos(self, mask: BitBoard) -> str:
        """
        Get the string representation of a figure on particular position.

        Parameters
        ----------
        mask : BitBoard
            position

        Returns
        -------
        figure_string : str
            Upper case for white, P for pawns, K for kings, _ for nothing.
        """
        if self.white & mask != 0:
            if self.pawns & mask != 0:
                return 'P'
            return 'K'
        if self.black & mask != 0:
            if self.pawns & mask != 0:
                return 'p'
            return 'k'
        return '_'

    def __str__(self):
        """
        Straightforward to string.
        White tiles are represented as 'x'.
        Unoccupied black tiles are represented as '_'.
        White pieces are upper case.
        Piece types are represented as first letter of their type.
        Finally current turn is appended

        Returns
        -------
        string : str
            Every attribute in one string
        """
        string = str()
        mask = BOARD_LEFT_TOP
        for i in range(32):
            # white tile on start
            if i % 8 == 0:
                string += 'x '

            # print figure
            string += self.print_pos(mask)

            # ugly, because of the smaller 32-bit representation
            if i % 4 == 3:
                if i % 8 == 7:
                    string += ' x '
                string += '\n'
            else:
                string += ' x '

            mask = mask >> 1

        string += 'Turn: White\n' if self.turn == Color.WHITE else 'Turn: Black\n'
        return string

    def __eq__(self, other) -> bool:
        """
        Straightforward equality.

        Parameters
        ----------
        other : Board

        Returns
        -------
        eq : bool
            True, if the two boards are equal
        """
        return (self.white == other.white and self.black == other.black
                and self.pawns == other.pawns and self.turn == other.turn)

    def __hash__(self) -> int:
        """
        Straightforward hash.

        Returns
        -------
        hash : int
            Hash of class as tuple of its attributes
        """
        return hash((self.white, self.black, self.pawns, self.turn))
