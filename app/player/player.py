
"""
This module covers another fundamental part of the game - the player itself.
It is used in visualizations, not in genetics, because it interacts with GUI chessboard.
"""

from app.genetic.genetic_player import GeneticPlayer
from app.gui.utils.chessboard import ChessBoard
from app.genetic.constants import AI_COEFS
from app.genetic.constants import MAX_TRAIN_DEPTH
from app.game.move import Move
from app.game.game import Game


class Player:
    """
    Parent class for AI and Human players.
    """
    def __init__(self, chessboard : ChessBoard = None):
        """
        Adds interface - chessboard to player.

        Parameters
        ----------
        chessboard : ChessBoard
            to add
        """
        self.chessboard = chessboard

    def set_chessboard(self, chessboard : ChessBoard) -> None:
        """
        Setter for chessboard.

        Parameters
        ----------
        chessboard : ChessBoard
            to add
        """

        self.chessboard = chessboard

    def move(self, depth : int = MAX_TRAIN_DEPTH) -> tuple[bool, bool, tuple[Move, float] | None]:
        """
        Pure abstract method for getting move from player.

        Parameters
        ----------
        depth : int
            Depth of thinking, used only in AI.

        Returns
        -------
        x : tuple[bool, bool, Move]
            x[0] - no moves possible, x[1] - made move, x[2] - best move predicted (only AI)
        """

class AIPlayer(Player):
    """
    Defines AI player that interacts with chessboard.
    """
    def __init__(self, coefs : list[float], chessboard : ChessBoard = None):
        """
        Adds interface - chessboard to player.

        Parameters
        ----------
        coefs : list[float]
            coefficient for GeneticPlayer.
        chessboard : ChessBoard
            to add
        """
        super().__init__(chessboard)

        # absolutely unnecessary, only because of pylint
        if coefs is None:
            coefs = AI_COEFS

        self.player = GeneticPlayer(coefs)
        self.game = chessboard.game if chessboard is not None else None

    def set_game(self, game : Game) -> None:
        """
        Setter for game.

        Parameters
        ----------
        game : Game
            to set
        """
        self.game = game

    def set_chessboard(self, chessboard : ChessBoard):
        """
        Setter for chessboard.

        Parameters
        ----------
        chessboard : ChessBoard
            to add
        """
        self.game = chessboard.game

    # performs move in game via AI genetic player
    def move(self, depth : int = MAX_TRAIN_DEPTH) -> tuple[bool, bool, tuple[Move, float] | None]:
        """
        Makes best move.

        Parameters
        ----------
        depth : int
            Depth of thinking

        Returns
        -------
        x : tuple[bool, bool, Move]
            x[0] - no moves possible, x[1] - made move, x[2] - best move predicted
        """
        no_moves, best = self.player.move(self.game, depth)
        # returns if there are no moves to perform and if the move was performed
        return no_moves, not no_moves, best


class HumanPlayer(Player):
    """
    Class for interacting human player with chessboard.
    """
    def __init__(self, chessboard : ChessBoard = None):
        """
        Adds interface - chessboard to player.

        Parameters
        ----------
        coefs : list[float]
            coefficient for GeneticPlayer.
        chessboard : ChessBoard
            to add
        """
        super().__init__(chessboard)
        self.last_clicked = None


    # depth is always None, only for polymorphism compatibility
    def move(self, depth : int = None) -> tuple[bool, bool, tuple[Move, float] | None]:
        """
        Makes move.

        Parameters
        ----------
        depth : int
            Not used

        Returns
        -------
        x : tuple[bool, bool, Move]
            x[0] - no moves possible, x[1] - made move, x[2] - not used
        """

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
