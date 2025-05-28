import pygame
import pytest
from unittest.mock import patch
import time

from checkers_sem.gui.constants import BACKGROUND_COLOR, BORDER_COLOR, POSSIBLE_MOVE_IMG
from checkers_sem.gui.utils.pos import Pos

from checkers_sem.game.move import Move
from checkers_sem.game.constants import MoveType, BitBoard, TAKE, Color, Piece, GameEnd

from checkers_sem.gui.utils.button import Button, ImageButton
from checkers_sem.gui.utils.checkbox import CheckBox
from checkers_sem.gui.utils.chessboard import ChessBoard
from checkers_sem.gui.utils.edit_text import EditText
from checkers_sem.gui.utils.loader import loader
from checkers_sem.gui.utils.move_table import MoveTable
from checkers_sem.gui.utils.progress_bar import ProgressBar
from checkers_sem.gui.utils.result import Result
from checkers_sem.gui.utils.slider import Slider
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.tile import Tile
from checkers_sem.gui.utils.timer import Timer
from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.utils.window import Window

from checkers_sem.state import state

from checkers_sem.game.game import Game
from checkers_sem.helper import bitboard_to_idx


def test_button():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    cnt = [0]

    def fake_on_click():
        cnt[0] += 1

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    button = Button(surface, pos, onclick=fake_on_click, text='abc')

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((30, 30)) == pygame.Color(BACKGROUND_COLOR)
    assert cnt[0] == 0
    assert button.text == 'abc'

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (10, 10), 'button': 1})

    button.handle_event(event)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((30, 30)) == pygame.Color(BACKGROUND_COLOR)
    assert button.text == 'abc'
    assert cnt[0] == 0

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 1})
    button.handle_event(event)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((30, 30)) == pygame.Color(BACKGROUND_COLOR)
    assert button.text == 'abc'
    assert cnt[0] == 1


def test_image_button():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    cnt = [0]

    def fake_on_click():
        cnt[0] += 1

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    button = ImageButton(surface, pos, onclick=fake_on_click, background_image=POSSIBLE_MOVE_IMG)
    button.draw()

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)
    assert cnt[0] == 0

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (10, 10), 'button': 1})

    button.handle_event(event)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)
    assert cnt[0] == 0

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 1})
    button.handle_event(event)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)
    assert cnt[0] == 1


def test_checkbox():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    cnt = [0]

    def fake_on_check():
        cnt[0] += 1

    def fake_on_uncheck():
        cnt[0] -= 1

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    checkbox = CheckBox(surface, pos, on_check=fake_on_check, on_uncheck=fake_on_uncheck)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)

    assert not checkbox.is_checked
    assert not checkbox.is_hovered
    assert cnt[0] == 0

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (10, 10), 'button': 1})

    checkbox.handle_event(event)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)
    assert not checkbox.is_checked
    assert not checkbox.is_hovered
    assert cnt[0] == 0

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 1})
    checkbox.handle_event(event)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)
    assert checkbox.is_checked
    assert not checkbox.is_hovered
    assert cnt[0] == 1

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 1})
    checkbox.handle_event(event)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)
    assert not checkbox.is_checked
    assert not checkbox.is_hovered
    assert cnt[0] == 0


def test_chessboard():
    pass


def test_edit_text():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    edit_text = EditText(surface, pos)
    edit_text.draw()

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)
    assert edit_text.get_string() == ''

    edit_text.set_string('0.12')

    assert edit_text.get_string() == '0.12'

    # not editing mode
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (10, 10), 'button': 1})
    edit_text.handle_event(event)
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_3, 'unicode': '3'})
    edit_text.handle_event(event)
    assert edit_text.get_string() == '0.12'

    # editing mode
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (50, 50), 'button': 1})
    edit_text.handle_event(event)
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_3, 'unicode': '3'})
    edit_text.handle_event(event)
    assert edit_text.get_string() == '0.123'

    # only 4 chars
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_4, 'unicode': '4'})
    edit_text.handle_event(event)
    assert edit_text.get_string() == '0.123'

    # backspace
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_BACKSPACE, 'unicode': '\b'})
    edit_text.handle_event(event)
    assert edit_text.get_string() == '0.12'

    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_BACKSPACE, 'unicode': '\b'})
    edit_text.handle_event(event)
    assert edit_text.get_string() == '0.1'

    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_BACKSPACE, 'unicode': '\b'})
    edit_text.handle_event(event)
    assert edit_text.get_string() == '0.'

    # '0.' can't be deleted
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_BACKSPACE, 'unicode': '\b'})
    edit_text.handle_event(event)
    assert edit_text.get_string() == '0.'


