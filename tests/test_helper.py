from checkers_sem.game.constants import BitBoard, Color
from checkers_sem.gui.constants import AVERAGE_GENETIC_COEFICIENTS_TEXT, FILE_NAMES
from checkers_sem.game.move import Move
from checkers_sem.genetic.genetic import Genetic
from checkers_sem.state import *
from checkers_sem.genetic.genetic_player import GeneticPlayer
import queue

from checkers_sem.helper import tuple_sum, tuple_prod, tuple_rev, multiply_list

import pytest

def test_seconds_to_string():
    pass

def test_coords_to_bitboard_mask():
    pass

def test_bitboard_to_coords():
    pass

def test_bitboard_to_idx():
    pass

def test_bitboard_to_bool_board():
    pass

def test_bitboard_to_pos():
    pass

def test_move_to_display_string():
    pass

def test_get_awaited_train_time():
    pass

def test_seconds_to_min_sec():
    pass

def test_time_to_text():
    pass

@pytest.mark.parametrize('tuples, ref', [
    (((0, 0, 0, 0), (1, 2, 3, 4)), (1, 2, 3, 4)),
    (((0, 0, 0, 0), (1, 2, 3, 4), (4, 5, 6, 7)), (5, 7, 9, 11)),
    (((-1, -3.5, -5, -6), (0, 5, 0, 0)), (-1, 1.5, -5, -6)),
    (((-1, -2, -3), (4, 5, 6)), (3, 3, 3)),
])
def test_tuple_sum(tuples, ref : tuple):
    assert tuple_sum(*tuples) == ref

@pytest.mark.parametrize('tup, ref', [
    ((0, 0, 0, 0), (0, 0, 0, 0)),
    ((1, 2, 3, 4), (4, 3, 2, 1)),
    ((-1, -3.5, -5, -6), (-6, -5, -3.5, -1)),
    ((0, 5, 0, 0), (0, 0, 5, 0)),
    ((1, 2, 3), (3, 2, 1)),
])
def test_tuple_rev(tup : tuple, ref : tuple):
    assert tuple_rev(tup) == ref

@pytest.mark.parametrize('l, ref', [
    ([0, 0, 0, 0], 0),
    ([1, 2, 3, 4], 24),
    ([0.5, 0.5, 1, 2, 3, 4], 6),
    ([1, 2, 3, 4, 5], 120),
    ([0, 5, 0, 0], 0),
    ([-1, -2, -3, 4, 5], -120),
])
def test_multiply_list(l : list[float], ref : float):
    assert multiply_list(l) == ref

@pytest.mark.parametrize('tuples, ref', [
    (((0, 0, 0, 0), (1, 2, 3, 4)), (0, 0, 0, 0)),
    (((0.5, 0.5, 0.5, 0.5), (1, 2, 3, 4)), (0.5, 1, 1.5, 2)),
    (((0, 0, 0, 0), (1, 2, 3, 4), (4, 5, 6, 7)), (0, 0, 0, 0)),
    (((0.25, 0.25, 0.25, 0.25), (1, 2, 3, 4), (4, 5, 6, 7)), (1.0, 2.5, 4.5, 7.0)),
    (((-1, -3.5, -5, -6), (0, 5, 0, 0)), (0, -17.5, 0, 0)),
    (((-1, -2, -3), (4, 5, 6)), (-4, -10, -18)),
])
def test_tuple_prod(tuples, ref : tuple):
    assert tuple_prod(*tuples) == ref

def test_do_one_generation_thread():
    pass

def test_choose_best_thread():
    pass

def test_get_genetic_completion() -> int:
    pass

def test_get_coefs_header_text():
    pass
