from checkers_sem.game.game import *
from checkers_sem.constants import *
from checkers_sem.genetic.genetic_player import *
from checkers_sem.gui.utils.chessboard import ChessBoard


class Player:
    def __init__(self, chessboard : ChessBoard = None):
        self.chessboard = chessboard

    def set_chessboard(self, chessboard):
        self.chessboard = chessboard

    def move(self, depth : int = MAX_TRAIN_DEPTH) -> tuple[bool, bool]:
        pass

class AIPlayer(Player):
    def __init__(self, coefs : list[float] = AI_COEFS, chessboard : ChessBoard = None):
        super().__init__(chessboard)
        self.player = GeneticPlayer(coefs)

    # performs move in game via AI genetic player
    def move(self, depth : int = MAX_TRAIN_DEPTH) -> tuple[bool, bool]:
        no_moves = self.player.move(self.chessboard.game, depth)
        # returns if there are no moves to perform and if the move was performed
        return no_moves, not no_moves

class HumanPlayer(Player):
    def __init__(self, chessboard : ChessBoard = None):
        super().__init__(chessboard)
        self.last_clicked = None


    # depth is always None, only for polymorphism compatibility
    def move(self, depth : int = None) -> tuple[bool, bool]:
        # returns if the player lost by no more moves left
        moves_num = len(self.chessboard.game.get_moves_from_mask())
        if moves_num == 0:
            return True, False

        # return if nothing was clicked
        clicked_now = self.chessboard.get_clicked_mask()
        if clicked_now is None:
            return False, False

        if self.last_clicked is not None and clicked_now in self.chessboard.game.get_moves_to_mask(self.last_clicked):
            # move can be performed
            self.chessboard.push_move(self.last_clicked, clicked_now)
            self.last_clicked = None
            return False, True

        if clicked_now not in self.chessboard.game.get_moves_from_mask():
            self.last_clicked = None
            return False, False

        # so far nothing was clicked
        self.last_clicked = clicked_now

        self.chessboard.set_possible_moves(self.chessboard.game.get_moves_to_mask(self.last_clicked))

        return False, False