"""
This module tests genetic player
"""

import numpy as np
import pytest
from unittest.mock import patch
from typing import Callable

from app.game.game import Game
from app.game.move import Move
from app.game.constants import Color, BitBoard, MoveType, TAKE, Piece
from app.genetic.constants import STATS_SIZE
from app.game.board import Board
from app.genetic.genetic_player import GeneticPlayer, play


@pytest.mark.parametrize('board_init, coefs, turn, ref_eval', [
    ((BitBoard(0x0000000f), BitBoard(0x00000000), BitBoard(0x00000004)), [1, 1, 1, 1, 1, 1], Color.WHITE, np.inf),
    ((BitBoard(0x0000000f), BitBoard(0x11111110), BitBoard(0x01000004)), [1, 1, 1, 1, 1, 1], Color.WHITE, -3),
    ((BitBoard(0x0000000f), BitBoard(0x11151110), BitBoard(0x00040004)), [0, 1, 2, 3, 4, 5], Color.BLACK, -6),
    ((BitBoard(0x0100000f), BitBoard(0x88888880), BitBoard(0x09000004)), [5, 4, 3, 2, 1, 0], Color.BLACK, -5),
    ((BitBoard(0x00000002), BitBoard(0x20000000), BitBoard(0x20000002)), [5, 4, 3, 2, 1, 0], Color.WHITE, 0),
])
def test_evaluate(board_init: tuple[BitBoard, BitBoard, BitBoard], coefs: np.array, turn: bool, ref_eval: np.float64):
    """
    Tests evaluate
    Parameters
    ----------
    board_init : tuple[BitBoard, BitBoard, BitBoard]
    coefs : np.array
    turn : bool
    ref_eval : np.float64
    """
    board = Board()
    board.white = board_init[0]
    board.black = board_init[1]
    board.pawns = board_init[2]
    board.turn = turn

    game = Game()
    game.board = board

    genetic_player = GeneticPlayer(coefs)

    assert genetic_player.evaluate(game) == ref_eval


class CallCounter:
    """
    Dummy class to count how many times was a func called
    """

    def __init__(self, func: Callable):
        """
        Init the class
        Parameters
        ----------
        func : Callable
        """
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        """
        Call the function
        Parameters
        ----------
        args : tuple
        kwargs : dict
        """
        self.calls += 1
        return self.func(*args, **kwargs)


@pytest.mark.parametrize('board_init, coefs, turn, ref_best_move, ref_eval_count', [
    ((BitBoard(0x0000000f), BitBoard(0x00000000), BitBoard(0x00000004)), [1, 1, 0, 0, 0, 0], Color.WHITE, None, 1),
    ((BitBoard(0x0000000f), BitBoard(0x00000000), BitBoard(0x00000004)), [1, 1, 0, 0, 0, 0], Color.BLACK, None, 1),
    ((BitBoard(0x00004000), BitBoard(0x00020000), BitBoard(0x00024000)), [1, 1, 0, 0, 0, 0], Color.WHITE,
     Move(Color.WHITE, (BitBoard(0x00004000), BitBoard(0x00200000)), MoveType() | TAKE | Piece.PAWN,
          BitBoard(0x00020000)), 1),
    ((BitBoard(0x00004000), BitBoard(0x00020000), BitBoard(0x00024000)), [1, 1, 0, 0, 0, 0], Color.BLACK,
     Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN,
          BitBoard(0x00004000)), 1),
])
def test_alpha_beta(board_init: tuple[BitBoard, BitBoard, BitBoard], coefs: np.array, turn: bool, ref_best_move: Move,
                    ref_eval_count: int):
    """
    Tests alpha beta
    Parameters
    ----------
    board_init : tuple[BitBoard, BitBoard, BitBoard]
    coefs : np.array
    turn : bool
    ref_best_move : Move
    ref_eval_count : int
    """
    board = Board()
    board.white = board_init[0]
    board.black = board_init[1]
    board.pawns = board_init[2]
    board.turn = turn

    game = Game()
    game.board = board

    genetic_player = GeneticPlayer(coefs)

    counter = CallCounter(genetic_player.evaluate)

    with patch('app.genetic.genetic_player.GeneticPlayer.evaluate', side_effect=counter):
        best_move = genetic_player.alpha_beta(game, -np.inf, np.inf, 3)[0]

    assert counter.calls == ref_eval_count

    if ref_best_move is None:
        assert best_move is None
        return

    assert best_move == ref_best_move


@pytest.mark.parametrize('board_init, coefs, turn, ref_best_move, ref_no_moves', [
    ((BitBoard(0x0000000f), BitBoard(0x00000000), BitBoard(0x00000004)), [1, 1, 0, 0, 0, 0], Color.WHITE, None, True),
    ((BitBoard(0x0000000f), BitBoard(0x00000000), BitBoard(0x00000004)), [1, 1, 0, 0, 0, 0], Color.BLACK, None, True),
    ((BitBoard(0x00004000), BitBoard(0x00020000), BitBoard(0x00024000)), [1, 1, 0, 0, 0, 0], Color.WHITE,
     Move(Color.WHITE, (BitBoard(0x00004000), BitBoard(0x00200000)), MoveType() | TAKE | Piece.PAWN,
          BitBoard(0x00020000)), False),
    ((BitBoard(0x00004000), BitBoard(0x00020000), BitBoard(0x00024000)), [1, 1, 0, 0, 0, 0], Color.BLACK,
     Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN,
          BitBoard(0x00004000)), False),
    ((BitBoard(0x000000ff), BitBoard(0x0000ff00), BitBoard(0x0000ffff)), [1, 1, 0, 0, 0, 0], Color.BLACK, None, True),

])
def test_move(board_init: tuple[BitBoard, BitBoard, BitBoard], coefs: np.array, turn: bool, ref_best_move: Move,
              ref_no_moves: bool):
    """
    Tests move
    Parameters
    ----------
    board_init : tuple[BitBoard, BitBoard, BitBoard]
    coefs : np.array
    turn : bool
    ref_best_move : Move
    ref_no_moves : bool
    """
    board = Board()
    board.white = board_init[0]
    board.black = board_init[1]
    board.pawns = board_init[2]
    board.turn = turn

    game = Game()
    game.board = board

    genetic_player = GeneticPlayer(coefs)

    no_moves, best_move = genetic_player.move(game, 3)

    assert no_moves == ref_no_moves

    if ref_best_move is None:
        assert best_move[0] is None
        return


def test_play():
    """
    Tests play
    """
    for _ in range(5):
        first = GeneticPlayer(np.random.rand(STATS_SIZE))
        first.coefs /= np.sum(first.coefs)
        second = GeneticPlayer(np.random.rand(STATS_SIZE))
        second.coefs /= np.sum(second.coefs)

        res = play(first, second, 2)
        assert res in [1, -1] or res - 0.5 < 1e-3
