"""
This module tests genetic GUI.
"""

import numpy as np

import pygame

from checkers_sem.gui.constants import BACKGROUND_COLOR, SLIDER_PROPERTIES
from checkers_sem.gui.genetic_window.genetic_window import GeneticWindow
from checkers_sem.gui.genetic_window.genetic_setting_window import GeneticSettingWindow
from checkers_sem.gui.genetic_window.genetic_helper import GeneticHelper
from checkers_sem.state import state


def test_genetic_window() -> None:
    """
    Tests the GeneticWindow class.
    """
    state.GENERATIONS = 3
    state.MAX_TRAIN_DEPTH = 1
    state.POPULATION_SIZE = 8

    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    gen_window = GeneticWindow(surface)

    assert gen_window.surface == surface
    assert gen_window.genetic_helper is not None
    assert gen_window.progress_bar is not None
    assert gen_window.settings is not None
    assert gen_window.coefs is not None

    assert gen_window.genetic_helper.genetic_thread is not None
    gen_window.genetic_helper.genetic_thread.join()

def test_genetic_setting_window() -> None:
    """
    Tests the GeneticSettingWindow class.
    """
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    gen_setting_window = GeneticSettingWindow(surface)

    assert gen_setting_window.surface == surface
    assert len(gen_setting_window.genetic_settings) == 5
    assert len(gen_setting_window.slider_headers) == 5
    assert len(gen_setting_window.slider_text_vals) == 5
    assert len(gen_setting_window.sliders) == 5
    assert gen_setting_window.awaited_time is not None
    assert gen_setting_window.awaited_time_header is not None
    assert gen_setting_window.start_button is not None

    for i, slider_prop in enumerate(SLIDER_PROPERTIES):
        ref_val = slider_prop[3]
        assert gen_setting_window.sliders[i].get_value() == ref_val

    gen_setting_window.genetic_settings = range(5)
    gen_setting_window.set_global_genetic_settings()
    for i, state_val in enumerate([state.POPULATION_SIZE, state.GENERATIONS, state.MAX_TRAIN_DEPTH, state.CROSSOVER_PCT, state.MUTATION_PCT]):
        assert state_val == gen_setting_window.genetic_settings[i]

def test_genetic_helper() -> None:
    """
    Tests the GeneticHelper.
    """
    state.POPULATION_SIZE = 8
    state.GENERATIONS = 3
    state.MAX_TRAIN_DEPTH = 1

    genetic_helper = GeneticHelper()

    assert genetic_helper.genetic is not None
    assert genetic_helper.current_generation == 0
    assert genetic_helper.genetic_thread is not None
    assert genetic_helper.best_queue is not None
    assert genetic_helper.best_player is None
    assert len(genetic_helper.average_coefs) == 6

    while genetic_helper.best_player is None:
        genetic_helper.check_thread()
        assert genetic_helper.current_generation <= state.GENERATIONS

    assert genetic_helper.current_generation == state.GENERATIONS
    assert genetic_helper.genetic_thread is None
    assert np.allclose(genetic_helper.get_coefs(), genetic_helper.best_player.coefs, atol=1e-3)
