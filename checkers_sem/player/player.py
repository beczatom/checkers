
from checkers_sem.genetic.genetic_player import *
from checkers_sem.gui.utils.chessboard import ChessBoard


class Player:
    def __init__(self, chessboard : ChessBoard = None):
        self.chessboard = chessboard

    def set_chessboard(self, chessboard : ChessBoard):
        self.chessboard = chessboard

    def move(self, depth : int = MAX_TRAIN_DEPTH) -> tuple[bool, bool, tuple[Move, float] | None]:
        pass

class AIPlayer(Player):
    def __init__(self, coefs : list[float] = AI_COEFS, chessboard : ChessBoard = None):
        super().__init__(chessboard)
        self.player = GeneticPlayer(coefs)
        self.game = chessboard.game if chessboard is not None else None

    def set_game(self, game : Game) -> None:
        self.game = game

    def set_chessboard(self, chessboard : ChessBoard):
        self.game = chessboard.game

    # performs move in game via AI genetic player
    def move(self, depth : int = MAX_TRAIN_DEPTH) -> tuple[bool, bool, tuple[Move, float] | None]:
        no_moves, best = self.player.move(self.game, depth)
        # returns if there are no moves to perform and if the move was performed
        return no_moves, not no_moves, best


class HumanPlayer(Player):
    def __init__(self, chessboard : ChessBoard = None):
        super().__init__(chessboard)
        self.last_clicked = None


    # depth is always None, only for polymorphism compatibility
    def move(self, depth : int = None) -> tuple[bool, bool, tuple[Move, float] | None]:
        # returns if the player lost by no more moves left
        moves_num = len(self.chessboard.game.get_moves_from_mask())
        if moves_num == 0:
            return True, False, None

        # return if nothing was clicked
        clicked_now = self.chessboard.get_clicked_mask()
        if clicked_now is None:
            return False, False, None

        if self.last_clicked is not None and clicked_now in self.chessboard.game.get_moves_to_mask(self.last_clicked):
            # move can be performed
            self.chessboard.push_move(self.last_clicked, clicked_now)
            self.last_clicked = None
            return False, True, None

        if clicked_now not in self.chessboard.game.get_moves_from_mask():
            self.last_clicked = None
            return False, False, None

        # so far nothing was clicked
        self.last_clicked = clicked_now

        self.chessboard.set_possible_moves(self.chessboard.game.get_moves_to_mask(self.last_clicked))

        return False, False, None