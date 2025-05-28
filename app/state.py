"""
This module holds some global variables for windows.
"""

from app.genetic.constants import POPULATION_SIZE, GENERATIONS, MAX_TRAIN_DEPTH, CROSSOVER_PCT, MUTATION_PCT, AI_COEFS
from app.gui.constants import TIME

# it is necessary to have many attributes for state class, it wouldn't be nice if I put them to a list
class State: # pylint: disable=too-many-instance-attributes
    """
    This class holds some global variables for windows initialized by constants files.
    """

    def __init__(self):
        """
        Initializes variables.
        """
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

    def get_genetic_settings(self) -> list[int]:
        """
        Gets genetic settings.
        Returns
        -------
        genetic_settings : list[int]
            setting for training
        """
        return [self.POPULATION_SIZE, self.GENERATIONS, self.MAX_TRAIN_DEPTH, self.CROSSOVER_PCT, self.MUTATION_PCT]

    def useless(self) -> None:
        """
        Absolutely useless, because can be directly accessed,
        but pylint wouldn't survive if there wasn't two public methods.
        """
        print('I\'m useless')


state = State()
