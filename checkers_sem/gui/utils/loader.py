import pygame

from checkers_sem.constants import *


class Loader:
    def __init__(self):
        self.LOADED_IMAGES = None

    def load_images(self):
        self.LOADED_IMAGES = {
            TILE_BACKGROUND: pygame.image.load(TILE_BACKGROUND).convert_alpha(),
            LEFT_ARROW_IMAGE: pygame.image.load(LEFT_ARROW_IMAGE).convert_alpha(),
            RIGHT_ARROW_IMAGE: pygame.image.load(RIGHT_ARROW_IMAGE).convert_alpha(),
            RESTART_ARROW_IMAGE: pygame.image.load(RESTART_ARROW_IMAGE).convert_alpha(),
            POSSIBLE_MOVE_IMG : pygame.image.load(POSSIBLE_MOVE_IMG).convert_alpha(),
            SLIDER_CIRCLE : pygame.image.load(SLIDER_CIRCLE).convert_alpha(),
            BEST_TILE_IMG: pygame.image.load(BEST_TILE_IMG).convert_alpha(),
            (Piece.PAWN, PieceColor.WHITE) : pygame.image.load(PIECE_IMAGES[(Piece.PAWN, PieceColor.WHITE)]).convert_alpha(),
            (Piece.PAWN, PieceColor.BLACK) : pygame.image.load(PIECE_IMAGES[(Piece.PAWN, PieceColor.BLACK)]).convert_alpha(),
            (Piece.KING, PieceColor.WHITE) : pygame.image.load(PIECE_IMAGES[(Piece.KING, PieceColor.WHITE)]).convert_alpha(),
            (Piece.KING, PieceColor.BLACK) : pygame.image.load(PIECE_IMAGES[(Piece.KING, PieceColor.BLACK)]).convert_alpha(),
        }


loader = Loader()