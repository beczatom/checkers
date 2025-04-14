from checkers_sem.genetic.player import *
from checkers_sem.constants import *

import multiprocessing as mp

def crossover_ox(first : Player, second : Player) -> Player:
    copy_from_first = np.random.randint(0, len(first.coefs) + 1, dtype=int)
    copy_from_first = int(copy_from_first)
    new_coefs = np.concatenate((first.coefs[:copy_from_first], second.coefs[copy_from_first:]))
    return Player(new_coefs)

def crossover_avg(first : Player, second : Player) -> Player:
    return Player((first.coefs + second.coefs) / 2)

def crossover_players(first : Player, second : Player) -> Player:
    method = np.random.rand()
    if method < 1/3:
        return crossover_ox(first, second)
    elif method < 2/3:
        return crossover_avg(first, second)

    return crossover_ox(second, first)

def play_process(fighter1 : Player, fighter2 : Player, new_generation : mp.Queue, sem : mp.Semaphore):
    res = play(fighter1, fighter2, MAX_TRAIN_DEPTH)
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

def tournament_process(fighter1 : tuple[int, Player], fighter2 : tuple[int, Player], results : mp.Queue, sem : mp.Semaphore):
    res = play(fighter1[1], fighter2[1], MAX_TRAIN_DEPTH)
    vector_res = np.zeros(POPULATION_SIZE)
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
        for _ in range(POPULATION_SIZE):
            random_coefs = np.random.randint(1, 10, size=STATS_SIZE)
            self.population.append(Player(random_coefs))

    def select(self):
        new_generation_q = mp.Queue()
        new_generation = []
        processes = []
        sem = mp.Semaphore(N_JOBS)

        for _ in range(POPULATION_SIZE):
            fighters_idx = np.random.choice(POPULATION_SIZE, size=2, replace=False)
            fighter1 = self.population[fighters_idx[0]]
            fighter2 = self.population[fighters_idx[1]]

            sem.acquire()
            processes.append(mp.Process(target=play_process, args=(fighter1, fighter2, new_generation_q, sem)))
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
        for _ in range(POPULATION_SIZE):
            will_be_crossed = np.random.rand()
            if will_be_crossed < CROSSOVER_PCT:
                parents_idx = np.random.choice(POPULATION_SIZE, size=2, replace=False)
                child = crossover_players(self.population[parents_idx[0]], self.population[parents_idx[1]])
                new_generation.append(child)
                continue

            new_generation.append(self.population[np.random.randint(len(self.population))])

        self.population = new_generation

    def mutate(self):
        for _ in range(POPULATION_SIZE):
            will_be_mutated = np.random.rand()
            if will_be_mutated < MUTATION_PCT:
                mutant_idx = np.random.choice(POPULATION_SIZE)
                rand_scaler_vector = np.random.rand(STATS_SIZE) * 2
                self.population[mutant_idx].coefs = np.multiply(self.population[mutant_idx].coefs, rand_scaler_vector)

    def best(self) -> Player:
        sem = mp.Semaphore(N_JOBS)
        processes = []

        results = np.zeros(POPULATION_SIZE)
        results_queue = mp.Queue()

        for i in range(POPULATION_SIZE):
            for j in range(i + 1, POPULATION_SIZE):

                white_idx, black_idx = i, j
                if i % 2 == 0:
                    white_idx, black_idx = j, i

                sem.acquire()
                processes.append(
                    mp.Process(target=tournament_process,
                               args=((white_idx, self.population[white_idx]),
                                     (black_idx, self.population[black_idx]),
                                     results_queue, sem)))
                processes[-1].start()

                for k, process in enumerate(processes):
                    if process.exitcode is not None:
                        results += results_queue.get()
                        print(results)
                        process.join()
                        processes.remove(process)


        for process in processes:
            results += results_queue.get()
            print(results)
            process.join()

        print(20*'-')
        print(results_queue.qsize())

        return self.population[np.argmax(results)]

