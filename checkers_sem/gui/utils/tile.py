import pygame
from checkers_sem.gui.utils.button import Button
from checkers_sem.constants import *

class Tile:
    def __init__(self, screen, rect, pos_mask : BitBoard, color_bool : TileColor):
        self.screen = screen
        self.rect = rect
        self.background_color = TILE_BACKGROUND_COLORS[color_bool]
        self.color_bool = color_bool
        self.pos_mask = pos_mask

        if color_bool == TileColor.BLACK:
            self.button = Button(screen, rect, '', self.background_color)


    def put_piece(self, piece : Piece, piece_color : PieceColor):
        if self.color_bool == TileColor.WHITE:
            raise Exception('Invalid color')

        self.button.text = PIECE_TEXTS[(piece, piece_color)]

    def clear_piece(self):
        if self.color_bool == TileColor.WHITE:
            raise Exception('Invalid color')

        self.button.text = ''

    def draw(self):
        if self.color_bool == TileColor.WHITE:
            pygame.draw.rect(self.screen, self.background_color, self.rect)
        else:
            self.button.draw()

    def clicked(self, mouse_pos) -> bool:
        if self.color_bool == TileColor.WHITE:
            raise Exception('Invalid color')
        return self.button.clicked(mouse_pos)

    def get_pos(self) -> BitBoard:
        if self.color_bool == TileColor.WHITE:
            raise Exception('Invalid color')
        return self.pos_mask