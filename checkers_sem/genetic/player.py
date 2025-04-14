from checkers_sem.game.game import *

class Player:
    def __init__(self, coefs : np.array):
        self.coefs = np.array(coefs, dtype=np.float64)
