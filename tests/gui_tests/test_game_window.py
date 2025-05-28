"""
This module tests the game windows.
"""
import time

import pygame

from app.game.game import Game
from app.player.player import AIPlayer, HumanPlayer
from app.gui.utils.chessboard import ChessBoard
from app.gui.utils.text import Text
from app.gui.utils.pos import Pos
from app.state import state
from app.game.constants import Color
from app.gui.constants import BACKGROUND_COLOR
from app.gui.game_window.eval_helper import EvalHelper
from app.gui.game_window.game_window import GameWindow
from app.gui.game_window.game_display import GameDisplay
from app.gui.game_window.ai_vs_ai_window import AIVSAIWindow
from app.gui.game_window.human_vs_human_window import HumanVsHumanWindow
from app.gui.game_window.human_vs_ai_window import HumanVSAIWindow
from app.genetic.constants import AI_COEFS


def test_eval_helper():
    """
    Test eval helper.
    """

    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)

    texts = {Color.WHITE: None, Color.BLACK: None}
    pos = Pos((1, 0.1), (0, 0, 0.9, 0))
    texts[Color.BLACK] = Text(surface, pos)
    pos = Pos((1, 0.1), (0.9, 0, 0, 0))
    texts[Color.WHITE] = Text(surface, pos)

    game = Game()
    pos = Pos((1, 0.8), (0.1, 0, 0.1, 0))
    chessboard = ChessBoard(surface, pos, game=game)

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
    game_display = GameDisplay(surface, pos, players=players)

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

    while game_display.res == (None, None) or game_display.active_thread:
        game_display.move_ai()
        game_display.check_game_end()

    assert game_display.timers[Color.WHITE].get_time_left() < state.TIME
    assert game_display.timers[Color.BLACK].get_time_left() < state.TIME
    assert not game_display.timers[Color.WHITE].time_going
    assert not game_display.timers[Color.BLACK].time_going

    assert game_display.res[0] is not None
    assert game_display.res[1] is not None
    assert game_display.active_thread is None


def test_game_window() -> None:
    """
    Test game window.
    """

    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)

    state.DEPTH_BLACK = 1
    state.DEPTH_WHITE = 1
    players = (AIPlayer(AI_COEFS), AIPlayer(AI_COEFS))
    game_window = GameWindow(surface, players)

    assert game_window.surface == surface

    assert game_window.players == players
    assert game_window.game_display is not None
    assert len(game_window.move_table.move_texts) == 0
    assert len(game_window.game_control_buttons) == 3

    assert game_window.res_window is None
    assert not game_window.res_window_showed

    game_window.check_game_end()

    assert game_window.res_window is None
    assert not game_window.res_window_showed


def test_ai_vs_ai_window():
    """
    Test AI vs AI window.
    """

    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)

    state.DEPTH_BLACK = 1
    state.DEPTH_WHITE = 1
    players = (AIPlayer(AI_COEFS), AIPlayer(AI_COEFS))
    ai_vs_ai_window = AIVSAIWindow(surface, players)

    assert ai_vs_ai_window.surface == surface

    for _ in range(2):
        assert ai_vs_ai_window.players == players
        assert ai_vs_ai_window.game_display is not None
        assert len(ai_vs_ai_window.move_table.move_texts) == 0
        assert len(ai_vs_ai_window.game_control_buttons) == 3
        assert ai_vs_ai_window.res_window is None
        assert not ai_vs_ai_window.res_window_showed

        ai_vs_ai_window.check_game_end()

        assert ai_vs_ai_window.res_window is None
        assert not ai_vs_ai_window.res_window_showed

        while ai_vs_ai_window.game_display.res == (None, None) or ai_vs_ai_window.game_display.active_thread:
            ai_vs_ai_window.refresh()

        assert len(ai_vs_ai_window.move_table.move_texts) != 0
        assert len(ai_vs_ai_window.game_control_buttons) == 3
        assert ai_vs_ai_window.res_window is not None
        assert ai_vs_ai_window.res_window_showed

        ai_vs_ai_window.result_onclick()

        assert ai_vs_ai_window.res_window is None
        assert ai_vs_ai_window.res_window_showed

        # time.sleep(1)

        before_moves = ai_vs_ai_window.move_table.move_texts

        # back move
        ai_vs_ai_window.get_button_control_function(0)()

        assert ai_vs_ai_window.move_table.move_texts == before_moves[:-1]

        # move forward
        ai_vs_ai_window.get_button_control_function(1)()

        assert ai_vs_ai_window.move_table.move_texts == before_moves

        # reset game
        ai_vs_ai_window.get_button_control_function(2)()


def test_human_vs_human_window():
    """
    Test Human vs Human window.
    """

    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)

    state.DEPTH_BLACK = 1
    state.DEPTH_WHITE = 1
    players = (HumanPlayer(), HumanPlayer())
    human_vs_human_window = HumanVsHumanWindow(surface, players)

    assert human_vs_human_window.surface == surface

    assert human_vs_human_window.players == players
    assert human_vs_human_window.game_display is not None
    assert len(human_vs_human_window.move_table.move_texts) == 0
    assert len(human_vs_human_window.game_control_buttons) == 3
    assert human_vs_human_window.res_window is None
    assert not human_vs_human_window.res_window_showed

    human_vs_human_window.check_game_end()

    assert human_vs_human_window.res_window is None
    assert not human_vs_human_window.res_window_showed


def test_human_vs_ai_window():
    """
    Test Human vs Human window.
    """

    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)

    state.DEPTH_BLACK = 1
    state.DEPTH_WHITE = 1
    players = (HumanPlayer(), AIPlayer(AI_COEFS))
    human_vs_human_window = HumanVSAIWindow(surface, players)

    assert human_vs_human_window.surface == surface

    assert human_vs_human_window.players == players
    assert human_vs_human_window.game_display is not None
    assert len(human_vs_human_window.move_table.move_texts) == 0
    assert len(human_vs_human_window.game_control_buttons) == 3
    assert human_vs_human_window.res_window is None
    assert not human_vs_human_window.res_window_showed

    human_vs_human_window.check_game_end()

    assert human_vs_human_window.res_window is None
    assert not human_vs_human_window.res_window_showed
