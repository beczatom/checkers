"""
This module tests genetic
"""

import copy
from unittest.mock import patch
import pytest
import multiprocessing as mp
import sys
import numpy as np
from networkx import NetworkXError

from app.genetic.genetic_player import GeneticPlayer
from app.utils.state import state
from app.genetic.constants import STATS_SIZE
from app.genetic.genetic import (Genetic, crossover_ox, crossover_avg, crossover_players, play_process,
                                 tournament_process)


def test_crossover_ox():
    """
    Tests crossover ox
    """
    for _ in range(5):
        first = GeneticPlayer(np.random.rand(STATS_SIZE))
        first.coefs /= np.sum(first.coefs)
        second = GeneticPlayer(np.random.rand(STATS_SIZE))
        second.coefs /= np.sum(second.coefs)

        div_point = np.random.randint(0, STATS_SIZE + 1, dtype=int)

        with patch('numpy.random.randint', return_value=div_point):
            child = crossover_ox(first, second)

        assert np.sum(child.coefs) - 1 < 1e-3

        sum_child = sum(first.coefs[0:div_point])
        sum_child += sum(second.coefs[div_point:])

        for i in range(0, div_point):
            assert first.coefs[i] / sum_child - child.coefs[i] < 1e-3

        for i in range(div_point, STATS_SIZE):
            assert second.coefs[i] / sum_child - child.coefs[i] < 1e-3


def test_crossover_avg():
    """
    Tests crossover avg
    """
    for _ in range(5):
        first = GeneticPlayer(np.random.rand(STATS_SIZE))
        first.coefs /= np.sum(first.coefs)
        second = GeneticPlayer(np.random.rand(STATS_SIZE))
        second.coefs /= np.sum(second.coefs)

        new_coefs = np.mean(np.array((first.coefs, second.coefs)), axis=0)
        new_coefs /= np.sum(new_coefs)

        assert np.allclose(crossover_avg(first, second).coefs, new_coefs)


def test_crossover_players():
    """
    Tests crossover players
    """
    for _ in range(5):
        first = GeneticPlayer(np.random.rand(STATS_SIZE))
        first.coefs /= np.sum(first.coefs)
        second = GeneticPlayer(np.random.rand(STATS_SIZE))
        second.coefs /= np.sum(second.coefs)

        children_num = np.random.randint(1, 5, dtype=int)

        fake_prob_output = np.linspace(0, 1, children_num)

        with (patch('numpy.random.rand', side_effect=fake_prob_output),
              patch('app.genetic.genetic.crossover_ox', return_value=1),
              patch('app.genetic.genetic.crossover_avg', return_value=2)):
            fake_children = crossover_players(first, second, children_num)

        for i in range(children_num):
            assert (fake_children[i] == 2 and 1 / 3 <= fake_prob_output[i] < 2 / 3) or \
                   (fake_children[i] == 1 and (fake_prob_output[i] < 1 / 3 or fake_prob_output[i] >= 2 / 3))


def test_play_process():
    """
    Tests play process
    """
    players_q = mp.Queue()

    for _ in range(5):
        players_q.put((1, 2))
    players_q.put(None)

    results_q = mp.Queue()

    with (patch('numpy.random.rand', return_value=1),
          patch('app.genetic.genetic.play', side_effect=[1, 1, -1, -1, 0])):
        play_process(players_q, results_q, state)

    assert results_q.get() == [1, 1, 2, 2, 1]


def test_tournament_process():
    """
    Tests tournament process
    """
    players_q = mp.Queue()

    for i in range(5):
        players_q.put(((i, 0), (i + 1, 1)))
    players_q.put(None)

    results_q = mp.Queue()

    with (patch('numpy.random.rand', return_value=1),
          patch('app.genetic.genetic.play', side_effect=[1, 1, -1, -1, 0])):
        tournament_process(players_q, results_q, state.MAX_TRAIN_DEPTH, 8)

    assert np.allclose(results_q.get(), [1, 1, 0, 1, 1.5, 0.5, 0, 0])


