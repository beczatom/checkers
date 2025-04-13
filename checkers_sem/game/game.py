from checkers_sem.game.board import Board
from checkers_sem.game.move import *
from collections import deque

def tree_fold_repetition(moves_stack : deque[Move, int]) -> bool:
    if len(moves_stack) < 6:
        return False

    return moves_stack[-1][0] == moves_stack[-3][0].revert() == moves_stack[-5][0] and \
        moves_stack[-2][0] == moves_stack[-4][0].revert() == moves_stack[-6][0]

class Game:

    def __init__(self):
        self.board = Board()
        self.moves_stack = deque[Move, int]()
        self.last_take = 0

    def push(self, move : Move):
        self.last_take += 1

        if move.move_type & TAKE:
            self.last_take = 0

        self.moves_stack.append((move, self.last_take))

        self.board.make_move(move)

    def pop(self):
        last_move, _ = self.moves_stack[-1]

        self.board.undo_move(last_move)

        self.moves_stack.pop()

        if len(self.moves_stack) != 0:
            self.last_take = self.moves_stack[-1][1]
        else:
            self.last_take = 0

    def peek(self):
        return self.moves_stack[-1][0]

    def get_moves(self):
        if self.last_take < 25:
            return self.board.get_legal_moves()
        return []

    def get_result(self) -> tuple | None:
        if self.board.black.bit_count() == 0:
            return 1, 0

        if self.board.white.bit_count() == 0:
            return 0, 1

        if self.last_take > 50 or tree_fold_repetition(self.moves_stack):
            return 1 / 2, 1 / 2
        return None

