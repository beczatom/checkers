import pygame

from unittest.mock import patch

from app.gui.utils.chessboard import ChessBoard
from app.genetic.constants import AI_COEFS
from app.game.game import Game
from app.gui.utils.pos import Pos
from app.game.constants import BitBoard, Color
from app.gui.constants import BACKGROUND_COLOR
from app.player.player import AIPlayer, HumanPlayer


def test_move_ai_player():
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    game = Game()
    pos = Pos((1, 1), (0, 0, 0, 0))
    chessboard = ChessBoard(surface, pos, game=game)

    board_before = hash(game.board)
    ai_player = AIPlayer(AI_COEFS, chessboard)
    no_moves, performed, best = ai_player.move()

    assert performed
    assert best is not None
    assert not no_moves

    assert board_before != hash(game.board)


def test_move_human_player():
    surface = pygame.Surface((800, 800))
    surface.fill(BACKGROUND_COLOR)
    game = Game()
    pos = Pos((1, 1), (0, 0, 0, 0))
    chessboard = ChessBoard(surface, pos, game=game)

    board_before = hash(game.board)
    human_player = HumanPlayer(chessboard)

    performed = False
    best = None
    no_moves = True

    with patch('app.gui.utils.chessboard.ChessBoard.get_clicked_mask',
               side_effect=[BitBoard(0x00000100), BitBoard(0x00001000)]):
        for _ in range(2):
            no_moves, performed, best = human_player.move()

    assert performed
    assert best is None
    assert not no_moves

    assert board_before != hash(game.board)
    assert game.board.turn == Color.BLACK
    assert game.board.white == BitBoard(0x00001eff)
    assert game.board.black == BitBoard(0xfff00000)
    assert game.board.pawns == BitBoard(0xfff01eff)
