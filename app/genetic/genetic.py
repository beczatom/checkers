"""
This module takes care about genetic training of players' coefficients.
"""

import multiprocessing as mp
import time
import numpy as np
from networkx.generators.random_graphs import random_regular_graph

from app.genetic.genetic_player import GeneticPlayer, play
from app.utils.state import State, state
from app.genetic.constants import STATS_SIZE, N_JOBS


def crossover_ox(first: GeneticPlayer, second: GeneticPlayer) -> GeneticPlayer:
    """
    Implements OX crossover between two players.

    Parameters
    ----------
    first : GeneticPlayer
        first parent
    second : GeneticPlayer
        second parent

    Returns
    -------
    child : GeneticPlayer
        result of OX crossover
    """

    # random range from first players coefficients (0, random)
    copy_from_first = np.random.randint(0, len(first.coefs) + 1, dtype=int)
    new_coefs = np.concatenate((first.coefs[:copy_from_first], second.coefs[copy_from_first:]))
    # normalization
    new_coefs /= np.sum(new_coefs)
    return GeneticPlayer(new_coefs)


def crossover_avg(first: GeneticPlayer, second: GeneticPlayer) -> GeneticPlayer:
    """
    Implements crossover by average between two players.

    Parameters
    ----------
    first : GeneticPlayer
        first parent
    second : GeneticPlayer
        second parent

    Returns
    -------
    child : GeneticPlayer
        result of average crossover
    """

    new_coefs = (first.coefs + second.coefs) / 2
    # normalization
    new_coefs /= np.sum(new_coefs)
    return GeneticPlayer(new_coefs)


def crossover_players(first: GeneticPlayer, second: GeneticPlayer, children_num: int = 2) -> list[GeneticPlayer]:
    """
    Implements crossover between two players.
    There are evenly distributed chance that:
        OX crossover will happen with first parent starting coefficients
        OX crossover will happen with second parent starting coefficients
        average crossover will happen

    Parameters
    ----------
    first : GeneticPlayer
        first parent
    second : GeneticPlayer
        second parent
    children_num : int
        number of children to produce

    Returns
    -------
    children : list[GeneticPlayer]
        results of crossovers
    """

    children = []

    for _ in range(children_num):
        method = np.random.rand()
        if method < 1 / 3:
            children.append(crossover_ox(first, second))
        elif method < 2 / 3:
            children.append(crossover_avg(first, second))
        else:
            # absolutely useless swap, but linter doesn't like calling it with (second, first)
            first, second = second, first
            children.append(crossover_ox(first, second))

    return children


def play_process(players_q: mp.Queue, new_generation_q: mp.Queue, current_state: State):
    """
    Playing games can be parallelized.
    While the queue with pairs of player is not empty, it starts game and pushes the winners to new generation.

    Parameters
    ----------
    players_q : mp.Queue[tuple[GeneticPlayer, GeneticPlayer]]
        player pairs to play a game
    new_generation_q : mp.Queue[list[GeneticPlayer]]
        winners participating in next generation (process pushes to that queue the winner list)
    current_state : State
        provides info about train depth
    """

    new_generation_list = []

    # for all games (shared memory with other processes)
    while (players := players_q.get()) is not None:
        # get the res
        res = play(players[0], players[1], current_state.MAX_TRAIN_DEPTH)

        # decide about winner
        match res:
            case 1:
                winner = players[0]
            case -1:
                winner = players[1]
            case _:
                # the game is a draw, but we want only one of them, so we randomly chose one
                winner = players[0]
                if np.random.rand() < 0.5:
                    winner = players[1]

        new_generation_list.append(winner)

    new_generation_q.put(new_generation_list)


