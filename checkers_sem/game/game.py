from checkers_sem.game.board import Board
from checkers_sem.game.move import *
from collections import deque

def three_fold_repetition(moves_stack : deque[tuple[Move, int]]) -> bool:
    if len(moves_stack) < 6:
        return False

    return moves_stack[-1][0] == moves_stack[-3][0].revert() == moves_stack[-5][0] and \
        moves_stack[-2][0] == moves_stack[-4][0].revert() == moves_stack[-6][0]

class Game:

    def __init__(self):
        self.board = Board()
        self.moves_stack = deque[tuple[Move, int]]()
        self.popped_moves = deque[tuple[Move, int]]()
        self.last_take = 0

    def push(self, move : Move):
        self.popped_moves = deque[tuple[Move, int]]()
        self.last_take += 1

        if move.move_type & TAKE:
            self.last_take = 0

        self.moves_stack.append((move, self.last_take))

        self.board.make_move(move)

    def pop(self) -> Move | None:
        if len(self.moves_stack) == 0:
            return None

        last_move, _ = self.moves_stack[-1]

        self.board.undo_move(last_move)

        self.popped_moves.append(self.moves_stack.pop())

        if len(self.moves_stack) != 0:
            self.last_take = self.moves_stack[-1][1]
        else:
            self.last_take = 0

        return None

    def push_from_popped(self):
        if len(self.popped_moves) == 0:
            return

        move, self.last_take = self.popped_moves.pop()
        self.moves_stack.append((move, self.last_take))
        self.board.make_move(move)

    def peek(self):
        return self.moves_stack[-1][0]

    def get_moves(self):
        if self.last_take < MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW:
            return self.board.get_legal_moves()
        return []

    def get_moves_from_mask(self):
        from_masks = []
        for move in self.board.get_legal_moves():
            from_masks.append(move.from_mask)
        return from_masks

    def get_moves_to_mask(self, from_mask : BitBoard) -> list[BitBoard]:
        to_masks = []
        for move in self.board.get_legal_moves():
            if move.from_mask == from_mask:
                to_masks.append(move.to_mask)
        return to_masks

    def get_move_from_to(self, from_mask : BitBoard, to_mask : BitBoard) -> Move | None:
        for move in self.board.get_legal_moves():
            if move.from_mask == from_mask and move.to_mask == to_mask:
                return move
        return None

    def get_result(self) -> tuple[float, float] | None:
        if self.board.black.bit_count() == 0:
            return 1, 0

        if self.board.white.bit_count() == 0:
            return 0, 1

        if self.last_take > MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW or three_fold_repetition(self.moves_stack):
            return 1 / 2, 1 / 2
        return None

    def get_end_type(self) -> int | None:
        if self.board.black.bit_count() == 0 or self.board.white.bit_count() == 0:
            return GameEnd.NO_FIGURES
        if self.last_take > MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW:
            return GameEnd.FIFTY_MOVES_WITHOUT_TAKE
        if three_fold_repetition(self.moves_stack):
            return GameEnd.THREEFOLD_REPETITION
        return None

    def get_move_history(self) -> list[Move]:
        move_history = [move for move, _ in self.moves_stack]
        return move_history

    def __str__(self):
        return str(self.board) + 'Last Take: ' + str(self.last_take) + '\n'

    def __eq__(self, other):
        return self.board == other.board and self.last_take == other.last_take and self.moves_stack == other.moves_stack

    def __hash__(self):
        return hash((self.board, self.last_take, tuple(self.moves_stack)))
