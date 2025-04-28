from checkers_sem.constants import *


class State:
    def __init__(self):
        self.POPULATION_SIZE = POPULATION_SIZE
        self.GENERATIONS = GENERATIONS
        self.MAX_TRAIN_DEPTH = MAX_TRAIN_DEPTH
        self.CROSSOVER_PCT = CROSSOVER_PCT
        self.MUTATION_PCT = MUTATION_PCT

    def get_genetic_settings(self):
        return [self.POPULATION_SIZE, self.GENERATIONS, self.MAX_TRAIN_DEPTH, self.CROSSOVER_PCT, self.MUTATION_PCT]

    # global POPULATION_SIZE = constants.POPULATION_SIZE
    # global GENERATIONS = GENERATIONS
    # global MAX_TRAIN_DEPTH = MAX_TRAIN_DEPTH
    # global CROSSOVER_PCT = CROSSOVER_PCT
    # global MUTATION_PCT = MUTATION_PCT


state = State()