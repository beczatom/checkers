"""
This module is responsible for PC decisions making in game.
"""

import numpy as np

from checkers_sem.game.game import Game
from checkers_sem.game.move import Move
from checkers_sem.constants import MAX_TRAIN_DEPTH, Color


class GeneticPlayer:
    """
    Represents a player with coefficients to evaluate a game and make moves in that.
    """

    def __init__(self, coefs: np.array):
        self.coefs = np.array(coefs, dtype=np.float64)

    def evaluate(self, game: Game) -> float:
        """
        Evaluates a game.

        Parameters
        ----------
        game : Game
            The game to evaluate.

        Returns
        -------
        evaluation : float
            The evaluation value.
        """

        # check if the game not ended
        possible_res = game.get_result()

        if possible_res is not None:
            # if ended, there is no better evaluation than +/- inf for white/black win
            # or 0 as perfect middle for draw
            if possible_res == 1:
                return np.inf
            if possible_res == -1:
                return -np.inf
            return 0

        # if the game didn't end we evaluate it with our coefs
        return np.dot(self.coefs, game.board.stats())

    def alpha_beta(self, game: Game, alpha: float, beta: float, depth: int) -> tuple[Move, float]:
        """
        Traditional min-max algorithm with alpha-beta pruning.

        Parameters
        ----------
        game : Game
            The game we need to find best move on.
        alpha : float
            Best already explored option on path to the root for white.
        beta : float
            Best already explored option on path to the root for black.
        depth : int
            Maximal depth of the tree (when reached zero, we only evaluate it).

        Returns
        -------
        (move, evaluation) : tuple[Move, float]
            The best move and evaluation of it
        """

        # terminal nodes
        if depth == 0 or game.get_result() is not None:
            if len(game.moves_stack) == 0:
                return None, self.evaluate(game)
            return game.peek(), self.evaluate(game)

        # white turn
        if game.board.turn == Color.WHITE:
            # pair of move and evaluation of that move
            best_move = (None, -np.inf)

            # for all child nodes
            for move in game.board.get_legal_moves():
                # push move
                game.push(move)

                # do the evaluation
                possible_best = self.alpha_beta(game, alpha, beta, depth - 1)

                # pop back, so we can have the same game again
                game.pop()

                # if the evaluation is better than what we found so far
                # or if we found nothing so far (happens when first child returned -inf)
                # but we want it also, otherwise, it would return None if white was losing (in every possible move)
                if best_move[1] < possible_best[1] or best_move[0] is None:
                    best_move = (move, possible_best[1])
                    alpha = possible_best[1]

                # alpha is higher than beta means that white has found something better for him
                # than the black could enforce, this means the black would never choose this path,
                # so all the child moves are irrelevant
                if alpha >= beta:
                    break

        else:
            # same as above
            best_move = (None, np.inf)
            for move in game.board.get_legal_moves():
                game.push(move)
                possible_best = self.alpha_beta(game, alpha, beta, depth - 1)
                game.pop()

                if best_move[1] > possible_best[1] or best_move[0] is None:
                    best_move = (move, possible_best[1])
                    beta = possible_best[1]

                if alpha >= beta:
                    break

        return best_move

    # returns true if lost for no possible moves or None if the game is currently undecided
    def move(self, game: Game, depth: int = MAX_TRAIN_DEPTH) -> tuple[bool, tuple[Move, float]]:
        """
        Player to make best move in game in given depth

        Parameters
        ----------
        game : Game
            Game the player will make best move in.
        depth : int
            Depth of the analysis.

        Returns
        -------
        (no_moves_left, (best_move, best_move_evaluation)) : tuple[bool, tuple[Move, float]]
            If the player has no moves left and the best move and evaluation of it.
        """

        # choose best move
        best = self.alpha_beta(game, -np.inf, np.inf, depth)

        # if player can not move, he loses
        # the player 'knows' about this, since best[0] is None implies best[1] = np.inf or -np.inf respectively
        # (there was no change in sons exploration)
        # so he tries to avoid it as much as possible

        # note, it may sound as a duplicate for best_move[0] is None above, but it is not,
        # because in min-max we want a player that if he can, he MUST move, no matter how bad is the move for him
        # here we check if he really has no moves left, that can happen also with non-zero material count
        # the rules are, that in that case player on turn loses
        if best[0] is None:
            return True, best

        game.push(best[0])
        return False, best

    def __str__(self) -> str:
        """
        Straightforward string representation of the coefficients of a player.

        Returns
        -------
        string : str
            String representation of the coefficients of a player.
        """
        return str(np.round(self.coefs, 3))


def play(white: GeneticPlayer, black: GeneticPlayer, depth: int) -> int:
    """
    Return result of two players playing a game on identical depth.

    Parameters
    ----------
    white : GeneticPlayer
        White player (starts the game).
    black : GeneticPlayer
        Black player.
    depth : int
        Depth of the analysis for both players.

    Returns
    -------
    result : int
        Result of the game.
    """

    # method used only in genetic train, so if the players are almost identical,
    # we just declare draw, the players would think similarly and the game would last long,
    # very often resulting in draw, also we don't see any reason to make difference between same coefficients
    if np.allclose(white.coefs, black.coefs, atol=1e-3):
        return 0

    # initial game state
    game = Game()

    # while the game is undecided
    while (res := game.get_result_train()) is None:

        # get turn (in checkers the turn do not change necessarily everytime (multiple takes))
        if game.board.turn == Color.WHITE:
            # we don't care about best move or the evaluation of it,
            # but we care about if the player lost by no ability to move
            if white.move(game, depth)[0]:
                return -1
        else:
            if black.move(game, depth)[0]:
                return 1

    # return the result
    return res
