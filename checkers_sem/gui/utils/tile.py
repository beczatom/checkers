import pygame
from checkers_sem.gui.utils.button import ImageButton
from checkers_sem.constants import *

class Tile:
    def __init__(self, surface : pygame.Surface, rect : pygame.Rect, pos_mask : BitBoard, color_bool : TileColor):
        self.surface = surface
        self.rect = rect
        self.background = TILE_BACKGROUND[color_bool]
        self.color_bool = color_bool
        self.pos_mask = pos_mask
        self.piece_img = None
        self.possible_move = False

        if color_bool == TileColor.BLACK:
            self.button = ImageButton(surface, self.rect, TILE_BACKGROUND[color_bool])


    def put_piece_img(self, piece : Piece, piece_color : PieceColor):
        if self.color_bool == TileColor.WHITE:
            raise Exception('Invalid color')

        self.piece_img = PIECE_IMAGES[(piece, piece_color)]
        self.possible_move = False

    def put_possible_move(self):
        self.possible_move = True


    def clear_img(self):
        if self.color_bool == TileColor.WHITE:
            raise Exception('Invalid color')

        self.piece_img = None
        self.possible_move = False

    def draw(self, mouse_pos : tuple[int, int] = (0, 0)):
        if self.color_bool == TileColor.WHITE:
            self.surface.fill(self.background)
            # pygame.draw.rect(self.screen, self.background, self.rect)
        else:
            self.button.draw(mouse_pos)
            if self.piece_img is not None:
                surface_rect = pygame.Rect(self.surface.get_rect())
                image_rect = pygame.Rect(surface_rect.x + surface_rect.width // 5, surface_rect.y + surface_rect.height // 5,
                                         3 * surface_rect.width // 5, 3 * surface_rect.height // 5)
                # image_rect = pygame.Rect(self.rect.x + self.rect.width // 5, self.rect.y + self.rect.height // 5,
                #                          3 * self.rect.width // 5, 3 * self.rect.height // 5)
                image = pygame.image.load(self.piece_img).convert_alpha()
                image = pygame.transform.scale(image, image_rect.size)
                self.surface.blit(image, image_rect)

        if self.possible_move:
            image = pygame.image.load(POSSIBLE_MOVE_IMG).convert_alpha()
            image = pygame.transform.scale(image, self.surface.get_rect().size)
            self.surface.blit(image, self.surface.get_rect())

    def clicked(self, mouse_pos) -> bool:
        if self.color_bool == TileColor.WHITE:
            raise Exception('Invalid color')
        return self.button.clicked(mouse_pos)

    def get_pos(self) -> BitBoard:
        if self.color_bool == TileColor.WHITE:
            raise Exception('Invalid color')
        return self.pos_mask