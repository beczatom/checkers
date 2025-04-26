from checkers_sem.game.game import *
from checkers_sem.constants import *
from checkers_sem.genetic.genetic_player import *
from checkers_sem.gui.utils.chessboard import ChessBoard

import time

class Player:
    def __init__(self, chessboard : ChessBoard = None):
        self.chessboard = chessboard
        self.time_left = 70
        self.last_start = None

    def set_chessboard(self, chessboard):
        self.chessboard = chessboard

    def time_start(self):
        self.last_start = time.time()

    def time_stop(self):
        self.time_left = self.get_time_left()
        self.last_start = None

    def get_time_left(self) -> float:
        return self.time_left - (time.time() - self.last_start) if self.last_start else self.time_left

    def move(self, depth : int = MAX_TRAIN_DEPTH, clicked_mouse_pos : tuple[int, int] = None):
        pass

class AIPlayer(Player):
    def __init__(self, chessboard : ChessBoard = None):
        super().__init__(chessboard)
        self.player = GeneticPlayer(AI_COEFS)

    # performs move in game via AI genetic player
    def move(self, depth : int = MAX_TRAIN_DEPTH, clicked_mouse_pos : tuple[int, int] = None):
        no_moves = self.player.move(self.chessboard.game, depth)
        super().time_stop()
        return no_moves

class HumanPlayer(Player):
    def __init__(self, chessboard : ChessBoard = None):
        super().__init__(chessboard)
        self.last_clicked = None


    # depth is always None, only for polymorphism compatibility
    def move(self, depth : int = None, clicked_mouse_pos : tuple[int, int] = None):
        if clicked_mouse_pos is None:
            return

        if self.last_clicked is not None:
            clicked_now = self.chessboard.get_clicked_mask(clicked_mouse_pos)
            if clicked_now in self.chessboard.game.get_moves_to_mask(self.last_clicked):
                # move can be performed
                self.chessboard.game.push(self.chessboard.game.get_move_from_to(self.last_clicked, clicked_now))
                self.chessboard.reset_possible_moves()
                self.last_clicked = None
                super().time_stop()
                return None

        # so far nothing was clicked
        self.last_clicked = self.chessboard.get_clicked_mask(clicked_mouse_pos)
        if self.last_clicked not in self.chessboard.game.get_moves_from_mask():
            self.last_clicked = None

        self.chessboard.set_possible_moves(self.chessboard.game.get_moves_to_mask(self.last_clicked))

        # returns 1. if the player lost by no more moves left, 2. if player made a move
        if len(self.chessboard.game.get_moves_from_mask()) == 0:
            return True, False

        return None