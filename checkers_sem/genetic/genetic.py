from checkers_sem.genetic.player import *
from checkers_sem.constants import *

import multiprocessing as mp

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

