"""
This module implements some useful function for all GUI classes.
"""
import queue

from checkers_sem.game.constants import BitBoard, Color
from checkers_sem.gui.constants import AVERAGE_GENETIC_COEFICIENTS_TEXT, FILE_NAMES
from checkers_sem.game.move import Move
from checkers_sem.genetic.genetic import Genetic
from checkers_sem.state import state
from checkers_sem.genetic.genetic_player import GeneticPlayer


def seconds_to_string(seconds: float) -> str:
    """
    Converts seconds to MM:SS format
    Parameters
    ----------
    seconds : float
        to convert

    Returns
    -------
    string : str
        string with MM:SS format
    """
    return f'{int(seconds) // 60:02} : {int(seconds) % 60:02}'


def coords_to_bitboard_mask(coords: tuple[int, int]) -> BitBoard | None:
    """
    Converts chessboard coordinates to BitBoard mask
    Parameters
    ----------
    coords : tuple[int, int]
        chessboard coordinates

    Returns
    -------
    mask : BitBoard
        converted bitboard mask
    """
    right_shift = coords[0] * 4 + coords[1]

    start = BitBoard(0x80000000)

    return BitBoard(start >> right_shift)


def bitboard_to_coords(bitboard: BitBoard) -> tuple[int, int]:
    """
    Converts bitboard mask to chessboard coordinates
    Parameters
    ----------
    bitboard : BitBoard
        bitboard mask

    Returns
    -------
    coords : tuple[int, int]
        chessboard coordinates
    """
    gap_from_start = 0
    while bitboard != BitBoard(0x80000000):
        bitboard <<= 1
        gap_from_start += 1

    row = gap_from_start // 4
    col = gap_from_start % 4
    col *= 2
    if row % 2 == 0:
        col += 1

    return row, col


def bitboard_to_idx(bitboard: BitBoard) -> int:
    """
    Converts bitboard mask idx to 32 bit array
    Parameters
    ----------
    bitboard : BitBoard
        bitboard mask

    Returns
    -------
    idx : int
        idx to 32 bit array
    """
    gap_from_start = 0
    while bitboard != BitBoard(0x80000000):
        bitboard <<= 1
        gap_from_start += 1
    return gap_from_start


def bitboard_to_bool_board(bitboard: BitBoard) -> list[bool]:
    """
    Converts bitboard to representation by bool values
    Parameters
    ----------
    bitboard : BitBoard
        bitboard to convert

    Returns
    -------
    bool_board : list[bool]
        list of bool values
    """
    return [bool(int(x)) for x in bin(bitboard)[2:].zfill(32)]


def bitboard_to_pos(bitboard: BitBoard) -> tuple[int, int]:
    """
    Converts bitboard to chessboard position from left down (traditional)
    Parameters
    ----------
    bitboard : BitBoard
        bitboard to convert

    Returns
    -------
    pos : tuple[int, int]
        traditional chessboard position
    """
    row, col = bitboard_to_coords(bitboard)
    row = 8 - row
    return row, col


def move_to_display_string(move: Move) -> str:
    """
    Converts move to displayable string
    Parameters
    ----------
    move : Move
        move to convert

    Returns
    -------
    string : str
        converted string
    """
    string = 'B ' if move.turn == Color.WHITE else 'Č '

    row, col = bitboard_to_pos(move.from_mask)
    string += FILE_NAMES[col] + str(row) + ' '
    if move.is_taking():
        string += 'x '
        row, col = bitboard_to_pos(move.took_mask)
        string += FILE_NAMES[col] + str(row)
    else:
        row, col = bitboard_to_pos(move.to_mask)
        string += '- ' + FILE_NAMES[col] + str(row)

    if move.is_promoting():
        string += '+'
    return string


def get_awaited_train_time(population: int, generations: int, depth: int) -> int:
    """
    From genetic setting computes estimated time.
    Parameters
    ----------
    population : int
        population size
    generations : int
        generation number
    depth : int
        depth of training

    Returns
    -------
    seconds : float
        estimated time in seconds
    """
    evolving_time = int(population * generations * 0.004 * 3.1 ** depth)
    choosing_best = int((population - 1) * (population - 2) / 2 * 0.004 * 3.1 ** depth)
    return evolving_time + choosing_best


