import pygame

from checkers_sem.gui.constants import BACKGROUND_COLOR, BORDER_COLOR
from checkers_sem.gui.utils.progress_bar import ProgressBar
from checkers_sem.gui.utils.pos import Pos


def test_init():
    surface = pygame.Surface((100, 100))
    surface.fill(BACKGROUND_COLOR)

    pos = Pos((0.5, 0.5), (0, 0, 0, 0), center=True)
    bar = ProgressBar(surface, pos, value=0.01)

    assert bar.value == 0.01
    assert surface.get_rect().center == (50, 50)
    assert surface.get_at((25, 25)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((74, 74)) == pygame.Color(BORDER_COLOR)
    assert surface.get_at((50, 50)) == pygame.Color(BACKGROUND_COLOR)
