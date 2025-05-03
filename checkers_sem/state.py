from checkers_sem.constants import *


class State:
    def __init__(self):
        self.POPULATION_SIZE = POPULATION_SIZE
        self.GENERATIONS = GENERATIONS
        self.MAX_TRAIN_DEPTH = MAX_TRAIN_DEPTH
        self.CROSSOVER_PCT = CROSSOVER_PCT
        self.MUTATION_PCT = MUTATION_PCT

        self.DEPTH_WHITE = MAX_TRAIN_DEPTH
        self.DEPTH_BLACK = MAX_TRAIN_DEPTH
        self.COEFS_BLACK = AI_COEFS
        self.COEFS_WHITE = AI_COEFS
        self.TIME = TIME

    def get_genetic_settings(self):
        return [self.POPULATION_SIZE, self.GENERATIONS, self.MAX_TRAIN_DEPTH, self.CROSSOVER_PCT, self.MUTATION_PCT]


state = State()