def time_to_text(seconds: int | float) -> str:
    """
    Converts seconds to slovak text.
    Parameters
    ----------
    seconds : int | float
        seconds to convert

    Returns
    -------
    text : str
        representation of seconds in slovak
    """
    string = str()

    if seconds == 0:
        string += '< 1 sekunda'
        return string

    hours = seconds // 3600

    if hours == 1:
        string += '1 hodina '
    elif 1 < hours < 5:
        string += f'{hours} hodiny '
    elif 5 <= hours:
        string += f'{hours} hodín '

    minutes = (seconds % 3600) // 60

    if minutes == 1:
        string += '1 minúta '
    elif 1 < minutes < 5:
        string += f'{minutes} minúty '
    elif 5 <= minutes:
        string += f'{minutes} minút '

    seconds = seconds % 60

    if seconds == 1:
        string += '1 sekunda'
    elif 1 < seconds < 5:
        string += f'{seconds} sekundy'
    elif 5 <= seconds:
        string += f'{seconds} sekúnd'

    if string[-1] == ' ':
        string = string[:-1]

    return string


def tuple_sum(*tuples) -> tuple:
    """
    Provides elementwise sum of tuples
    Parameters
    ----------
    tuples
        to calculate sum
    Returns
    -------
    sum : tuple
        sum of tuples
    """
    tuples = list(tuples)
    return tuple(map(sum, zip(*tuples)))


def tuple_rev(tup: tuple) -> tuple:
    """
    Reverses tuple
    Parameters
    ----------
    tup : tuple
        tuple to reverse

    Returns
    -------
    rev : tuple
        reversed tuple
    """
    return tup[::-1]


def multiply_list(l: list[float]) -> float:
    """
    Calculates the product of list elements
    Parameters
    ----------
    l : list[float]
        list of elements

    Returns
    -------
    product : float
        product of elements
    """
    prod = l[0]
    for x in l[1:]:
        prod *= x
    return prod


def tuple_prod(*tuples) -> tuple:
    """
    Calculates the product of tuples elementwise
    Parameters
    ----------
    tuples
        tuples to calculate product

    Returns
    -------
    product : tuple
        elementwise product of tuples
    """
    tuples = list(tuples)
    return tuple(map(multiply_list, zip(*tuples)))


def do_one_generation_thread(genetic: Genetic) -> None:
    """
    Thread function to do one generation in genetic
    Parameters
    ----------
    genetic : Genetic
        where to do generation
    """
    genetic.do_iteration()


def choose_best_thread(genetic: Genetic, q: queue.Queue[GeneticPlayer]) -> None:
    """
    Thread function to choose the best genetic player
    Parameters
    ----------
    genetic : Genetic
        where to choose
    q : queue.Queue[GeneticPlayer]
        where to put the best
    """
    q.put(genetic.best())


def get_genetic_completion(generations: int) -> float:
    """
    Gets relative completion of genetic training
    Parameters
    ----------
    generations : int
        already did generations

    Returns
    -------
    relative_completion : float
        relative completion of genetic training
    """
    evolving_games = state.POPULATION_SIZE * state.GENERATIONS
    choosing_best_games = (state.POPULATION_SIZE - 1) * (state.POPULATION_SIZE - 2) / 2
    elapsed_games = state.POPULATION_SIZE * generations

    return elapsed_games / (evolving_games + choosing_best_games)


def get_coefs_header_text(generations: int) -> str:
    """
    Gets slovak text to display how many generations have been trained
    Parameters
    ----------
    generations : int
        how many generations have been trained

    Returns
    -------
    text : str
        text to display
    """

    string = AVERAGE_GENETIC_COEFICIENTS_TEXT
    if generations == 0:
        string += ' pri inicializácii'
    elif generations == 1:
        string += ' po 1 generácii'
    else:
        string += f' po {generations} generáciách'

    return string
