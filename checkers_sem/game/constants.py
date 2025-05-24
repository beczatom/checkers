import numpy as np

BitBoard = np.uint32

ALL_ROWS  =             BitBoard(0xffffffff)
BOARD_LEFT_TOP =        BitBoard(0x80000000)

EVEN_ROW =              BitBoard(0x0f0f0f0f)

PROMOTION_ROW_WHITE =   BitBoard(0xf0000000)
PROMOTION_ROW_BLACK =   BitBoard(0x0000000f)

INITIAL_WHITE =         BitBoard(0x00000fff)
INITIAL_BLACK =         BitBoard(0xfff00000)

LEFT_EDGE =             BitBoard(0x08080808)
RIGHT_EDGE =            BitBoard(0x10101010)
HORIZONTAL_EDGE =       LEFT_EDGE | RIGHT_EDGE

TOP_NEXT_PROM_EDGE =    BitBoard(0x0f000000)
BOTTOM_NEXT_PROM_EDGE = BitBoard(0x000000f0)

TOP_ROW =               BitBoard(0xf0000000)
BOTTOM_ROW =            BitBoard(0x0000000f)

CENTER =                BitBoard(0x00666600)


#   0000 0001   promotion
#   0000 0010   take
#   0000 1100   took_type

MoveType = np.uint8
PROMOTION = MoveType(0x01)
TAKE =      MoveType(0x02)
TOOK_TYPE = MoveType(0x0c)

class Color:
    WHITE = True
    BLACK = False

class Piece:
    PAWN = np.uint8(0x04)
    KING = np.uint8(0x08)

MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW_TRAIN = 30
MOVES_WITHOUT_TAKE_TO_CLAIM_DRAW = 50

class GameEnd:
    # somebody won
    NO_FIGURES = 1
    NO_MOVES = 2
    NO_TIME = 3

    # draw
    THREEFOLD_REPETITION = 4
    FIFTY_MOVES_WITHOUT_TAKE = 5
