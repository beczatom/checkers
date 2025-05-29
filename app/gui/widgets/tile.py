"""
This module implements a tile on chessboard
"""

import pygame

from app.gui.widgets.button import ImageButton
from app.gui.widgets.widget import Widget
from app.gui.widgets.loader import loader
from app.gui.constants import TILE_BACKGROUND, POSSIBLE_MOVE_IMG, BEST_TILE_IMG
from app.game.constants import BitBoard, Piece


class Tile(Widget):
    """
    This class implements a tile on chessboard
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the tile.
        Parameters
        ----------
        args
            for parent class
        kwargs
            for this child class
        """
        super().__init__(*args)
        self.pos_mask = kwargs.get('pos_mask', None)
        self.img_on_top = None
        self.best_move = False
        self.button = ImageButton(*args,
                                  background_image=TILE_BACKGROUND, onclick=kwargs.get('onclick'))

    def set_background_image(self, name: str) -> None:
        """
        Sets background image.
        Parameters
        ----------
        name : string
            name of the image
        """
        self.button.set_background_image(name)

    def put_piece_img(self, piece: Piece, piece_color: bool) -> None:
        """
        Puts a piece on the tile.
        Parameters
        ----------
        piece : Piece
            piece type
        piece_color : bool
            color of piece
        """
        self.img_on_top = loader.LOADED_IMAGES[(piece, piece_color)]

    def put_possible_move(self) -> None:
        """
        Puts a possible move on the tile.
        """
        self.img_on_top = loader.LOADED_IMAGES[POSSIBLE_MOVE_IMG]

    def put_best_move(self) -> None:
        """
        Puts a best move on the tile.
        """
        self.set_background_image(BEST_TILE_IMG)

    def clear_top(self) -> None:
        """
        Clears any piece or possible moves on the tile.
        """
        self.img_on_top = None

    def clear_img(self) -> None:
        """
        Sets tile to default, no image on top, default background image.
        """
        self.img_on_top = None
        self.set_background_image(TILE_BACKGROUND)

    def draw(self) -> None:
        """
        Draws the tile on the screen.
        """
        self.button.draw()
        if self.img_on_top is not None:
            surface_rect = pygame.Rect(self.surface.get_rect())
            image_rect = pygame.Rect(surface_rect.x + surface_rect.width // 5,
                                     surface_rect.y + surface_rect.height // 5,
                                     3 * surface_rect.width // 5, 3 * surface_rect.height // 5)
            image = pygame.transform.scale(self.img_on_top, image_rect.size)
            self.surface.blit(image, image_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles events on the tile.
        Parameters
        ----------
        event : pygame.event.Event
            event that occurred
        """
        self.button.handle_event(event)

    def get_pos(self) -> BitBoard:
        """
        Gets the position that tile represents.
        Returns
        -------
        pos : BitBoard
            position of tile in the chessboard coordinates
        """
        return self.pos_mask
