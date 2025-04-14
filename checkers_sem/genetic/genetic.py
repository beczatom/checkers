from checkers_sem.genetic.player import *
from checkers_sem.constants import *


class Genetic:
    def __init__(self):
        self.population = []
        self.init_population()

    def init_population(self):
        for _ in range(POPULATION_SIZE):
            random_coefs = np.random.randint(1, 10, size=STATS_SIZE)
            self.population.append(Player(random_coefs))

