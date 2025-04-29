from checkers_sem.constants import *
from checkers_sem.game.move import Move
# from checkers_sem.gui.menu import Menu
# from checkers_sem.gui.utils.button import Button

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


# def init_menu_button(self):
#     top = self.surface.get_rect().height // 16
#     left = top
#
#     size_x = self.surface.get_width() // 12
#     size_y = self.surface.get_height() // 16
#
#     mouse_rect = pygame.Rect(left, top, size_x, size_y)
#
#     def menu_button_onclick():
#         Menu(self.surface).show()
#
#     button = Button(self.surface.subsurface(mouse_rect), (left, top), MENU_BUTTON_TEXT, menu_button_onclick)
#     button.draw()
#     return button
