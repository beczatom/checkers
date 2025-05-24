import pygame

from checkers_sem.gui.constants import BACKGROUND_COLOR, BAR_IMAGE
from checkers_sem.gui.utils.widget import Widget

class Bar(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.value = kwargs.get('value', 0)

        self.draw_border()

        self.background_color = BACKGROUND_COLOR
        self.bar_image = BAR_IMAGE
        self.bar_image = pygame.image.load(BAR_IMAGE).convert_alpha()

    def set_value(self, value):
        self.value = value

    def draw(self):
        self.draw_border()
        top, left = self.rect_without_border.topleft
        size_y = self.rect_without_border.height
        size_x = int(self.rect_without_border.width * self.value)
        img_rect = pygame.Rect(left, top, size_x, size_y)
        self.surface.blit(self.bar_image, img_rect, area=img_rect)
