from checkers_sem.genetic.genetic_player import *
from checkers_sem.constants import *
from checkers_sem.state import *

import time

import multiprocessing as mp

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
    if method < 1/3:
        return crossover_ox(first, second)
    elif method < 2/3:
        return crossover_avg(first, second)

    return crossover_ox(second, first)

def play_process(fighter1 : GeneticPlayer, fighter2 : GeneticPlayer, new_generation : mp.Queue, sem : mp.Semaphore, state : State ):
    res = play(fighter1, fighter2, state.MAX_TRAIN_DEPTH)
    match res:
        case 1, 0:
            winner = fighter1
        case 0, 1:
            winner = fighter2
        case _:
            random_player = np.random.rand()
            if random_player < 0.5:
                winner = fighter1
            else:
                winner = fighter2
    new_generation.put(winner)
    sem.release()

def tournament_process(fighter1 : tuple[int, GeneticPlayer], fighter2 : tuple[int, GeneticPlayer], results : mp.Queue, sem : mp.Semaphore, state : State ):
    res = play(fighter1[1], fighter2[1], state.MAX_TRAIN_DEPTH)
    vector_res = np.zeros(state.POPULATION_SIZE)
    match res:
        case 1, 0:
            vector_res[fighter1[0]] = 1
        case 0, 1:
            vector_res[fighter2[0]] = 1
        case _:
            vector_res[fighter1[0]] = 1/2
            vector_res[fighter2[0]] = 1/2
    results.put(vector_res)
    sem.release()

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
        new_generation_q = mp.Queue()
        new_generation = []
        processes = []
        sem = mp.Semaphore(N_JOBS)

        for _ in range(state.POPULATION_SIZE):
            fighters_idx = np.random.choice(state.POPULATION_SIZE, size=2, replace=False)
            fighter1 = self.population[fighters_idx[0]]
            fighter2 = self.population[fighters_idx[1]]

            sem.acquire()
            processes.append(mp.Process(target=play_process, args=(fighter1, fighter2, new_generation_q, sem, state)))
            processes[-1].start()

            for k, process in enumerate(processes):
                if process.exitcode is not None:
                    new_generation.append(new_generation_q.get())
                    process.join()
                    processes.remove(process)


        for process in processes:
            new_generation.append(new_generation_q.get())
            process.join()

        self.population = new_generation


    def crossover(self):
        new_generation = []
        for _ in range(state.POPULATION_SIZE):
            will_be_crossed = np.random.rand()
            if will_be_crossed < state.CROSSOVER_PCT:
                parents_idx = np.random.choice(state.POPULATION_SIZE, size=2, replace=False)
                child = crossover_players(self.population[parents_idx[0]], self.population[parents_idx[1]])
                new_generation.append(child)
                continue

            new_generation.append(self.population[np.random.randint(len(self.population))])

        self.population = new_generation

    def mutate(self):
        for _ in range(state.POPULATION_SIZE):
            will_be_mutated = np.random.rand()
            if will_be_mutated < state.MUTATION_PCT:
                mutant_idx = np.random.choice(state.POPULATION_SIZE)
                rand_scaler_vector = np.random.rand(STATS_SIZE) * 2
                new_coefs = np.multiply(self.population[mutant_idx].coefs, rand_scaler_vector)
                self.population[mutant_idx].coefs = new_coefs / np.sum(new_coefs)

    def best(self) -> GeneticPlayer:
        sem = mp.Semaphore(N_JOBS)
        processes = []

        results = np.zeros(state.POPULATION_SIZE)
        print('state population size', state.POPULATION_SIZE)
        results_queue = mp.Queue()

        for i in range(state.POPULATION_SIZE):
            for j in range(i + 1, state.POPULATION_SIZE):

                white_idx, black_idx = i, j
                if i % 2 == 0:
                    white_idx, black_idx = j, i

                sem.acquire()
                processes.append(
                    mp.Process(target=tournament_process,
                               args=((white_idx, self.population[white_idx]),
                                     (black_idx, self.population[black_idx]),
                                     results_queue, sem, state)))
                processes[-1].start()

                for k, process in enumerate(processes):
                    if process.exitcode is not None:
                        print('All: ', results)
                        results += results_queue.get()

                        process.join()
                        processes.remove(process)


        for process in processes:
            results += results_queue.get()
            print(results)
            process.join()

        print(20*'-')
        print(results_queue.qsize())
        print(self.population[np.argmax(results)])

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
            self.print()

            self.select()
            self.crossover()
            self.mutate()

    # FIXME test
    def print(self):
        for player in self.population:
            print(player)

if __name__ == "__main__":
    GENERATIONS = 5
    POPULATION_SIZE = 16
    MUTATION_PCT = 0.1
    CROSSOVER_PCT = 0.8


    for i in range(1, 11):
        MAX_TRAIN_DEPTH = i
        print(f'START {i}: ')
        start = time.time()
        for j in range(GENERATIONS):
            Genetic().do_iteration()
        print(f'DONE {i}: ', time.time() - start)


    # gen = Genetic()
    # start = time.time()
    # gen.do()
    # print('GEN DONE:', time.time() - start)
    # print(gen.best())
    # print('DONE:', time.time() - start)

