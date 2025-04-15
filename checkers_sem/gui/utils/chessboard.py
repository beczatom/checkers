
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


class ChessBoard:
    def __init__(self, screen):
        self.screen = screen
        self.tiles = self.tiles_init()

    def tiles_init(self) -> list[list[Tile]]:
        square_size = SCREEN_WIDTH // 2 // 8

        tiles = []
        for i in range(8):
            tiles.append([])
            tile_color = TileColor.WHITE if i % 2 == 0 else TileColor.BLACK
            for j in range(8):
                rect_y = i * square_size
                rect_x = j * square_size
                tiles[-1].append(Tile(self.screen, pygame.Rect(rect_x, rect_y, square_size, square_size),
                                                               coords_to_bitboard_mask((i, j)), tile_color))
                tiles[-1][-1].draw()
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
                    self.tiles[i][j].put_piece(piece, piece_color)
                else:
                    self.tiles[i][j].clear_piece()
                self.tiles[i][j].draw()

    def draw(self, game : Game):
        print(game.board.pawns & game.board.white)

        white_pawns = BitBoard(game.board.pawns & game.board.white)

        black_pawns = BitBoard(game.board.pawns & game.board.black)

        white_kings = BitBoard(~game.board.pawns & game.board.white)

        black_kings = BitBoard(~game.board.pawns & game.board.black)

        bool_boards = list(map(self.bitboard_to_bool_board, [white_pawns, black_pawns, white_kings, black_kings]))

        self.set_figures(bool_boards, [(Piece.PAWN, PieceColor.WHITE),
                                       (Piece.PAWN, PieceColor.BLACK),
                                       (Piece.KING, PieceColor.WHITE),
                                       (Piece.KING, PieceColor.BLACK)])