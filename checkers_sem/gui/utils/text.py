
from checkers_sem.gui.utils.widget import *

class Text(Widget):
    def __init__(self, surface : pygame.surface, left_top : tuple[int, int], string : str | int | float, font_size : int = DEFAULT_FONT_SIZE):
        super().__init__(surface, left_top)

        self.font_size = font_size
        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)
        self.string = str(string)

    def set_string(self, string : str | int | float):
        self.string = str(string)

    def draw(self):
        self.surface.fill(BACKGROUND_COLOR)
        text = self.font.render(self.string, True, DEFAULT_TEXT_COLOR)
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)