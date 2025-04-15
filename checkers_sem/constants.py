import numpy as np

#GAME###################################################################################################################

BitBoard = np.uint32

NOT_A_FILE =           ~BitBoard(0x08080808)
NOT_B_FILE =           ~BitBoard(0x80808080)
NOT_G_FILE =           ~BitBoard(0x01010101)
NOT_H_FILE =           ~BitBoard(0x10101010)
ALL_FILES  =            BitBoard(0xffffffff)

EVEN_ROW =              BitBoard(0x0f0f0f0f)

PROMOTION_ROW_WHITE =   BitBoard(0xf0000000)
PROMOTION_ROW_BLACK =   BitBoard(0x0000000f)

INITIAL_WHITE =         BitBoard(0x00000fff)
INITIAL_BLACK =         BitBoard(0xfff00000)

LEFT_EDGE =         BitBoard(0x08080808)
RIGHT_EDGE =        BitBoard(0x10101010)
HORIZONTAL_EDGE =   LEFT_EDGE | RIGHT_EDGE

TOP_NEXT_PROM_EDGE =    BitBoard(0x0f000000)
BOTTOM_NEXT_PROM_EDGE = BitBoard(0x000000f0)

TOP_ROW =               BitBoard(0xf0000000)
BOTTOM_ROW =            BitBoard(0x0000000f)

CENTER =                BitBoard(0x00666600)
MoveType = np.uint8
PROMOTION = MoveType(0x01)
TAKE =      MoveType(0x02)
TOOK_TYPE = MoveType(0x0c)

class Turn:
    WHITE = True
    BLACK = False

class Piece:
    PAWN = np.uint8(0x04)
    KING = np.uint8(0x08)

class PieceColor:
    WHITE = True
    BLACK = False

#GENETIC################################################################################################################

GENERATIONS = 5
POPULATION_SIZE = 10
MAX_TRAIN_DEPTH = 4
MUTATION_PCT = 0.125
CROSSOVER_PCT = 0.75

N_JOBS = 8

STATS_SIZE = 6

#GUI####################################################################################################################

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

class GameType:
    HUMAN_VS_HUMAN = 1
    HUMAN_VS_PC = 2
    PC_VS_PC = 3

MENU_TITLE = 'Checkers Menu'
HUMAN_VS_HUMAN_TEXT = 'Human vs Human'
HUMAN_VS_PC_TEXT = 'Human vs PC'
PC_VS_PC_TEXT = 'PC vs PC'

PIECE_TEXTS = {
    (Piece.PAWN, PieceColor.WHITE) : 'P',
    (Piece.PAWN, PieceColor.BLACK) : 'p',
    (Piece.KING, PieceColor.WHITE) : 'K',
    (Piece.KING, PieceColor.BLACK) : 'k',
}

class TileColor:
    WHITE = True
    BLACK = False

TILE_BACKGROUND_COLORS = {
    TileColor.BLACK:    (6, 7, 14),
    TileColor.WHITE:    (148, 161, 135),
}