def tournament_process(players_q: mp.Queue, results: mp.Queue, depth: int, res_length: int):
    """
    Does the 'tournament' used to choose the best player.

    Parameters
    ----------
    players_q : mp.Queue[ tuple [ tuple[int, GeneticPlayer], tuple[int, GeneticPlayer] ] ]
        queue of two players to play a game and their indexes (to add result to correct position in results)
    results : mp.Queue[np.array[float]]
        queue of results of the games played, the process pushes its part of the game results
    depth : int
        depth of players to decide the best move
    res_length : int
        length of results to return, on the correct positions will be the players scores,
        on the other positions will be zeros

    """

    vector_res = np.zeros(res_length)

    # while there are games to play
    while (players := players_q.get()) is not None:
        white, black = players

        res = play(white[1], black[1], depth)

        # add score to correct position
        match res:
            case 1:
                vector_res[white[0]] += 1
            case -1:
                vector_res[black[0]] += 1
            case _:
                vector_res[white[0]] += 1 / 2
                vector_res[black[0]] += 1 / 2

    # push the process part of the results
    results.put(vector_res)


class Genetic:
    """
    This class does the genetic training.
    """

    def __init__(self):
        self.population = []
        self.init_population()

    def init_population(self):
        """
        Initializes the population.
        """

        # fill the population with random players
        for _ in range(state.POPULATION_SIZE):
            random_coefs = np.random.rand(STATS_SIZE)

            # normalize coefficients
            random_coefs /= np.sum(random_coefs)
            self.population.append(GeneticPlayer(random_coefs))

    def select(self) -> None:
        """
        Does selection.
        """

        # initialize the containers
        players_q = mp.Queue()
        new_generation_q = mp.Queue()
        new_generation = []
        processes = []

        # population_size times play a game
        for _ in range(state.POPULATION_SIZE):
            # randomly choose two different players
            players_idx = np.random.choice(state.POPULATION_SIZE, size=2, replace=False)
            player1 = self.population[players_idx[0]]
            player2 = self.population[players_idx[1]]

            # put them to players queue
            players_q.put((player1, player2))

        # start N_JOBS processes
        for _ in range(N_JOBS):
            # mp.Queue.qsize() is defined in documentation as unreliable
            players_q.put(None)
            processes.append(mp.Process(target=play_process, args=(players_q, new_generation_q, state)))
            processes[-1].start()

        # join the processes, and extend the new generations by winners
        for process in processes:
            process.join()
            new_generation.extend(new_generation_q.get())

        # set the population to new
        self.population = new_generation

    def crossover(self) -> None:
        """
        Does crossover.
        """

        new_generation = []
        for i in range(int(np.ceil(state.POPULATION_SIZE / 2))):
            # children number, always two, except for the last pair if population is odd
            children_num = 1 if state.POPULATION_SIZE % 2 == 1 and i == state.POPULATION_SIZE // 2 - 1 else 2

            # if crossover will happen
            if np.random.rand() < state.CROSSOVER_PCT:
                # randomly choose parents
                parents_idx = np.random.choice(state.POPULATION_SIZE, size=2, replace=False)

                # do crossover and append children
                children = crossover_players(self.population[parents_idx[0]],
                                             self.population[parents_idx[1]],
                                             children_num)
                new_generation.extend(children)
                continue

            # if not, put random players to new generation
            for _ in range(children_num):
                new_generation.append(self.population[np.random.randint(len(self.population))])

        # set the population to children
        self.population = new_generation

    def mutate(self):
        """
        Does mutation.
        """

        for _ in range(state.POPULATION_SIZE):
            if np.random.rand() < state.MUTATION_PCT:
                # randomly pick a player
                mutant_idx = np.random.choice(state.POPULATION_SIZE)

                # to scale coeficients
                rand_scaler_vector = np.random.rand(STATS_SIZE) * 2
                new_coefs = np.multiply(self.population[mutant_idx].coefs, rand_scaler_vector)

                # normalize
                self.population[mutant_idx].coefs = new_coefs / np.sum(new_coefs)

    def get_games_for_best_choosing(self, games_num_each: int) -> mp.Queue:
        """
        Returns games needed to choose the best player in the population.

        Raises
        -------
        error : NetworkXError
            If the population is less than two players.

        Returns
        -------
        games : mp.Queue[ tuple[ tuple[int, GeneticPlayer], tuple[int, GeneticPlayer] ] ]
            pair of players and their indexes in population list
        """

        games_q = mp.Queue()

        # each player will play two games (if there are only two players then just one)
        # for less than two players the function will rightfully raise an error
        # games_num_each = 1 if len(self.population) <= 2 else 2

        graph = random_regular_graph(d=games_num_each, n=len(self.population))

        # fill the queue with games
        for player_idx_comb in list(graph.edges()):
            players = ((player_idx_comb[0], self.population[player_idx_comb[0]]),
                       (player_idx_comb[1], self.population[player_idx_comb[1]]))
            games_q.put(players)

        return games_q

    def best(self) -> GeneticPlayer:
        """
        Because we do not have evaluation function, we need to choose the best player differently.
        We use a tournament for that (kind of Squid game).
        Each player in population will firstly play two random games.
        The lowest scoring players will be eliminated.
        When all the players have same score, we do everybody against everybody.
        Then pick the one with the highest score (if there are more, we just pick one of them) and return it.

        Notes
        -------
        This isn't the fairest algorithm,
        but in this way we can quickly reduce the population.

        Returns
        -------
        best_player : GeneticPlayer
            the winner of this tournament.
        """

        # equal scores
        all_equal = False

        # if we already reduced the population to one, we can return the last one
        while len(self.population) != 1:
            # initialization
            processes = []
            results = np.zeros(len(self.population))
            results_q = mp.Queue()

            # everybody plays two games,
            # except when we had equal scores or only two players left (then everybody against everybody)
            games_each = len(self.population) - 1 if all_equal or len(self.population) <= 2 else 2
            games_q = self.get_games_for_best_choosing(games_each)

            # start the tournament processes
            for _ in range(N_JOBS):
                games_q.put(None)
                processes.append(mp.Process(target=tournament_process,
                                            args=(games_q, results_q, state.MAX_TRAIN_DEPTH, len(self.population))))
                processes[-1].start()

            # get the results from processes
            for process in processes:
                process.join()
                results += results_q.get()

            print('Results:', results)

            # getting the min indexes
            min_indexes = np.where(results == np.min(results))[0]

            if not all_equal:
                # if all are min, then the scores are equal
                if len(min_indexes) == len(self.population):
                    all_equal = True
                    continue
                # dropping the minimal scorers
                self.population = [player for i, player in enumerate(self.population) if i not in min_indexes]
            else:
                # getting the best scorer
                # note, np.argmax returns only one value, the first maximum
                # it could sound not as a random max, but we have no idea what's going on in the list
                # so it can be considered as random
                max_index = np.argmax(results)
                self.population = [self.population[max_index]]

            print('New population length:', len(self.population))

        return self.population[0]

    def do_iteration(self) -> list[GeneticPlayer]:
        """
        Does one iteration of the 'training'.

        Returns
        -------
        population : list[GeneticPlayer]
            The population after one iteration of the 'training'.
        """

        self.print()
        self.select()
        self.crossover()
        self.mutate()
        return self.population

    def get_average_coefs(self) -> list[float]:
        """
        Returns average coefficients in current population.

        Returns
        -------
        coefs : list[float]
            average coefficients of players in population
        """

        sum_coefs = 0
        for player in self.population:
            sum_coefs += player.coefs
        return sum_coefs / len(self.population)

    def do(self) -> None:
        """
        Does the 'training'.
        Except for choosing best,
        because the lack of evaluation function,
        we will need to do it separately.
        """

        avgs = []
        for i in range(state.GENERATIONS):
            print(f'Average coefficients before {i + 1}. iteration :')
            print(self.get_average_coefs())
            avgs.append(self.get_average_coefs())
            self.select()
            self.crossover()
            if i != state.GENERATIONS - 1 :
                self.mutate()
        np.save("avg_genotypes_three.npy", avgs)

    def print(self) -> None:
        """
        Basic printing of players in current population.
        """

        for player in self.population:
            print(player)


if __name__ == "__main__":
    # WSL and Windows sometimes keeps stopping processes with 'fork' mode
    # mp.set_start_method('spawn')

    gen = Genetic()
    start = time.time()
    gen.do()
    print('Starting to choose best:', time.time() - start, 's')
    best = gen.best()
    print('ALL DONE:', time.time() - start, 's')
    print(50 * '-')
    print('Best:', best)
