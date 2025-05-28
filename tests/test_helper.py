"""
This module tests helper
"""

import pytest
import queue

from app.game.constants import BitBoard, Color, Piece
from app.game.move import Move, TAKE, PROMOTION, MoveType
from app.genetic.genetic import Genetic
from app.state import state
from app.helper import (seconds_to_string, coords_to_bitboard_mask, bitboard_to_coords,
                        bitboard_to_idx, bitboard_to_bool_board, bitboard_to_pos, move_to_display_string,
                        tuple_sum, tuple_prod, tuple_rev, multiply_list,
                        time_to_text, do_one_generation_thread, choose_best_thread)


@pytest.mark.parametrize('seconds, ref_text', [
    (0, '00 : 00'),
    (60, '01 : 00'),
    (12, '00 : 12'),
    (78, '01 : 18'),
    (3501, '58 : 21')
])
def test_seconds_to_string(seconds: int, ref_text: str):
    """
    Tests seconds to string
    Parameters
    ----------
    seconds : int
    ref_text : str
    """
    assert seconds_to_string(seconds) == ref_text


@pytest.mark.parametrize('coords, ref_mask', [
    ((0, 0), BitBoard(0x80000000)),
    ((7, 3), BitBoard(0x00000001)),
    ((6, 1), BitBoard(0x00000040)),
    ((1, 2), BitBoard(0x02000000)),
    ((3, 1), BitBoard(0x00040000))
])
def test_coords_to_bitboard_mask(coords: tuple[int, int], ref_mask: BitBoard):
    """
    Tests coords to bitboard mask
    Parameters
    ----------
    coords : tuple[int, int]
    ref_mask : BitBoard
    """
    assert coords_to_bitboard_mask(coords) == ref_mask


@pytest.mark.parametrize('mask, ref_coords', [
    (BitBoard(0x80000000), (0, 1)),
    (BitBoard(0x00000001), (7, 6)),
    (BitBoard(0x00000040), (6, 3)),
    (BitBoard(0x02000000), (1, 4)),
    (BitBoard(0x00040000), (3, 2))
])
def test_bitboard_to_coords(mask: BitBoard, ref_coords: tuple[int, int]):
    """
    Tests bitboard to coords
    Parameters
    ----------
    mask : BitBoard
    ref_coords : tuple[int, int]
    """
    assert bitboard_to_coords(mask) == ref_coords


@pytest.mark.parametrize('mask, ref_idx', [
    (BitBoard(0x80000000), 0),
    (BitBoard(0x00000001), 31),
    (BitBoard(0x00000040), 25),
    (BitBoard(0x02000000), 6),
    (BitBoard(0x00040000), 13)
])
def test_bitboard_to_idx(mask: BitBoard, ref_idx: int):
    assert bitboard_to_idx(mask) == ref_idx


