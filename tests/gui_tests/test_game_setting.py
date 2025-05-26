"""
This module defines a windows responsible for game settings
"""

import pygame

from checkers_sem.gui.game_setting.game_setting_widget import GameSettingWidget
from checkers_sem.gui.game_setting.game_setting_ai_vs_ai import GameSettingAIVSAI
from checkers_sem.gui.game_setting.game_setting_human_vs_human import GameSettingHumanVSHuman
from checkers_sem.gui.game_setting.game_setting_human_vs_ai import GameSettingHumanVSAI
from checkers_sem.gui.constants import START_TRAIN_BUTTON_TEXT, HUMAN_VS_HUMAN_TEXT, HUMAN_VS_PC_TEXT, PC_VS_PC_TEXT, \
    BACKGROUND_COLOR, TIME_SLIDER_TEXT, DEPTH_BLACK_TEXT, DEPTH_WHITE_TEXT, COEFICIENTS_TEXT, STAT_TEXTS
from checkers_sem.genetic.constants import AI_COEFS
from checkers_sem.gui.utils.pos import Pos
from checkers_sem.state import state

from checkers_sem.gui.game_setting.game_setting_window import GameSettingWindow

def test_game_setting_window() -> None:
    """
    Game setting window testing
    """
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    game_setting_window = GameSettingWindow(surface)
    assert game_setting_window.surface == surface
    assert game_setting_window.start_button is not None
    assert game_setting_window.start_button.text == START_TRAIN_BUTTON_TEXT
    assert len(game_setting_window.mode_buttons) == 3

    for i, button_text in enumerate([HUMAN_VS_HUMAN_TEXT, HUMAN_VS_PC_TEXT, PC_VS_PC_TEXT]):
        assert game_setting_window.mode_buttons[i].text == button_text

def test_game_setting_widget() -> None:
    """
    Game setting widget testing
    """
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    pos = Pos((1, 1), (0, 0, 0, 0), center=True)

    game_setting_widget = GameSettingWidget(surface, pos)
    assert game_setting_widget.time_header_text.text == TIME_SLIDER_TEXT
    assert game_setting_widget.time_slider_val is not None
    assert game_setting_widget.time_slider.get_value() == state.TIME


def test_game_setting_human_vs_human() -> None:
    """
    Game setting human vs human widget testing
    """
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    pos = Pos((1, 1), (0, 0, 0, 0), center=True)

    game_setting_human_vs_human = GameSettingHumanVSHuman(surface, pos)
    assert game_setting_human_vs_human.time_header_text.text == TIME_SLIDER_TEXT
    assert game_setting_human_vs_human.time_slider_val is not None
    assert game_setting_human_vs_human.time_slider.get_value() == state.TIME

    assert game_setting_human_vs_human.depth_header.text == DEPTH_BLACK_TEXT
    assert game_setting_human_vs_human.depth_text_val is not None
    assert game_setting_human_vs_human.depth_slider.get_value() == state.DEPTH_BLACK

    assert game_setting_human_vs_human.coefs_header.text == COEFICIENTS_TEXT

    for i, text in enumerate(STAT_TEXTS):
        assert game_setting_human_vs_human.coefs_edit_texts_headers[i].text == text

    for i, value in enumerate(AI_COEFS):
        assert game_setting_human_vs_human.coefs_edit_texts[i].get_string() == str(value)

def test_game_setting_human_vs_ai() -> None:
    """
    Game setting human vs AI widget testing
    """
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    pos = Pos((1, 1), (0, 0, 0, 0), center=True)

    game_setting_human_vs_ai = GameSettingHumanVSAI(surface, pos)
    assert game_setting_human_vs_ai.time_header_text.text == TIME_SLIDER_TEXT
    assert game_setting_human_vs_ai.time_slider_val is not None
    assert game_setting_human_vs_ai.time_slider.get_value() == state.TIME

    assert game_setting_human_vs_ai.depth_header.text == DEPTH_BLACK_TEXT
    assert game_setting_human_vs_ai.depth_text_val is not None
    assert game_setting_human_vs_ai.depth_slider.get_value() == state.DEPTH_BLACK

    assert game_setting_human_vs_ai.coefs_header.text == COEFICIENTS_TEXT

    for i, text in enumerate(STAT_TEXTS):
        assert game_setting_human_vs_ai.coefs_edit_texts_headers[i].text == text

    for i, value in enumerate(AI_COEFS):
        assert game_setting_human_vs_ai.coefs_edit_texts[i].get_string() == str(value)

def test_game_setting_ai_vs_ai() -> None:
    """
    Game setting AI vs AI widget testing
    """
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    pos = Pos((1, 1), (0, 0, 0, 0), center=True)

    game_setting_ai_vs_ai = GameSettingAIVSAI(surface, pos)
    assert game_setting_ai_vs_ai.time_header_text.text == TIME_SLIDER_TEXT
    assert game_setting_ai_vs_ai.time_slider_val is not None
    assert game_setting_ai_vs_ai.time_slider.get_value() == state.TIME

    assert game_setting_ai_vs_ai.depth_black_slider[0].text == DEPTH_BLACK_TEXT
    assert game_setting_ai_vs_ai.depth_black_slider[1] is not None
    assert game_setting_ai_vs_ai.depth_black_slider[2].get_value() == state.DEPTH_BLACK

    assert game_setting_ai_vs_ai.depth_white_slider[0].text == DEPTH_WHITE_TEXT
    assert game_setting_ai_vs_ai.depth_white_slider[1] is not None
    assert game_setting_ai_vs_ai.depth_white_slider[2].get_value() == state.DEPTH_WHITE

    assert game_setting_ai_vs_ai.coefs_header.text == COEFICIENTS_TEXT

    for i, text in enumerate(STAT_TEXTS):
        assert game_setting_ai_vs_ai.coefs_edit_texts_headers[i].text == text

    for i, value in enumerate(AI_COEFS):
        assert game_setting_ai_vs_ai.coefs_white_edit_texts[i].get_string() == str(value)
        assert game_setting_ai_vs_ai.coefs_black_edit_texts[i].get_string() == str(value)
