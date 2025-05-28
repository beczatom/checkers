from checkers_sem.genetic.constants import POPULATION_SIZE, GENERATIONS, MAX_TRAIN_DEPTH, CROSSOVER_PCT, MUTATION_PCT
from checkers_sem.game.constants import Color, Piece, GameEnd
#GUI####################################################################################################################

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

REFRESH_RATE_MS = 10

class MenuOption:
    HUMAN_VS_HUMAN = 1
    HUMAN_VS_PC = 2
    PC_VS_PC = 3
    GENETIC = 4

MENU_TITLE = 'Dáma'
HUMAN_VS_HUMAN_TEXT = 'Hráč proti hráčovi'
HUMAN_VS_PC_TEXT = 'Hráč proti počítaču'
PC_VS_PC_TEXT = 'Počítač proti počítaču'
GENETIC_TEXT = 'Genetické trénovanie'

SLIDER_PROPERTIES = [
    ('Veľkosť populácie', 2, 50, POPULATION_SIZE),
    ('Počet generácií', 1, 50, GENERATIONS),
    ('Hĺbka trénovania', 1, 10, MAX_TRAIN_DEPTH),
    ('Percento kríženia', 0, 100, CROSSOVER_PCT * 100),
    ('Percento mutácie', 0, 100, MUTATION_PCT * 100),
]

BAR_IMAGE = 'checkers_sem/assets/bar.svg'

GENETIC_SETTINGS_TEXT =             'Nastavenia trénovania'

STAT_TEXTS = [
    'Hodnota pešiaka',
    'Hodnota kráľa',
    'Pešiak pred povýšením',
    'Figúra na bokoch',
    'Figúra na základni',
    'Figúra v centre'
]
AVERAGE_GENETIC_COEFICIENTS_TEXT =  'Priemerné koeficienty'
COEFICIENTS_TEXT =  'Koeficienty počítača'
WHITE_TEXT = 'Biely'
BLACK_TEXT = 'Čierny'

BEST_GENETIC_COEFICIENTS_TEXT =  'Výsledné koeficienty'

SLIDER_CIRCLE = 'checkers_sem/assets/slider_circle.svg'

DEFAULT_FONT = 'checkers_sem/assets/SpecialElite-Regular.ttf'
DEFAULT_TEXT_COLOR = (0,0,0)

PIECE_IMAGES = {
    (Piece.PAWN, Color.WHITE) : 'checkers_sem/assets/white_pawn.svg',
    (Piece.PAWN, Color.BLACK) : 'checkers_sem/assets/black_pawn.svg',
    (Piece.KING, Color.WHITE) : 'checkers_sem/assets/white_king.svg',
    (Piece.KING, Color.BLACK) : 'checkers_sem/assets/black_king.svg',
}

POSSIBLE_MOVE_IMG = 'checkers_sem/assets/possible_move.svg'
BEST_TILE_IMG = 'checkers_sem/assets/best_tile.svg'
SHOW_BEST_MOVES_TEXT = 'Najlepšie ťahy'

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

TILE_BACKGROUND = 'checkers_sem/assets/black_tile.svg'

CHESSBOARD_LEFT_PADDING = 50

AWAITED_TIME_TRAIN_TEXT = 'Očakávaná doba trénovania:'
START_TRAIN_BUTTON_TEXT = 'Štart'

FILE_NAMES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

GAME_CONTROL_BUTTON_IMAGES = ['checkers_sem/assets/left_arrow.svg',
                              'checkers_sem/assets/right_arrow.svg',
                              'checkers_sem/assets/restart_button.svg']

LEFT_ARROW_IMAGE = 'checkers_sem/assets/left_arrow.svg'
RIGHT_ARROW_IMAGE = 'checkers_sem/assets/right_arrow.svg'
RESTART_ARROW_IMAGE = 'checkers_sem/assets/restart_button.svg'

MENU_IMAGE = 'checkers_sem/assets/menu.png'


PLAY_BUTTON_TEXT = 'Hraj'

TIME = 300

TIME_SLIDER_TEXT = 'Čas'
TIME_SLIDER_MIN = 10
TIME_SLIDER_MAX = 3599

DEPTH_WHITE_TEXT = 'Hĺbka bieleho'
DEPTH_BLACK_TEXT = 'Hĺbka čierneho'
DEPTH_SLIDER_MIN = 1
DEPTH_SLIDER_MAX = 10


TIME_SLIDER_PROPERTIES = ('Čas', 10, 3599, TIME)
DEPTH_SLIDER_PROPERTIES = ('Hĺbka', 1, 10, 5)

CHECKED_CHECKBOX_BACKGROUND =  'checkers_sem/assets/black_tile.svg'

MENU_BUTTON_TEXT = 'Menu'

OK_TEXT =           'Okej'

WIN_TEXT = {1 : 'Biely vyhral', -1 : 'Čierny vyhral', 0 : 'Remíza' }

GAME_END_TYPE_TEXT = {
    GameEnd.NO_FIGURES :                'Nezostala žiadna figúrka',
    GameEnd.NO_MOVES :                  'Nezostal žiaden ťah',
    GameEnd.NO_TIME :                   'Čas vypršal',
    GameEnd.THREEFOLD_REPETITION :      'Opakovanie ťahov',
    GameEnd.FIFTY_MOVES_WITHOUT_TAKE :  'Veľa ťahov bez výmeny'
}