def test_init_population():
    """
    Test init population
    """
    state.POPULATION_SIZE = 10
    gen = Genetic()
    for i in range(10):
        assert sum(gen.population[i].coefs) - 1 < 1e-3


def test_select():
    """
    Test select
    """
    if sys.platform == 'win32':
        return

    state.POPULATION_SIZE = 10
    gen = Genetic()
    gen.population = range(10)

    with (patch('numpy.random.choice', side_effect=[(1, 5) for _ in range(10)]),
          patch('app.genetic.genetic.play', return_value=-1)):
        gen.select()

    assert np.equal(gen.population, [5 for _ in range(10)]).all()


@pytest.mark.parametrize('crossover_pct', [0.2, 0.5])
def test_crossover(crossover_pct: float):
    """
    Test crossover
    Parameters
    ----------
    crossover_pct : float
    """
    state.CROSSOVER_PCT = crossover_pct
    gen = Genetic()
    gen.population = range(state.POPULATION_SIZE)
    with (patch('numpy.random.rand', return_value=0.4),
          patch('numpy.random.randint', return_value=5),
          patch('app.genetic.genetic.crossover_players', return_value=[1, 1])):
        gen.crossover()

    if 0.4 < crossover_pct:
        assert np.equal(gen.population, [1 for _ in range(state.POPULATION_SIZE)]).all()
    else:
        assert np.equal(gen.population, [5 for _ in range(state.POPULATION_SIZE)]).all()


@pytest.mark.parametrize('mutation_pct', [0.2, 0.5])
def test_mutate(mutation_pct: float):
    """
    Tests mutation
    Parameters
    ----------
    mutation_pct : float
    """
    state.MUTATION_PCT = mutation_pct
    gen = Genetic()

    before_population = copy.deepcopy([player.coefs for player in gen.population])

    with patch('numpy.random.rand', return_value=0.4):
        gen.mutate()

    if 0.4 >= mutation_pct:
        assert np.equal([player.coefs for player in gen.population], before_population).all()


@pytest.mark.parametrize('population_size, games_num_each',
                         [
                             (5, 2), (5, 5), (5, 6), (10, 2), (10, 7), (25, 2), (25, 13), (100, 2), (100, 17)
                         ])
def test_get_games_for_best_choosing(population_size: int, games_num_each: int):
    """
    Tests get games for best choosing
    Parameters
    ----------
    population_size : int
    games_num_each : int
    """
    state.POPULATION_SIZE = population_size
    gen = Genetic()

    try:
        games_q = gen.get_games_for_best_choosing(games_num_each)
    except NetworkXError:
        if (population_size * games_num_each) % 2 == 0 and games_num_each < population_size:
            assert False
        return

    games = np.zeros(population_size)

    games_q.put(None)
    while (x := games_q.get()) is not None:
        p1, p2 = x
        games[p1[0]] += 1
        games[p2[0]] += 1

    assert np.sum(games == games_num_each) == population_size


def fake_tournament_process(players_q: mp.Queue, results: mp.Queue, depth: int, res_length: int):
    """
    Dummy function for tournaments process
    Parameters
    ----------
    players_q : mp.Queue
    results : mp.Queue
    depth : int
    res_length : int
    """
    res = [res_length]
    res.extend(res_length - i - 1 for i in range(res_length - 1))
    results.put(res)


def test_best():
    """
    Tests best
    """
    if sys.platform == 'win32':
        return

    state.POPULATION_SIZE = 4
    gen = Genetic()

    known_best = gen.population[0]

    with patch('app.genetic.genetic.tournament_process', side_effect=fake_tournament_process):
        best = gen.best()

    assert best == known_best


def test_do_iteration():
    """
    Tests do iteration
    """
    gen = Genetic()
    population_size = len(gen.population)
    with patch('app.genetic.genetic.Genetic.select', return_value=None):
        gen.do_iteration()
    assert len(gen.population) == population_size


def test_get_average_coefs():
    """
    Tests get average coefs
    """
    gen = Genetic()
    assert len(gen.get_average_coefs()) == STATS_SIZE
