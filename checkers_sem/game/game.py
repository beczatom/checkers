from checkers_sem.game.board import Board
from checkers_sem.game.move import *
from collections import deque


class Game:

    def __init__(self):
        self.board = Board()
        self.moves_stack = deque[Move, int]()
        self.last_take = 0
