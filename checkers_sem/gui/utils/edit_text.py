import pygame

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.constants import DEFAULT_FONT, FIRST_BORDER_WIDTH, BACKGROUND_COLOR, BORDER_GAP, DEFAULT_TEXT_COLOR

class EditText(Widget):
    def __init__(self, surface : pygame.surface, left_top : tuple[int, int], string : str | int | float, font_size : int = DEFAULT_FONT_SIZE):
        super().__init__(surface, left_top)

        self.font_size = font_size
        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)
        self.string = str(string)

        self.editing = False

    def set_string(self, string : str | int | float):
        self.string = str(string)

    def get_string(self) -> str:
        return self.string

    def handle_event(self, event : pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.editing = self.screen_rect.collidepoint(pygame.mouse.get_pos())

        if event.type == pygame.KEYDOWN and self.editing:
            if event.key == pygame.K_BACKSPACE and len(self.string) > 0:
                self.string = self.string[:-1]

            if event.unicode.isdigit():
                self.string = self.string + str(event.unicode)

            if len(self.string) < 2:
                self.string = '0.'

            if len(self.string) > 5:
                self.string = self.string[:5]

            self.draw()

    def draw(self):
        self.draw_one_border(self.surface.get_rect(), FIRST_BORDER_WIDTH, BORDER_GAP)
        self.surface.fill(BACKGROUND_COLOR, self.rect_without_border)
        text = self.font.render(self.string, True, DEFAULT_TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect_without_border.center)
        self.surface.blit(text, text_rect)