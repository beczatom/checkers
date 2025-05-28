"""
This module tests menu window
"""

import pygame

from app.gui.constants import BACKGROUND_COLOR, PLAY_BUTTON_TEXT, GENETIC_TEXT
from app.gui.menu import Menu

def test_menu() -> None:
    """
    Menu testing
    """
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    menu = Menu(surface)
    assert menu.screen == surface
    assert len(menu.buttons) == 2
    assert menu.buttons[0].text == PLAY_BUTTON_TEXT
    assert menu.buttons[1].text == GENETIC_TEXT
    assert menu.next_window is None
