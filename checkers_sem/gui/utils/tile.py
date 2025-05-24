from checkers_sem.gui.utils.button import ImageButton
from checkers_sem.gui.utils.widget import Widget
from collections.abc import Callable
from checkers_sem.gui.utils.loader import *
from checkers_sem.game.constants import BitBoard

class Tile(Widget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int], pos_mask : BitBoard, onclick : Callable[[],None]):
        super().__init__(surface, left_top)
        self.pos_mask = pos_mask
        self.img_on_top = None
        self.best_move = False
        self.button = ImageButton(surface, self.left_top, TILE_BACKGROUND, onclick)

    def set_background_image(self, name : str):
        self.button.set_background_image(name)

    def put_piece_img(self, piece : Piece, piece_color : bool):
        self.img_on_top = loader.LOADED_IMAGES[(piece, piece_color)]

    def put_possible_move(self):
        self.img_on_top = loader.LOADED_IMAGES[POSSIBLE_MOVE_IMG]

    def put_best_move(self):
        self.set_background_image(BEST_TILE_IMG)
        # self.img_on_top = loader.LOADED_IMAGES[BEST_MOVE_IMG]

    def clear_top(self):
        self.img_on_top = None

    def clear_img(self):
        self.img_on_top = None
        self.set_background_image(TILE_BACKGROUND)

    def draw(self):
        self.button.draw()
        if self.img_on_top is not None:
            surface_rect = pygame.Rect(self.surface.get_rect())
            image_rect = pygame.Rect(surface_rect.x + surface_rect.width // 5, surface_rect.y + surface_rect.height // 5,
                                     3 * surface_rect.width // 5, 3 * surface_rect.height // 5)
            image = pygame.transform.scale(self.img_on_top, image_rect.size)
            self.surface.blit(image, image_rect)

    def handle_event(self, event : pygame.event.Event):
        return self.button.handle_event(event)

    def get_pos(self) -> BitBoard:
        return self.pos_mask