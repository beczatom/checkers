
import pygame

from checkers_sem.game.game import Game
from checkers_sem.gui.utils.tile import Tile
from checkers_sem.constants import *

# coords being from (0, 0) on top-left corner
def coords_to_bitboard_mask(coords : tuple[int, int]) -> BitBoard | None:
    if coords[0] % 2 == coords[1] % 2: return None

    right_shift = 4 * coords[0]
    right_shift += coords[1] // 2

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

class ChessBoard:
    def __init__(self, surface : pygame.surface, top_left : tuple[int, int],  game : Game):
        self.surface = surface
        self.rect = pygame.Rect(top_left, surface.get_size())
        self.draw_borders()
        self.tiles = self.tiles_init()
        self.possible_moves = []
        self.game = game


    def draw_border(self, rect: pygame.Rect, border_width: int, border_gap: int):
        pygame.draw.rect(self.surface, BORDER_COLOR, rect)
        rect = pygame.Rect(rect.left + border_width, rect.top + border_width,
                           rect.width - 2 * border_width, rect.height - 2 * border_width)
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, rect)
        return pygame.Rect(rect.left + border_gap, rect.top + border_gap,
                           rect.width - 2 * border_gap, rect.height - 2 * border_gap)

    def draw_borders(self):
        available_rect = self.surface.get_rect()
        available_rect = self.draw_border(available_rect, FIRST_BORDER_WIDTH, BORDER_GAP)
        available_rect = self.draw_border(available_rect, SECOND_BORDER_WIDTH, 0)

        self.surface = self.surface.subsurface(available_rect)

    def tiles_init(self) -> list[list[Tile]]:
        square_size = self.surface.get_width() // 8

        tiles = []
        for i in range(8):
            tiles.append([])
            tile_color = TileColor.WHITE if i % 2 == 0 else TileColor.BLACK
            for j in range(8):
                rect_y = i * square_size
                rect_x = j * square_size
                tile_rect = pygame.Rect(rect_x, rect_y, square_size, square_size)

                screen_rect = pygame.Rect(self.rect.x + rect_x, self.rect.y + rect_y, square_size, square_size)
                tiles[-1].append(Tile(self.surface.subsurface(tile_rect), screen_rect,
                                                               coords_to_bitboard_mask((i, j)), tile_color))
                tiles[-1][-1].draw(pygame.mouse.get_pos())
                tile_color = not tile_color
        return tiles

    def bitboard_to_bool_board(self, bitboard : BitBoard) -> list[list[bool]]:
        bin_list = [bool(int(x)) for x in bin(bitboard)[2:].zfill(32)]

        k = 0

        bool_board = []
        for i in range(8):
            bool_board.append([])
            white = bool(i % 2 == 0)
            for j in range(8):
                bool_board[-1].append(False if white else bin_list[k])
                k += 0 if white else 1
                white = not white

        return bool_board


    def set_figures(self, bool_boards : list[list[list[bool]]], pieces : list[tuple[Piece, PieceColor]]):
        for i in range(8):
            for j in range(8):
                if i % 2 == j % 2: continue
                values = [bool_boards[k][i][j] for k in range(4)]
                true_idx = values.count(True)
                if true_idx == 1:
                    piece, piece_color = pieces[values.index(True)]
                    self.tiles[i][j].put_piece_img(piece, piece_color)
                elif (i, j) not in self.possible_moves:
                    self.tiles[i][j].clear_img()
                self.tiles[i][j].draw()

    def draw(self):
        white_pawns = BitBoard(self.game.board.pawns & self.game.board.white)
        black_pawns = BitBoard(self.game.board.pawns & self.game.board.black)

        white_kings = BitBoard(~self.game.board.pawns & self.game.board.white)
        black_kings = BitBoard(~self.game.board.pawns & self.game.board.black)

        bool_boards = list(map(self.bitboard_to_bool_board, [white_pawns, black_pawns, white_kings, black_kings]))

        self.set_figures(bool_boards, [(Piece.PAWN, PieceColor.WHITE),
                                       (Piece.PAWN, PieceColor.BLACK),
                                       (Piece.KING, PieceColor.WHITE),
                                       (Piece.KING, PieceColor.BLACK)])


    def get_clicked_mask(self, mouse_pos) -> BitBoard | None:
        for i in range(8):
            for j in range(8):
                if i % 2 == j % 2: continue
                if self.tiles[i][j].clicked(mouse_pos):
                    return self.tiles[i][j].pos_mask

        return None

    def set_possible_moves(self, possible_to_masks : list[BitBoard]):
        self.possible_moves = []
        for possible_to_mask in possible_to_masks:

            row, col = bitboard_to_coords(possible_to_mask)
            self.possible_moves.append((row, col))
            self.tiles[row][col].put_possible_move()

    def reset_possible_moves(self):
        self.possible_moves = []
