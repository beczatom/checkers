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