@pytest.mark.parametrize('mask, ref_bool_board', [
    (BitBoard(0x80000000),
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (BitBoard(0x00000001),
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
    (BitBoard(0x00000040),
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
    (BitBoard(0x02000000),
     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (BitBoard(0x00040000),
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
])
def test_bitboard_to_bool_board(mask: BitBoard, ref_bool_board: list[bool]):
    """
    Tests bitboard to bool board
    Parameters
    ----------
    mask : BitBoard
    ref_bool_board : list[bool]
    """
    assert bitboard_to_bool_board(mask) == ref_bool_board


@pytest.mark.parametrize('mask, ref_coords', [
    (BitBoard(0x80000000), (8, 1)),
    (BitBoard(0x00000001), (1, 6)),
    (BitBoard(0x00000040), (2, 3)),
    (BitBoard(0x02000000), (7, 4)),
    (BitBoard(0x00040000), (5, 2))
])
def test_bitboard_to_pos(mask: BitBoard, ref_coords: tuple[int, int]):
    """
    Tests bitboard to coords
    Parameters
    ----------
    mask : BitBoard
    ref_coords : tuple[int, int]
    """
    assert bitboard_to_pos(mask) == ref_coords


@pytest.mark.parametrize('move, ref_text', [
    (Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000010)), MoveType()), 'B g1 - h2'),
    (Move(Color.BLACK, (BitBoard(0x80000000), BitBoard(0x08000000)), MoveType()), 'Č b8 - a7'),
    (Move(Color.WHITE, (BitBoard(0x00008000), BitBoard(0x00400000)), MoveType() | TAKE | Piece.PAWN,
          BitBoard(0x00040000)), 'B b4 x c5'),
    (Move(Color.BLACK, (BitBoard(0x00000010), BitBoard(0x00000001)), MoveType() | PROMOTION), 'Č h2 - g1+'),
    (Move(Color.WHITE, (BitBoard(0x00200000), BitBoard(0x10000000)), MoveType() | PROMOTION | TAKE | Piece.KING,
          BitBoard(0x01000000)), 'B f6 x g7+'),
])
def test_move_to_display_string(move: Move, ref_text: str):
    """
    Tests move to display string
    Parameters
    ----------
    move : Move
    ref_text : str
    """
    assert move_to_display_string(move) == ref_text


@pytest.mark.parametrize('seconds, ref_text', [
    (0, '< 1 sekunda'),
    (60, '1 minúta'),
    (12, '12 sekúnd'),
    (64, '1 minúta 4 sekundy'),
    (11282, '3 hodiny 8 minút 2 sekundy')
])
def test_time_to_text(seconds: int, ref_text: str):
    """
    Tests time to text
    Parameters
    ----------
    seconds : int
    ref_text : str
    """
    assert time_to_text(seconds) == ref_text


@pytest.mark.parametrize('tuples, ref', [
    (((0, 0, 0, 0), (1, 2, 3, 4)), (1, 2, 3, 4)),
    (((0, 0, 0, 0), (1, 2, 3, 4), (4, 5, 6, 7)), (5, 7, 9, 11)),
    (((-1, -3.5, -5, -6), (0, 5, 0, 0)), (-1, 1.5, -5, -6)),
    (((-1, -2, -3), (4, 5, 6)), (3, 3, 3)),
])
def test_tuple_sum(tuples: tuple, ref: tuple):
    """
    tests tuple sum
    Parameters
    ----------
    tuples : tuple
    ref : tuple
    """
    assert tuple_sum(*tuples) == ref


@pytest.mark.parametrize('tup, ref', [
    ((0, 0, 0, 0), (0, 0, 0, 0)),
    ((1, 2, 3, 4), (4, 3, 2, 1)),
    ((-1, -3.5, -5, -6), (-6, -5, -3.5, -1)),
    ((0, 5, 0, 0), (0, 0, 5, 0)),
    ((1, 2, 3), (3, 2, 1)),
])
def test_tuple_rev(tup: tuple, ref: tuple):
    """
    Tests tuple rev
    Parameters
    ----------
    tup : tuple
    ref : tuple
    """
    assert tuple_rev(tup) == ref


@pytest.mark.parametrize('l, ref', [
    ([0, 0, 0, 0], 0),
    ([1, 2, 3, 4], 24),
    ([0.5, 0.5, 1, 2, 3, 4], 6),
    ([1, 2, 3, 4, 5], 120),
    ([0, 5, 0, 0], 0),
    ([-1, -2, -3, 4, 5], -120),
])
def test_multiply_list(l: list[float], ref: float):
    """
    Tests multiply list
    Parameters
    ----------
    l : list[float]
    ref : float
    """
    assert multiply_list(l) == ref


@pytest.mark.parametrize('tuples, ref', [
    (((0, 0, 0, 0), (1, 2, 3, 4)), (0, 0, 0, 0)),
    (((0.5, 0.5, 0.5, 0.5), (1, 2, 3, 4)), (0.5, 1, 1.5, 2)),
    (((0, 0, 0, 0), (1, 2, 3, 4), (4, 5, 6, 7)), (0, 0, 0, 0)),
    (((0.25, 0.25, 0.25, 0.25), (1, 2, 3, 4), (4, 5, 6, 7)), (1.0, 2.5, 4.5, 7.0)),
    (((-1, -3.5, -5, -6), (0, 5, 0, 0)), (0, -17.5, 0, 0)),
    (((-1, -2, -3), (4, 5, 6)), (-4, -10, -18)),
])
def test_tuple_prod(tuples: tuple, ref: tuple):
    """
    Tests tuple prod
    Parameters
    ----------
    tuples : tuple
    ref : tuple
    """
    assert tuple_prod(*tuples) == ref


def test_do_one_generation_thread():
    """
    Tests do_one_generation_thread
    """
    state.GENERATIONS = 3
    state.MAX_TRAIN_DEPTH = 2
    state.POPULATION_SIZE = 8
    state.CROSSOVER_PCT = 1
    state.MUTATION_PCT = 1
    gen = Genetic()
    array_before = gen.population.copy()
    do_one_generation_thread(gen)
    assert array_before != gen.population


def test_choose_best_thread():
    """
    Tests choose_best_thread
    """
    state.GENERATIONS = 3
    state.MAX_TRAIN_DEPTH = 2
    state.POPULATION_SIZE = 8
    gen = Genetic()
    q = queue.Queue()
    choose_best_thread(gen, q)
    assert q.qsize() == 1
