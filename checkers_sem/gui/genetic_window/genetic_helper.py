"""
This module helps with performing genetic train
"""

from threading import Thread
import queue

from checkers_sem.genetic.genetic import Genetic
from checkers_sem.helper import do_one_generation_thread, get_genetic_completion, choose_best_thread
from checkers_sem.state import state


class GeneticHelper:
    """
    This class helps GeneticWindow perform genetic train
    """

    def __init__(self):
        """
        Initialise the genetic helper
        """
        self.genetic = Genetic()
        self.current_generation = 0
        self.genetic_thread = Thread(target=do_one_generation_thread, args=(self.genetic,))
        self.genetic_thread.start()
        self.best_queue = queue.Queue()
        self.best_player = None
        self.average_coefs = self.genetic.get_average_coefs()

    def get_coefs(self) -> list[float]:
        """
        Gets average coefficients if training or the best if finished picking the best
        Returns
        -------
        coefs : list[float]
            coefficients of the current generation or the best player
        """
        if self.best_player is None:
            return [round(value, 3) for value in self.average_coefs]
        return [round(value, 3) for value in self.best_player.coefs]

    def get_completed_pct(self) -> float:
        """
        Gets how much of the work was done.
        Returns
        -------
        pct : float
            percentage of the work done
        """
        return 1 if self.best_player else get_genetic_completion(self.current_generation)

    def check_thread(self) -> None:
        """
        Checks if genetic thread is running,
        if not then visualizes the partial results and,
        if necessary, starts a new one.
        """

        # we are done or we are working -> don't disturb us
        if self.best_player or self.genetic_thread.is_alive():
            if self.best_player is not None:
                self.genetic_thread = None
            return

        self.genetic_thread.join()
        self.genetic_thread = None

        # we were choosing best
        if self.current_generation == state.GENERATIONS:
            self.best_player = self.best_queue.get()
            return

        self.average_coefs = self.genetic.get_average_coefs()

        self.current_generation += 1
        # decide whether continue training or choose best
        if self.current_generation < state.GENERATIONS:
            self.genetic_thread = Thread(target=do_one_generation_thread, args=(self.genetic,))
        else:
            self.genetic_thread = Thread(target=choose_best_thread, args=(self.genetic, self.best_queue))

        self.genetic_thread.start()
