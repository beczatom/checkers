from checkers_sem.game.game import *

class Player:
    def __init__(self, coefs : np.array):
        self.coefs = np.array(coefs, dtype=np.float64)

    def evaluate(self, game : Game) -> float:
        possible_res = game.get_result()

        if possible_res is not None:
            if possible_res[0] == 1: return np.inf
            if possible_res[1] == 1: return -np.inf
            return 0

        return np.dot(self.coefs, game.board.stats())