def test_loader():
    assert loader.LOADED_IMAGES is not None
    assert len(loader.LOADED_IMAGES.items()) > 0
    for key, value in loader.LOADED_IMAGES.items():
        assert value is not None


def test_move_table():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    move_table = MoveTable(surface, pos)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)

    moves = [
        Move(Color.WHITE, (BitBoard(0x00000800), BitBoard(0x00008000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00100000), BitBoard(0x00010000)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000100), BitBoard(0x00001000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x01000000), BitBoard(0x00100000)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000010), BitBoard(0x00000100)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00800000), BitBoard(0x00080000)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00400000), BitBoard(0x00040000)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00008000), BitBoard(0x00400000)), MoveType() | TAKE | Piece.PAWN,
             BitBoard(0x00040000))
    ]
    move_texts = [
        '1. B a3 - b4',
        '2. Č h6 - g5',
        '3. B g3 - h4',
        '4. Č g7 - h6',
        '5. B h2 - g3',
        '6. Č h8 - g7',
        '7. B b2 - a3',
        '8. Č b6 - a5',
        '9. B a1 - b2',
        '10. Č d6 - c5',
        '11. B b4 x c5'
    ]

    move_table.set_move_texts(moves)
    assert move_table.move_texts == move_texts
    assert move_table.start_idx == 0

    # not colliding
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (10, 10), 'button': 5})
    move_table.handle_event(event)
    assert move_table.start_idx == 0

    # colliding
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 5})
    move_table.handle_event(event)
    assert move_table.start_idx == 1

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 5})
    move_table.handle_event(event)
    assert move_table.start_idx == 2

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 5})
    move_table.handle_event(event)
    assert move_table.start_idx == 2

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 4})
    move_table.handle_event(event)
    assert move_table.start_idx == 1

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 4})
    move_table.handle_event(event)
    assert move_table.start_idx == 0

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 4})
    move_table.handle_event(event)
    assert move_table.start_idx == 0


@pytest.mark.parametrize('size, margin, center, ref_left_top', [
    ((0.5, 0.5), (0, 0, 0, 0), True, (0.25, 0.25)),
    ((1.1, 0.5), (0, 0, 0, 0), True, None),
    ((0.5, 0.5), (0, 0, 0, 0), False, (0, 0)),
    ((0.5, 0.25), (0.5, 0, 0.25, 0), True, (0.25, 0.5)),
    ((0.5, 0.25), (0.5, 0, 0, 0), True, (0.25, 0.625)),
])
def test_pos(size: tuple[float, float], margin: tuple[float, float, float, float], center: bool, ref_left_top):
    try:
        pos = Pos(size, margin, center=center)
        assert pos.size == size
        assert pos.left_top == ref_left_top
    except ValueError:
        if ref_left_top is not None:
            assert False


def test_progress_bar():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    bar = ProgressBar(surface, pos, value=0.01)

    assert bar.value == 0.01
    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)


@pytest.mark.parametrize('res', [
    ((-1, GameEnd.NO_TIME)),
    ((0, GameEnd.THREEFOLD_REPETITION)),
    ((1, GameEnd.NO_MOVES)),
    ((1, GameEnd.NO_FIGURES)),
    ((0, GameEnd.FIFTY_MOVES_WITHOUT_TAKE))
])
def test_result(res: tuple[float, int]):
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    Result(surface, pos, res=res)

    assert surface.get_rect().center == (50, 50)


