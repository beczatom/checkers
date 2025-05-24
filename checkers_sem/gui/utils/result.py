from collections.abc import Callable

from checkers_sem.gui.utils.widget import Widget

from checkers_sem.gui.utils.loader import *

from checkers_sem.gui.utils.button import Button
from checkers_sem.gui.utils.text import Text

from checkers_sem.gui.constants import DEFAULT_FONT_SIZE, WIN_TEXT, GAME_END_TYPE_TEXT, OK_TEXT
from checkers_sem.helper import tuple_sum

class Result(Widget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int],
                 res : int, game_end_type : int,
                 onclick : Callable[[], None] = None, ):
        super().__init__(surface, left_top)

        self.draw_border()

        self.res = res
        self.game_end_type = game_end_type

        self.init_res_text()
        self.init_game_end_type_text()

        self.onclick = onclick
        self.ok_button = self.init_ok_button()

    def init_res_text(self):
        top = self.rect_without_border.height // 8
        left = self.rect_without_border.x
        font_size = 2 * DEFAULT_FONT_SIZE
        text_rect = pygame.Rect(left, top, self.rect_without_border.width, font_size * 2)

        string = WIN_TEXT[self.res]
        Text(self.surface.subsurface(text_rect), tuple_sum(self.screen_left_top, (left, top)),
             string, font_size= font_size).draw()

    def init_game_end_type_text(self):
        top = self.rect_without_border.height // 3
        left = self.rect_without_border.x
        font_size = DEFAULT_FONT_SIZE
        text_rect = pygame.Rect(left, top, self.rect_without_border.width, font_size * 2)

        string = GAME_END_TYPE_TEXT[self.game_end_type]
        Text(self.surface.subsurface(text_rect), tuple_sum(self.screen_left_top, (left, top)),
             string, font_size=font_size).draw()

    def init_ok_button(self) -> Button:
        top = 3 * self.rect_without_border.height // 4
        font_size = DEFAULT_FONT_SIZE

        left = self.rect_without_border.width // 3
        button_rect = pygame.Rect(left, top, self.rect_without_border.width // 3, font_size * 2)

        button = Button(self.surface.subsurface(button_rect), tuple_sum(self.screen_left_top, (left, top)),
               OK_TEXT, self.onclick, font_size=font_size)

        button.draw()
        return button

    def handle_event(self, event : pygame.event.Event):
        self.ok_button.handle_event(event)

    def draw(self):
        pass
