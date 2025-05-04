from collections.abc import Callable

from checkers_sem.gui.utils.widget import Widget

from checkers_sem.gui.utils.loader import *

from checkers_sem.helper import *

class Slider(Widget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int],
                 min : int = 0, max : int = 100, initial : int = 50,
                 onchange : Callable[[int], None] = None, ):
        super().__init__(surface, left_top)

        self.min = min
        self.max = max
        self.value = initial

        self.circle_rect = self.__get_circle_rect()

        self.mouse_drag = False

        self.onchange = onchange

    def handle_event(self, event : pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            left_top = tuple_sum(self.left_top, (self.circle_rect.x, self.circle_rect.y))
            circle_screen_rect = pygame.Rect(*left_top, *self.circle_rect.size)
            if circle_screen_rect.collidepoint(event.pos):
                self.mouse_drag = True

        if event.type == pygame.MOUSEMOTION and self.mouse_drag:
            pos_x = event.pos[0]
            pos_on_line = pos_x - self.left_top[0] - self.circle_rect.width // 2
            if pos_on_line < 0:
                pos_on_line = 0

            if pos_on_line > self.surface.get_width() - self.circle_rect.width:
                pos_on_line = self.surface.get_width() - self.circle_rect.width

            self.value = int((pos_on_line / (self.surface.get_width() - self.circle_rect.width)) * (self.max - self.min) + self.min)
            self.onchange(self.value)
            self.draw()

        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_drag = False

    def __get_circle_rect(self) -> pygame.Rect:
        line_width = self.get_height() // 8
        top = self.get_height() // 2 - line_width // 2
        circle_size = 3 * self.get_height() // 5
        circle_left = (self.value - self.min) / (self.max - self.min) * (self.screen_rect.width - circle_size)
        circle_top = top - circle_size // 2

        return pygame.Rect(circle_left, circle_top, circle_size, circle_size)

    def draw(self):
        self.surface.fill(BACKGROUND_COLOR)
        # Line
        line_width = self.get_height() // 8
        top = self.get_height() // 2 - line_width // 2


        line_rect = pygame.Rect(0, top, self.surface.get_width(), line_width)
        pygame.draw.rect(self.surface, BORDER_COLOR, line_rect)

        self.circle_rect = self.__get_circle_rect()

        circle = loader.LOADED_IMAGES[SLIDER_CIRCLE]
        circle = pygame.transform.scale(circle, self.circle_rect.size)
        self.surface.blit(circle, self.circle_rect)


    def get_value(self):
        return int(self.value)