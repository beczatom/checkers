import pygame
from checkers_sem.gui.utils.button import ImageButton
from checkers_sem.constants import *
from checkers_sem.gui.utils.widget import Widget
from collections.abc import Callable
from checkers_sem.gui.utils.loader import *

class Tile(Widget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int], pos_mask : BitBoard, onclick : Callable[[],None]):
        super().__init__(surface, left_top)
        self.background = TILE_BACKGROUND
        self.pos_mask = pos_mask
        self.piece_img = None
        self.possible_move = False
        self.button = ImageButton(surface, self.left_top, TILE_BACKGROUND, onclick)


    def put_piece_img(self, piece : Piece, piece_color : PieceColor):
        self.piece_img = loader.LOADED_IMAGES[(piece, piece_color)]
        self.possible_move = False

    def put_possible_move(self):
        self.possible_move = True

    def clear_img(self):
        self.piece_img = None
        self.possible_move = False

    def draw(self):
        self.button.draw()
        if self.piece_img is not None:
            surface_rect = pygame.Rect(self.surface.get_rect())
            image_rect = pygame.Rect(surface_rect.x + surface_rect.width // 5, surface_rect.y + surface_rect.height // 5,
                                     3 * surface_rect.width // 5, 3 * surface_rect.height // 5)
            image = pygame.transform.scale(self.piece_img, image_rect.size)
            self.surface.blit(image, image_rect)

        if self.possible_move:
            image = loader.LOADED_IMAGES[POSSIBLE_MOVE_IMG]
            image = pygame.transform.scale(image, self.surface.get_rect().size)
            self.surface.blit(image, self.surface.get_rect())

    def handle_event(self, event : pygame.event.Event):
        return self.button.handle_event(event)

    def get_pos(self) -> BitBoard:
        return self.pos_mask