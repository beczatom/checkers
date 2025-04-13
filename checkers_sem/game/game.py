from checkers_sem.game.board import Board
from checkers_sem.game.move import *
from collections import deque


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

