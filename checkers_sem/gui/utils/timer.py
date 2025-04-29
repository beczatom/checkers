from checkers_sem.gui.utils.widget import *

def seconds_to_string(seconds : float) -> str:
    return f'{int(seconds) // 60:02} : {int(seconds) % 60:02}'

class Timer(Widget):
    def __init__(self, surface : pygame.Surface, left_top : tuple[int, int], **kwargs):
        super().__init__(surface, left_top)

        self.background_color = kwargs.get('background_color', BACKGROUND_COLOR)

        self.first_border = kwargs.get('first_border', False)
        self.second_border = kwargs.get('second_border', False)

        if not self.first_border and self.second_border:
            raise Exception('second_border cannot be True if first_border is False')

        if self.first_border:
            self.draw_border()

        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)

        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)

    def draw(self, seconds : float):
        self.draw_border()
        text = self.font.render(seconds_to_string(seconds), True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)