def test_slider():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    value = [80]

    def fake_on_change(val: int):
        value[0] = val

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    slider = Slider(surface, pos, min=10, max=120, initial=80, onchange=fake_on_change)
    slider.draw()

    assert slider.get_value() == 80
    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BACKGROUND_COLOR)

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (10, 10), 'button': 1})
    slider.handle_event(event)
    assert value[0] == 80

    event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (0, 10), 'button': 1})
    slider.handle_event(event)
    assert value[0] == 80

    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (15, 15), 'button': 1})
    slider.handle_event(event)
    assert value[0] == 80

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (50, 50), 'button': 1})
    slider.handle_event(event)
    assert value[0] == 80

    event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (0, 10), 'button': 1})
    slider.handle_event(event)
    assert value[0] == 10


def test_text():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    text = Text(surface, pos, font_size=3)

    assert text.font_size == 3
    assert text.text == ''
    text.set_text('abcd')
    assert text.text == 'abcd'

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((10, 10)) == pygame.Color(BACKGROUND_COLOR)


def test_tile():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)

    value = [0]

    def fake_on_click():
        value[0] += 1

    tile = Tile(surface, pos, onclick=fake_on_click, pos_mask=BitBoard(0x00000001))
    tile.draw()

    assert tile.get_pos() == BitBoard(0x00000001)

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (10, 10), 'button': 1})

    tile.handle_event(event)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((48, 50)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)
    assert value[0] == 0

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 40), 'button': 1})
    tile.handle_event(event)

    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((48, 50)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)
    assert value[0] == 1

    tile.put_possible_move()
    tile.draw()
    assert surface.get_at((48, 50)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)

    tile.put_best_move()
    tile.draw()
    assert surface.get_at((25, 50)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((48, 50)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)

    tile.clear_top()
    tile.draw()
    assert surface.get_at((25, 50)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((48, 50)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)

    tile.put_piece_img(Piece.PAWN, Color.WHITE)
    tile.draw()
    assert surface.get_at((48, 50)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)

    tile.clear_img()
    tile.draw()
    assert surface.get_at((48, 50)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BORDER_COLOR)


def test_timer():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)

    state.TIME = 50

    timer = Timer(surface, pos)

    assert timer.get_time_left() == 50
    assert not timer.time_is_over()
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((30, 50)) == pygame.Color(BACKGROUND_COLOR)

    timer.time_start()
    assert timer.time_going
    time.sleep(1)
    timer.time_stop()
    assert not timer.time_going

    assert (time_left := timer.get_time_left()) < state.TIME
    time.sleep(1)
    assert time_left == timer.get_time_left()


def test_widget():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)

    widget = Widget(surface, pos)

    assert widget.screen_left_top == (25, 25)
    assert widget.left_top == (25, 25)
    assert widget.screen_rect.center == (50, 50)
    assert widget.surface.get_rect().size == (50, 50)

    assert surface.get_at((25, 25)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((30, 50)) == pygame.Color(BACKGROUND_COLOR)

    widget.draw_borders()
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((30, 50)) == pygame.Color(BACKGROUND_COLOR)

    subwidget = Widget(widget.surface, Pos((0.6, 0.6), (0, 0, 0, 0), center=True), widget.screen_left_top)

    assert subwidget.screen_left_top == (35, 35)
    assert subwidget.left_top == (10, 10)
    assert subwidget.screen_rect.center == (50, 50)
    assert subwidget.surface.get_rect().size == (30, 30)

    assert surface.get_at((35, 35)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((64, 64)) == pygame.Color(BACKGROUND_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)

    subwidget.draw_borders()
    assert surface.get_at((35, 35)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((64, 64)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)


def test_window():
    surface = pygame.Surface((200, 200))
    surface.fill(BACKGROUND_COLOR)

    window = Window(surface)
    assert surface.get_at((6, 10)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)

    assert window.run
    assert window.active_thread is None

    value = [0]

    def fake_refresh():
        value[0] += 1

    event = pygame.event.Event(pygame.QUIT)
    pygame.event.post(event)

    with (patch('checkers_sem.gui.utils.window.Window.refresh', side_effect=fake_refresh),
          patch('pygame.display.update', side_effect=fake_refresh)):
        try:
            window.show()
            assert False
        except StopIteration:
            assert value[0] == 0


def test_tiles_init() -> None:
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    pos = Pos((1, 1), (0, 0, 0, 0), center=True)

    chessboard = ChessBoard(surface, pos)

    assert surface.get_at((0, 0)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)

    assert len(chessboard.tiles) == 32

    mask = BitBoard(0x80000000)
    for tile in chessboard.tiles:
        assert tile.get_pos() == mask
        mask = mask >> 1
        assert surface.get_at((tile.screen_rect.center[0] - 5, tile.screen_rect.center[1])) == pygame.Color(
            BORDER_COLOR)


def test_set_figures() -> None:
    pieces = [(Piece.PAWN, Color.WHITE),
              (Piece.PAWN, Color.BLACK),
              (Piece.KING, Color.WHITE),
              (Piece.KING, Color.BLACK)]

    bool_boards = [
        [0, 0, 0, 1,
         0, 0, 0, 1,
         0, 0, 0, 1,
         0, 0, 0, 1,
         0, 0, 0, 1,
         0, 0, 0, 1,
         0, 0, 0, 1,
         0, 0, 0, 1],
        [1, 0, 0, 0,
         1, 0, 0, 0,
         1, 0, 0, 0,
         1, 0, 0, 0,
         1, 0, 0, 0,
         1, 0, 0, 0,
         1, 0, 0, 0,
         1, 0, 0, 0],
        [0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0],
        [0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0]
    ]
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    pos = Pos((1, 1), (0, 0, 0, 0), center=True)

    game = Game()
    chessboard = ChessBoard(surface, pos, game=game)
    chessboard.draw()
    chessboard.set_figures(bool_boards, pieces)

    for i, tile in enumerate(chessboard.tiles):
        if i % 4 == 0:
            assert tile.surface.get_at(tile.surface.get_rect().center) == pygame.Color(BORDER_COLOR)
        if i % 4 == 3:
            assert tile.surface.get_at(tile.surface.get_rect().center) == pygame.Color(BACKGROUND_COLOR)


def test_push_move() -> None:
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    pos = Pos((1, 1), (0, 0, 0, 0), center=True)

    game = Game()
    chessboard = ChessBoard(surface, pos, game=game)
    chessboard.draw()

    from_pos = BitBoard(0x00000100)
    from_tile = chessboard.tiles[bitboard_to_idx(from_pos)]
    to_pos = BitBoard(0x00001000)
    to_tile = chessboard.tiles[bitboard_to_idx(to_pos)]

    assert from_tile.surface.get_at(from_tile.surface.get_rect().center) == pygame.Color(BACKGROUND_COLOR)
    assert to_tile.surface.get_at(to_tile.surface.get_rect().center) == pygame.Color(BORDER_COLOR)

    chessboard.push_move(from_pos, to_pos)

    assert from_tile.surface.get_at(from_tile.surface.get_rect().center) == pygame.Color(BORDER_COLOR)
    assert to_tile.surface.get_at(to_tile.surface.get_rect().center) == pygame.Color(BACKGROUND_COLOR)


def test_set_possible_moves() -> None:
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    pos = Pos((1, 1), (0, 0, 0, 0), center=True)

    game = Game()
    chessboard = ChessBoard(surface, pos, game=game)

    mask = BitBoard(0x80000000)
    for tile in chessboard.tiles:
        assert tile.get_pos() == mask

        assert tile.surface.get_at(
            (tile.surface.get_rect().center[0] - 19, tile.surface.get_rect().center[1])) == pygame.Color(
            BACKGROUND_COLOR)
        assert tile.surface.get_at(
            (tile.surface.get_rect().center[0] - 3, tile.surface.get_rect().center[1])) == pygame.Color(
            BACKGROUND_COLOR)

        chessboard.set_possible_moves([mask])

        assert tile.surface.get_at(
            (tile.surface.get_rect().center[0] - 19, tile.surface.get_rect().center[1])) == pygame.Color(
            BACKGROUND_COLOR)
        assert tile.surface.get_at(
            (tile.surface.get_rect().center[0] - 3, tile.surface.get_rect().center[1])) == pygame.Color(
            BORDER_COLOR)

        mask = mask >> 1
