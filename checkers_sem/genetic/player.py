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

    def alpha_beta(self, game : Game, alpha : float, beta : float, depth : int) -> tuple[Move, float]:
        # FIXME duplicita get_result()
        if depth == 0 or game.get_result() is not None:
            return game.peek(), self.evaluate(game)

        if game.board.turn == Turn.WHITE:
            # pair of move and evaluation of that move
            best_move = (None, -np.inf)

            for move in game.board.get_legal_moves():
                game.push(move)
                possible_best = self.alpha_beta(game, alpha, beta, depth - 1)
                game.pop()

                if best_move[1] <= possible_best[1]:
                    best_move = (move, possible_best[1])
                    alpha = possible_best[1]

                if alpha >= beta:
                    break

        else:
            # pair of move and evaluation of that move
            best_move = (None, np.inf)
            for move in game.board.get_legal_moves():
                game.push(move)
                possible_best = self.alpha_beta(game, alpha, beta, depth - 1)
                game.pop()

                if best_move[1] >= possible_best[1]:
                    best_move = (move, possible_best[1])
                    beta = possible_best[1]

                if alpha >= beta:
                    break

        return best_move

    # returns true if lost for no possible moves or None if the game is currently undecided
    def move(self, game : Game, depth : int):
        best = self.alpha_beta(game, -np.inf, np.inf, depth)

        # if player can not move, he loses
        # the player 'knows' about this, since best[0] is None implies best[1] = np.inf or -np.inf respectively
        # (there was no change in sons exploration)
        # so he tries to avoid it as much as possible
        if best[0] is None:
            return True

        game.push(best[0])

def play(white : Player, black : Player, depth : int ) -> tuple[float, float]:
    if np.array_equal(white.coefs, black.coefs):
        return 1/2, 1/2

    game = Game()

    while (res := game.get_result()) is None:
        if game.board.turn == Turn.WHITE:
            if white.move(game, depth):
                return 0, 1
        else:
            if black.move(game, depth):
                return 1, 0

    return res
