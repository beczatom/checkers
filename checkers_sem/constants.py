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

# FILE_MASKS = np.array(
#     [
#         BitBoard(0x08080808), # A
#         BitBoard(0x80808080), # B
#         BitBoard(0x04040404), # C
#         BitBoard(0x40404040), # D
#         BitBoard(0x02020202), # E
#         BitBoard(0x20202020), # F
#         BitBoard(0x01010101), # G
#         BitBoard(0x10101010), # H
#     ]
# )
#
# ROW_MASKS = np.array(
#     [
#         BitBoard(0xf0000000), # 1
#         BitBoard(0x0f000000), # 2
#         BitBoard(0x00f00000), # 3
#         BitBoard(0x000f0000), # 4
#         BitBoard(0x0000f000), # 5
#         BitBoard(0x00000f00), # 6
#         BitBoard(0x000000f0), # 7
#         BitBoard(0x0000000f), # 8
#     ]
# )


#   0000 0001   promotion
#   0000 0010   take
#   0000 1100   took_type

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

class MenuOption:
    HUMAN_VS_HUMAN = 1
    HUMAN_VS_PC = 2
    PC_VS_PC = 3
    GENETIC = 4

MENU_TITLE = 'Checkers Menu'
HUMAN_VS_HUMAN_TEXT = 'Hráč proti hráčovi'
HUMAN_VS_PC_TEXT = 'Hráč proti počítaču'
PC_VS_PC_TEXT = 'Počítač proti počítaču'
GENETIC_TEXT = 'Genetické trénovanie'

SLIDER_PROPERTIES = [
    ('Veľkosť populácie', 2, 50, 10),
    ('Počet generácií', 1, 50, 10),
    ('Hĺbka trénovania', 1, 10, 4),
    ('Percento kríženia', 0, 100, 85),
    ('Percento mutácie', 0, 100, 25),
]

SLIDER_CIRCLE = 'assets/slider_circle.svg'

DEFAULT_FONT = 'assets/SpecialElite-Regular.ttf'
DEFAULT_TEXT_COLOR = (0,0,0)

PIECE_IMAGES = {
    (Piece.PAWN, PieceColor.WHITE) : 'assets/white_pawn.svg',
    (Piece.PAWN, PieceColor.BLACK) : 'assets/black_pawn.svg',
    (Piece.KING, PieceColor.WHITE) : 'assets/white_king.svg',
    (Piece.KING, PieceColor.BLACK) : 'assets/black_king.svg',
}

POSSIBLE_MOVE_IMG = 'assets/possible_tile.svg'

AI_COEFS = [3.6, 10.6, 4.4, 2.7, 5.2, 3.2]

class TileColor:
    WHITE = True
    BLACK = False

BACKGROUND_COLOR =  (224, 211, 175)
TEXT_COLOR = (0, 0, 0)

HOVER_BACKGROUND_COLOR =  (0, 0, 0)
HOVER_TEXT_COLOR = (255, 255, 255)

BORDER_COLOR = (0, 0, 0)

FIRST_BORDER_WIDTH = 4
SECOND_BORDER_WIDTH = 2
BORDER_GAP = 3

DEFAULT_FONT_SIZE = 20

TILE_BACKGROUND = {
    TileColor.BLACK:    'assets/black_tile.svg',
    TileColor.WHITE:    BACKGROUND_COLOR,
}

CHESSBOARD_LEFT_PADDING = 50

AWAITED_TIME_TRAIN_TEXT = 'Očakávaná doba trénovania:'
START_TRAIN_BUTTON_TEXT = 'Štart'
