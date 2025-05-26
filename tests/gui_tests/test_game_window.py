"""
This module tests the game windows.
"""

import copy
from threading import Thread

import pygame

from checkers_sem.game.game import Game
from checkers_sem.player.player import AIPlayer
from checkers_sem.gui.utils.chessboard import ChessBoard
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.pos import Pos
from checkers_sem.state import state
from checkers_sem.game.constants import Color
from checkers_sem.gui.constants import BACKGROUND_COLOR
from checkers_sem.gui.game_window.eval_helper import EvalHelper
from checkers_sem.gui.game_window.game_window import GameWindow
from checkers_sem.gui.game_window.game_display import GameDisplay
from checkers_sem.genetic.constants import AI_COEFS


def test_eval_helper():
    """
    Test eval helper.
    """

    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)

    texts = {Color.WHITE : None, Color.BLACK : None}
    pos = Pos((1, 0.1), (0, 0, 0.9, 0))
    texts[Color.BLACK] = Text(surface, pos)
    pos = Pos((1, 0.1), (0.9, 0, 0, 0))
    texts[Color.WHITE] = Text(surface, pos)

    game = Game()
    pos = Pos((1, 0.8), (0.1, 0, 0.1, 0))
    chessboard = ChessBoard(surface, pos, game = game)

    eval_helper = EvalHelper(chessboard, texts)

    assert eval_helper.chessboard == chessboard
    assert eval_helper.texts == texts
    assert eval_helper.evaluation_start_hash == hash(None)
    assert eval_helper.best_move is None
    assert eval_helper.active_thread is None

    move = next(chessboard.game.board.get_legal_moves())
    chessboard.push_move(move.from_mask, move.to_mask)

    eval_helper.get_eval()
    while eval_helper.active_thread is not None:
        eval_helper.get_eval()

    assert eval_helper.eval_values[Color.WHITE] is None
    assert eval_helper.eval_values[Color.BLACK] is not None

    assert texts[Color.WHITE].text == ''
    assert texts[Color.BLACK].text == ''

    eval_helper.update_eval()

    assert texts[Color.WHITE].text == ''
    assert texts[Color.BLACK].text != ''

    assert chessboard.best_move is None

    eval_helper.update_best_move()

    assert chessboard.best_move is not None

    evaluation = 85

    eval_helper.set_eval(evaluation, Color.WHITE)
    assert eval_helper.eval_values[Color.WHITE] == evaluation
    assert eval_helper.eval_values[Color.BLACK] is not None

def test_game_display():
    """
    Test game display.
    """
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    pos = Pos((1, 1), (0, 0, 0, 0))

    players = (AIPlayer(AI_COEFS), AIPlayer(AI_COEFS))
    state.DEPTH_BLACK = 1
    state.DEPTH_WHITE = 1
    game_display = GameDisplay(surface, pos, players = players)

    assert game_display.chessboard is not None
    assert game_display.players == players
    assert game_display.timers is not None
    assert game_display.res == (None, None)
    assert game_display.turn == Color.WHITE
    assert game_display.eval_helper is not None
    assert game_display.active_thread is None

    game_display.make_move()

    assert game_display.timers[Color.WHITE].get_time_left() < state.TIME
    assert not game_display.timers[Color.WHITE].time_going
    assert game_display.timers[Color.BLACK].time_going

    while game_display.res == (None, None):
        game_display.move_ai()
        game_display.check_game_end()

    assert game_display.timers[Color.WHITE].get_time_left() < state.TIME
    assert game_display.timers[Color.BLACK].get_time_left() < state.TIME
    assert not game_display.timers[Color.WHITE].time_going
    assert not game_display.timers[Color.BLACK].time_going

    assert game_display.res[0] is not None
    assert game_display.res[1] is not None
    assert game_display.active_thread is None
