import pygame

from checkers_sem.constants import *

class Window:
    def __init__(self, surface : pygame.surface):
        self.surface = surface
        self.surface.fill(BACKGROUND_COLOR)

    def show(self):
        raise Exception('Pure virtual method')
