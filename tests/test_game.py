from checkers_sem.game.game import Game
import copy

def test_legal_moves():
    game = Game()

    while moves := game.get_moves():
        game_bef = copy.deepcopy(game)

        move = next(moves)

        game.push(move)
        game.pop()

        assert game_bef == game

        game.push(move)

        if game.get_result() is not None:
            break
