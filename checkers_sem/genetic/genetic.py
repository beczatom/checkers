
import multiprocessing as mp
import time

from checkers_sem.genetic.genetic_player import *
from checkers_sem.state import *
from itertools import combinations


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
            case 1, 0:
                winner = players[0]
            case 0, 1:
                winner = players[1]
            case _:
                winner = players[0]
                if np.random.rand() < 0.5:
                    winner = players[1]

        new_generation_list.append(winner)
    new_generation_q.put(new_generation_list)


def tournament_process(players_q : mp.Queue, results : mp.Queue, state : State ):
    vector_res = np.zeros(state.POPULATION_SIZE)

    while (players := players_q.get()) is not None:
        white, black = players
        if np.random.rand() > 0.5:
            white, black = black, white

        res = play(white[1], black[1], state.MAX_TRAIN_DEPTH)

        match res:
            case 1, 0:
                vector_res[white[0]] += 1
            case 0, 1:
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

    def best(self) -> GeneticPlayer:
        processes = []

        players_q = mp.Queue()
        results = np.zeros(state.POPULATION_SIZE)
        results_q = mp.Queue()

        player_indexes = combinations(range(POPULATION_SIZE), 2)

        for players in [((i, self.population[i]), (j, self.population[j])) for i, j in player_indexes]:
            players_q.put(players)

        for _ in range(N_JOBS):
            players_q.put(None)
            processes.append(mp.Process(target=tournament_process, args=(players_q, results_q, state)))
            processes[-1].start()

        for process in processes:
            process.join()
            results += results_q.get()
            print(results)

        return self.population[np.argmax(results)]

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

