from checkers_sem.genetic.constants import POPULATION_SIZE, GENERATIONS, MAX_TRAIN_DEPTH, CROSSOVER_PCT, MUTATION_PCT
from checkers_sem.gui.constants import TIME

class State:
    def __init__(self):
        self.POPULATION_SIZE = POPULATION_SIZE
        self.GENERATIONS = GENERATIONS
        self.MAX_TRAIN_DEPTH = MAX_TRAIN_DEPTH
        self.CROSSOVER_PCT = CROSSOVER_PCT
        self.MUTATION_PCT = MUTATION_PCT

        self.DEPTH_WHITE = MAX_TRAIN_DEPTH
        self.DEPTH_BLACK = MAX_TRAIN_DEPTH
        self.COEFS_BLACK = [0.37, 0.26, 0.112, 0.065, 0.118, 0.076]
        self.COEFS_WHITE = [0.182, 0.355, 0.07, 0.137, 0.188, 0.069]
        self.TIME = TIME

    def get_genetic_settings(self):
        return [self.POPULATION_SIZE, self.GENERATIONS, self.MAX_TRAIN_DEPTH, self.CROSSOVER_PCT, self.MUTATION_PCT]


state = State()