from checkers_sem.constants import *
from checkers_sem.game.move import Move
from checkers_sem.genetic.genetic import Genetic
from checkers_sem.state import *
from checkers_sem.genetic.genetic_player import GeneticPlayer
import queue

def seconds_to_string(seconds : float) -> str:
    return f'{int(seconds) // 60:02} : {int(seconds) % 60:02}'

def coords_to_bitboard_mask(coords : tuple[int, int]) -> BitBoard | None:
    right_shift = coords[0] * 4 + coords[1]

    start = BitBoard(0x80000000)

    return BitBoard(start >> right_shift)

def bitboard_to_coords(bitboard : BitBoard) -> tuple[int, int]:
    gap_from_start = 0
    while bitboard != BitBoard(0x80000000):
        bitboard <<= 1
        gap_from_start += 1

    row = gap_from_start // 4
    col = gap_from_start % 4
    col *= 2
    if row % 2  == 0:
        col += 1

    return row, col

def bitboard_to_idx(bitboard : BitBoard) -> int:
    gap_from_start = 0
    while bitboard != BitBoard(0x80000000):
        bitboard <<= 1
        gap_from_start += 1
    return gap_from_start

def bitboard_to_bool_board(bitboard : BitBoard) -> list[bool]:
    return [bool(int(x)) for x in bin(bitboard)[2:].zfill(32)]

def bitboard_to_pos(bitboard : BitBoard) -> tuple[int, int]:
    row, col = bitboard_to_coords(bitboard)
    row = 8 - row
    return row, col

def move_to_display_string(move: Move) -> str:
    string = 'B ' if move.turn == Turn.WHITE else 'Č '

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


def get_awaited_train_time(population : int, generations : int, depth : int) -> int:
    evolving_time = int(population * generations * 0.004 * 3.1 ** depth)
    choosing_best = int((population - 1) * (population - 2) / 2 * 0.004 * 3.1 ** depth)
    return evolving_time + choosing_best

def seconds_to_min_sec(seconds : int):
    return f'{seconds // 60:02} : {seconds % 60:02}'

def time_to_text(seconds : int) -> str:
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

    return string

def tuple_sum(tuple1 : tuple[int, int], tuple2 : tuple[int, int]):
    return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]



def do_one_generation_thread(genetic : Genetic):
    genetic.do_iteration()

def choose_best_thread(genetic : Genetic, q : queue.Queue[GeneticPlayer]):
    q.put(genetic.best())

def get_genetic_completion(generations : int) -> int:
    evolving_games = state.POPULATION_SIZE * state.GENERATIONS
    choosing_best_games = (state.POPULATION_SIZE - 1) * (state.POPULATION_SIZE - 2) / 2
    elapsed_games = state.POPULATION_SIZE * generations

    return elapsed_games / (evolving_games + choosing_best_games)

def get_coefs_header_text(generations : int) -> str:
    string = AVERAGE_GENETIC_COEFICIENTS_TEXT
    if generations == 1:
        string += ' po 1 generácii'
    else:
        string += f' po {generations} generáciách'

    return string

