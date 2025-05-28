"""
This module does the evaluation of the game and displays it.
"""

import copy
from threading import Thread

from app.game.game import Game
from app.player.player import AIPlayer
from app.gui.utils.chessboard import ChessBoard
from app.gui.utils.text import Text
from app.state import state
from app.game.constants import Color


class EvalHelper:
    """
    This class does the evaluation of the game and displays it.
    """

    def __init__(self, chessboard: ChessBoard, texts: dict[bool, Text]):
        """
        Initializes the evaluation class.
        Parameters
        ----------
        chessboard : ChessBoard
            to evaluate the game and display the best move
        texts : dict[bool, Text]
            the evaluation texts
        """
        self.chessboard = chessboard
        self.texts = texts
        self.eval_values = {Color.BLACK: None, Color.WHITE: None}
        self.evaluation_start_hash = hash(None)
        self.best_move = None
        self.active_thread = None

    def get_eval(self) -> None:
        """
        Evaluates the game and saves the evaluation.
        """
        # if we are working and have result
        if self.active_thread is not None and not self.active_thread.is_alive():
            self.active_thread.join()
            if self.evaluation_start_hash != hash(self.chessboard.game):
                self.chessboard.reset_best_move()
                self.best_move = None
            self.active_thread = None

        # if something changed and we are not working on it
        if self.active_thread is None and self.evaluation_start_hash != hash(self.chessboard.game):
            self.evaluation_start_hash = hash(self.chessboard.game)
            self.active_thread = Thread(target=self.evaluating_thread, args=(copy.deepcopy(self.chessboard.game),))
            self.active_thread.start()

    def set_eval(self, evaluation: float, color: bool) -> None:
        """
        Sets evaluation.
        Useful, because when AI is thinking it returns the eval value also,
        so we don't need to evaluate again.
        Parameters
        ----------
        evaluation : float
            The evaluation value.
        color : bool
            Which player evaluated the game.
        """
        self.eval_values[color] = evaluation
        self.evaluation_start_hash = hash(self.chessboard.game)

    def update_eval(self):
        """
        Updates evaluation texts.
        """
        self.get_eval()
        for color in [Color.WHITE, Color.BLACK]:
            if self.eval_values[color] is not None:
                self.texts[color].set_text(f'{self.eval_values[color]:.3f}')
                self.texts[color].draw()

    def update_best_move(self) -> None:
        """
        Gets the best move and updates the best move.
        """
        if self.chessboard.best_move is None and self.evaluation_start_hash == hash(self.chessboard.game) and \
                self.active_thread is None:
            self.get_eval()
            self.chessboard.set_best_move(self.best_move)
            self.chessboard.draw()

    def evaluating_thread(self, game: Game) -> None:
        """
        Function for thread to evaluate the game.
        Parameters
        ----------
        game : Game
            game to evaluate
        """
        player = AIPlayer(state.COEFS_BLACK)
        player.set_game(game)
        _, _, best = player.move(state.DEPTH_BLACK)
        game.pop()
        self.eval_values[Color.BLACK] = best[1]
        self.best_move = (best[0].from_mask, best[0].to_mask)
