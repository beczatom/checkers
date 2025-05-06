"""
This module handles the game itself.
It holds the board and all the move history.
Also takes care of result and pushing / popping moves to / from board.
"""

from collections import deque
from collections.abc import Iterator

from checkers_sem.game.board import Board
from checkers_sem.game.move import Move
from checkers_sem.constants import BitBoard, TAKE, GameEnd, MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW, \
    MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW_TRAIN


def three_fold_repetition(moves_stack: deque[tuple[Move, int]]) -> bool:
    """
    Detects if in move_stack was threefold repetition (same move back and forth for two players).

    Parameters
    ----------
    moves_stack : deque[tuple[Move, int]]
        history of moves

    Returns
    -------
    three_fold_repetition : bool
        True if occurred, False otherwise
    """
    if len(moves_stack) < 6:
        return False

    return moves_stack[-1][0] == moves_stack[-3][0].revert() == moves_stack[-5][0] and \
        moves_stack[-2][0] == moves_stack[-4][0].revert() == moves_stack[-6][0]


class Game:
    """
    Class representing a game.
    It has a board, on which the game is played.
    Then holds the history of moves, and also the popped ones (will be used for "analyzing, replaying" the game).
    Last take number indicating how many moves passed after last take (important for result).

    Notes
    -------
        in the history of moves we hold a pair of move and last_take value,
        it is because when we go back, we can't know the value at that time
    """

    def __init__(self):
        self.board = Board()
        self.moves_stack = deque[tuple[Move, int]]()
        self.popped_moves = deque[tuple[Move, int]]()
        self.last_take = 0

    def push(self, move: Move) -> None:
        """
        Pushes a move to the board.

        Parameters
        ----------
        move : Move
            move to push
        """

        # resets the popped moves (we don't do any branching in histories)
        self.popped_moves = deque[tuple[Move, int]]()

        # last take increased by one
        self.last_take += 1

        # if the current move is taking, we reset the last_take counter
        if move.move_type & TAKE:
            self.last_take = 0

        # append to history and push to move
        self.moves_stack.append((move, self.last_take))
        self.board.make_move(move)

    def pop(self) -> None:
        """
        Pops a move from the board.
        """

        # if empty game do nothing
        if len(self.moves_stack) == 0:
            return

        # get the last move
        last_move, _ = self.moves_stack[-1]

        # undo it
        self.board.undo_move(last_move)

        # put to 'alternative history' (we might want it back later)
        self.popped_moves.append(self.moves_stack.pop())

        # set the last take as the previous move (before undo)
        self.last_take = 0 if len(self.moves_stack) == 0 else self.moves_stack[-1][1]

    def push_from_popped(self) -> None:
        """
        Push a move from the popped ones (going forward in history).
        """

        # if none was popped (or was reset) we don't do anything
        if len(self.popped_moves) == 0:
            return

        # gets the move from popped queue and pushes it to main
        move, self.last_take = self.popped_moves.pop()
        self.moves_stack.append((move, self.last_take))
        self.board.make_move(move)

    def peek(self) -> Move:
        """
        Returns the last move.

        Returns
        -------
        last_move : Move
            last move pushed
        """

        return self.moves_stack[-1][0]

    def get_moves(self) -> Iterator[Move] | list[Move]:
        """
        Returns legal moves in the current state.

        Returns
        -------
        moves : Iterator[Move] | list[Move]
            legal moves iterator or empty list if the game is a draw by rules
        """

        if self.last_take < MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW:
            return self.board.get_legal_moves()
        return []

    def get_moves_from_mask(self) -> list[Move]:
        """
        Returns all the masks of figures which can move.

        Returns
        -------
        from_masks : list[Move]
            all figure masks that can move
        """

        from_masks = []
        for move in self.board.get_legal_moves():
            from_masks.append(move.from_mask)
        return from_masks

    def get_moves_to_mask(self, from_mask: BitBoard) -> list[BitBoard]:
        """
        Returns all the masks of position where we can move to, from from_mask.

        Parameters
        -------
        from_mask : BitBoard
            from where to check

        Returns
        -------
        to_masks : list[Move]
            masks of position where we can move to
        """

        to_masks = []
        for move in self.board.get_legal_moves():
            if move.from_mask == from_mask:
                to_masks.append(move.to_mask)
        return to_masks

    def get_move_from_to(self, from_mask: BitBoard, to_mask: BitBoard) -> Move | None:
        """
        Gets the exact move from from_mask to to_mask.
        Note, at most one such move exists.
        Method may sound not useful, but we don't want to set flags as take, promotion, ...
        Particularly when we have a class (Board) that does the job.

        Parameters
        ----------
        from_mask : BitBoard
            from position
        to_mask : BitBoard
            to position

        Returns
        -------
        move : Move | None
            if we find such move we return it, otherwise we return None
        """

        for move in self.board.get_legal_moves():
            if move.from_mask == from_mask and move.to_mask == to_mask:
                return move
        return None

    def get_result_train(self) -> int | None:
        """
        Gets result of the game in genetic training.
        The number of moves to claim draw is decreased, because the train would last long.

        Returns
        -------
        result : int | None
            the result of the game in genetic training, if it didn't end, we return None
        """

        if self.board.black.bit_count() == 0:
            return 1

        if self.board.white.bit_count() == 0:
            return -1

        if self.last_take > MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW_TRAIN or three_fold_repetition(self.moves_stack):
            return 0

        return None

    def get_result(self) -> int | None:
        """
        Gets result of the game.

        Returns
        -------
        result : int | None
            the result of the game, if it didn't end, we return None
        """

        if self.board.black.bit_count() == 0:
            return 1

        if self.board.white.bit_count() == 0:
            return -1

        if self.last_take > MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW or three_fold_repetition(self.moves_stack):
            return 0

        return None

    def get_end_type(self) -> int | None:
        """
        Gets the reason why the game ended.

        Returns
        -------
        game_end_type : int | None
            the reason why the game ended, if it didn't end, we return None
        """

        if self.board.black.bit_count() == 0 or self.board.white.bit_count() == 0:
            return GameEnd.NO_FIGURES
        if self.last_take > MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW:
            return GameEnd.FIFTY_MOVES_WITHOUT_TAKE
        if three_fold_repetition(self.moves_stack):
            return GameEnd.THREEFOLD_REPETITION
        return None

    def get_move_history(self) -> list[Move]:
        """
        Returns move history as list (without last_take).

        Returns
        -------
        move_history : list[Move]
            The moves made so far
        """

        move_history = [move for move, _ in self.moves_stack]
        return move_history

    def __str__(self):
        """
        Only board to string and when the last take happened.

        Returns
        -------
        string : str
            board, and last take
        """

        return str(self.board) + 'Last Take: ' + str(self.last_take) + '\n'

    def __eq__(self, other):
        """
        Straightforward equality.

        Parameters
        ----------
        other : Game

        Returns
        -------
        eq : bool
            True, if the two games are equal
        """

        return self.board == other.board and self.last_take == other.last_take and self.moves_stack == other.moves_stack

    def __hash__(self):
        """
        Straightforward hash.

        Returns
        -------
        hash : int
            Hash of class as tuple of its attributes
        """

        return hash((self.board, self.last_take, tuple(self.moves_stack)))
