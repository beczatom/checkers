
import multiprocessing as mp
import time

from networkx.generators.random_graphs import random_regular_graph

from checkers_sem.genetic.genetic_player import *
from checkers_sem.state import *


def crossover_ox(first : GeneticPlayer, second : GeneticPlayer) -> GeneticPlayer:
    copy_from_first = np.random.randint(0, len(first.coefs) + 1, dtype=int)
    copy_from_first = int(copy_from_first)
    new_coefs = np.concatenate((first.coefs[:copy_from_first], second.coefs[copy_from_first:]))
    new_coefs /= np.sum(new_coefs)
    return GeneticPlayer(new_coefs)


def crossover_avg(first : GeneticPlayer, second : GeneticPlayer) -> GeneticPlayer:
    new_coefs = (first.coefs + second.coefs) / 2
    new_coefs /= np.sum(new_coefs)
    return GeneticPlayer(new_coefs)


def crossover_players(first : GeneticPlayer, second : GeneticPlayer) -> GeneticPlayer:
    method = np.random.rand()
    if method < 2/3:
        return crossover_ox(first, second)
    elif method < 1/3:
        return crossover_avg(first, second)

    return crossover_ox(second, first)


def play_process(players_q : mp.Queue, new_generation_q : mp.Queue, state : State ):
    new_generation_list = []
    while (players := players_q.get()) is not None:
        res = play(players[0], players[1], state.MAX_TRAIN_DEPTH)
        match res:
            case 1:
                winner = players[0]
            case -1:
                winner = players[1]
            case _:
                winner = players[0]
                if np.random.rand() < 0.5:
                    winner = players[1]

        new_generation_list.append(winner)
    new_generation_q.put(new_generation_list)


def tournament_process(players_q : mp.Queue, results : mp.Queue, depth : int, res_length : int ):
    vector_res = np.zeros(res_length)

    while (players := players_q.get()) is not None:
        white, black = players
        if np.random.rand() > 0.5:
            white, black = black, white

        res = play(white[1], black[1], depth)

        match res:
            case 1:
                vector_res[white[0]] += 1
            case -1:
                vector_res[black[0]] += 1
            case _:
                vector_res[white[0]] += 1 / 2
                vector_res[black[0]] += 1 / 2
    results.put(vector_res)

class Genetic:
    def __init__(self):
        self.population = []
        self.init_population()

    def init_population(self):
        for _ in range(state.POPULATION_SIZE):
            random_coefs = np.random.rand(STATS_SIZE)
            random_coefs /= np.sum(random_coefs)
            self.population.append(GeneticPlayer(random_coefs))

    def select(self):
        players_q = mp.Queue()
        new_generation_q = mp.Queue()
        new_generation = []
        processes = []

        for _ in range(state.POPULATION_SIZE):
            fighters_idx = np.random.choice(state.POPULATION_SIZE, size=2, replace=False)
            fighter1 = self.population[fighters_idx[0]]
            fighter2 = self.population[fighters_idx[1]]
            players_q.put((fighter1, fighter2))

        for _ in range(N_JOBS):
            players_q.put(None)
            processes.append(mp.Process(target=play_process, args=(players_q, new_generation_q, state)))
            processes[-1].start()

        for process in processes:
            process.join()
            new_generation.extend(new_generation_q.get())

        self.population = new_generation


    def crossover(self):
        new_generation = []
        for _ in range(state.POPULATION_SIZE):
            if np.random.rand() < state.CROSSOVER_PCT:
                parents_idx = np.random.choice(state.POPULATION_SIZE, size=2, replace=False)
                child = crossover_players(self.population[parents_idx[0]], self.population[parents_idx[1]])
                new_generation.append(child)
                continue

            new_generation.append(self.population[np.random.randint(len(self.population))])

        self.population = new_generation

    def mutate(self):
        for _ in range(state.POPULATION_SIZE):
            if np.random.rand() < state.MUTATION_PCT:
                mutant_idx = np.random.choice(state.POPULATION_SIZE)
                rand_scaler_vector = np.random.rand(STATS_SIZE) * 2
                new_coefs = np.multiply(self.population[mutant_idx].coefs, rand_scaler_vector)
                self.population[mutant_idx].coefs = new_coefs / np.sum(new_coefs)

    def get_games_for_best_choosing(self) -> mp.Queue:
        games_q = mp.Queue()

        games_num_each = int(np.ceil(len(self.population) / 32))

        while games_num_each * len(self.population) % 2 != 0:
            games_num_each += 1
            if games_num_each >= len(self.population):
                raise RuntimeError('Regular graph : n * d must be even')

        G = random_regular_graph(d=games_num_each, n = len(self.population))

        scheduled_games_num = np.zeros(len(self.population))
        for player_idx_comb in list(G.edges()):
            scheduled_games_num[player_idx_comb[0]] += 1
            scheduled_games_num[player_idx_comb[1]] += 1
            players = ((player_idx_comb[0], self.population[player_idx_comb[0]]),
                        (player_idx_comb[1], self.population[player_idx_comb[1]]))
            games_q.put(players)

        return games_q

    def best(self) -> GeneticPlayer:

        while len(self.population) != 1:
            processes = []
            results = np.zeros(len(self.population))
            results_q = mp.Queue()
            games_q = self.get_games_for_best_choosing()

            for _ in range(min(N_JOBS, len(self.population) // 2)):
                games_q.put(None)
                processes.append(mp.Process(target=tournament_process,
                                            args=(games_q, results_q, state.MAX_TRAIN_DEPTH, len(self.population))))
                processes[-1].start()

            for process in processes:
                process.join()
                results += results_q.get()

            max_indexes = np.where(results == np.max(results))[0]

            if len(max_indexes) == len(self.population):
                break

            self.population = [self.population[i] for i in max_indexes]

        return self.population[0]

    def do_iteration(self) -> list[GeneticPlayer]:
        self.print()
        self.select()
        self.crossover()
        self.mutate()
        return self.population

    def get_average_coefs(self) -> list[float]:
        sum_coefs = 0
        for player in self.population:
            sum_coefs += player.coefs
        return sum_coefs / len(self.population)


    def do(self):
        for i in range(state.GENERATIONS):
            print(f'Before {i} it.')
            print(self.get_average_coefs())
            self.select()
            self.crossover()
            self.mutate()

    def print(self):
        for player in self.population:
            print(player)

if __name__ == "__main__":

    # mp.set_start_method('spawn')
    gen = Genetic()
    start = time.time()
    gen.do()
    print('GEN DONE:', time.time() - start)
    best = gen.best()
    print('DONE:', time.time() - start)
    print(30 * '-')
    print(best)

