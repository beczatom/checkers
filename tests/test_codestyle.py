"""
This module tests codestyle
"""

import inspect
import pytest
from pylint.lint import Run
from pylint.reporters import CollectingReporter

from app.game import board, game, move
from app.genetic import genetic, genetic_player
from app.player import player
from app.gui.utils import (button, checkbox, chessboard, edit_text, loader, move_table, pos, progress_bar,
                           result, slider, text, tile, timer, widget, window)
from app.gui import menu
from app import helper, main, state
from app.gui.genetic_window import genetic_window, genetic_setting_window, genetic_helper
from app.gui.game_setting import game_setting_window, game_setting_widget, game_setting_human_vs_human, \
    game_setting_human_vs_ai, game_setting_ai_vs_ai
from app.gui.game_window import game_window, game_display, eval_helper, human_vs_human_window, human_vs_ai_window, \
    ai_vs_ai_window


# I was inspired by BI-PYT homework testing
@pytest.mark.parametrize('file', [board, game, move, genetic, genetic_player, player,
                                  button, checkbox, chessboard, edit_text, loader, move_table, pos, progress_bar,
                                  result, slider, text, tile, timer, widget, window,
                                  menu,
                                  helper, main, state,
                                  genetic_window, genetic_setting_window, genetic_helper,
                                  game_setting_window, game_display, eval_helper, game_setting_widget,
                                  game_setting_human_vs_human, game_setting_human_vs_ai, game_setting_ai_vs_ai,
                                  game_window, human_vs_human_window, human_vs_ai_window, ai_vs_ai_window
                                  ])
def test_codestyle(file):
    """
    Tests codestyle for given files.
    """
    src_file = inspect.getfile(file)
    rep = CollectingReporter()
    # disabled warnings:
    # 0301 line too long
    # 0103 variables name (does not like shorter than 2 chars)
    res = Run(['--disable=C0301,C0103', '-sn', src_file], reporter=rep, exit=False)

    score = res.linter.stats.global_note

    for m in res.linter.reporter.messages:
        print(f'{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}')

    print(f'pylint score = {score} ({score * 10:.2f}%)')

    assert score >= 10
