import pygame

from checkers_sem.game.game import Game
from checkers_sem.gui.utils.widget import Widget
from checkers_sem.gui.utils.tile import Tile
from checkers_sem.game.constants import BitBoard, Piece, Color
from checkers_sem.helper import coords_to_bitboard_mask, bitboard_to_bool_board, bitboard_to_idx
from checkers_sem.gui.utils.pos import Pos

class ChessBoard(Widget):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args)
        self.draw_border()
        self.tiles = self.tiles_init()
        self.possible_moves = []
        self.best_move = None, None
        self.game = kwargs.get('game', None)
        self.clicked_mask = None
        self.clicked = False

    def generate_tile_onclick(self, pos : BitBoard):
        def tile_onclick():
            self.clicked_mask = pos
            self.clicked = True
        return tile_onclick

    def tiles_init(self) -> list[Tile]:
        # square_size = self.rect_without_border.width / 8
        square_size = 1 / 8

        tiles = []
        for i in range(8):
            top = i * square_size
            left = 0
            left += square_size if i % 2 == 0 else 0
            for j in range(4):

                # rect = pygame.Rect(left, top, square_size, square_size)
                # screen_left_top = tuple_sum(self.left_top, (left, top))

                mask = coords_to_bitboard_mask((i, j))
                tiles.append(Tile(self.surface.subsurface(self.rect_without_border),
                                  Pos((1 / 8, 1 / 8), (top, 0, 0, left)),
                                  self.screen_left_top,
                                  pos_mask = mask, onclick = self.generate_tile_onclick(mask)))

                left += 2 * square_size
                tiles[-1].draw()

        return tiles


    def set_figures(self, bool_boards : list[list[bool]], pieces : list[tuple[Piece, bool]]):
        for i in range(32):
            values = [bool_boards[k][i] for k in range(4)]
            true_idx = values.count(True)

            if self.best_move is not None and (i == self.best_move[0] or i == self.best_move[1]):
                if i == self.best_move[1]:
                    self.tiles[i].clear_top()
                self.tiles[i].put_best_move()
            elif true_idx == 1:
                piece, piece_color = pieces[values.index(True)]
                self.tiles[i].clear_img()
                self.tiles[i].put_piece_img(piece, piece_color)
            elif i not in self.possible_moves:
                self.tiles[i].clear_img()
            self.tiles[i].draw()

    def draw(self):
        self.draw_border()
        white_pawns = BitBoard(self.game.board.pawns & self.game.board.white)
        black_pawns = BitBoard(self.game.board.pawns & self.game.board.black)

        white_kings = BitBoard(~self.game.board.pawns & self.game.board.white)
        black_kings = BitBoard(~self.game.board.pawns & self.game.board.black)

        bool_boards = list(map(bitboard_to_bool_board, [white_pawns, black_pawns, white_kings, black_kings]))

        self.set_figures(bool_boards, [(Piece.PAWN, Color.WHITE),
                                       (Piece.PAWN, Color.BLACK),
                                       (Piece.KING, Color.WHITE),
                                       (Piece.KING, Color.BLACK)])

    def get_clicked_mask(self) -> BitBoard:
        return self.clicked_mask

    def push_move(self, from_pos : BitBoard, to_pos : BitBoard):
        self.game.push(self.game.get_move_from_to(from_pos, to_pos))
        self.set_possible_moves([])
        self.clicked_mask = None
        self.best_move = None
        self.draw()

    def set_possible_moves(self, possible_to_masks : list[BitBoard]):
        for possible_to_mask in self.possible_moves:
            idx = bitboard_to_idx(possible_to_mask)
            self.tiles[idx].clear_top()
            self.tiles[idx].draw()

        self.possible_moves = []
        for possible_to_mask in possible_to_masks:
            idx = bitboard_to_idx(possible_to_mask)
            self.possible_moves.append(possible_to_mask)
            self.tiles[idx].put_possible_move()
            self.tiles[idx].draw()

    def set_best_move(self, best_move : tuple[BitBoard, BitBoard]):
        self.best_move = (bitboard_to_idx(best_move[0]), bitboard_to_idx(best_move[1]))

    def reset_best_move(self):
        self.best_move = None

    def reset_possible_moves(self):
        self.possible_moves = []

    def handle_event(self, event : pygame.event.Event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        self.clicked = False
        for tile in self.tiles:
            tile.handle_event(event)

        if not self.clicked:
            self.clicked_mask = None