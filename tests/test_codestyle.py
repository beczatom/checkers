import inspect
import pytest
from pylint.lint import Run
from pylint.reporters import CollectingReporter

from checkers_sem.game import board, game, move
from checkers_sem.genetic import genetic, genetic_player
from checkers_sem.player import player
from checkers_sem.gui.utils import progress_bar

# I was inspired by BI-PYT homework testing
@pytest.mark.parametrize('file', [board, game, move, genetic, genetic_player, player, progress_bar])
def test_codestyle(file):
    """ Tests codestyle for given files. """
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
