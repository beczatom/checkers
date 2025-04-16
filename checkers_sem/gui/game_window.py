import pygame

from checkers_sem.game.game import Game
from checkers_sem.genetic.player import Player
from checkers_sem.constants import *
from checkers_sem.gui.utils.chessboard import ChessBoard


class GameWindow:
    def __init__(self, screen, players : tuple[Player, Player]):
        self.screen = screen
        self.white = players[0]
        self.black = players[1]
        self.game = Game()
        self.screen.fill((255, 255, 153))
        self.chessboard = ChessBoard(self.screen)

        self.turn = Turn.WHITE
        self.res = None


    def make_move(self):
        if self.res is not None: return

        if self.game.board.turn == Turn.WHITE:
            res = self.white.move(self.game, MAX_TRAIN_DEPTH)
            if res:
                self.res = (0, 1)
                return
        else:
            res = self.black.move(self.game, MAX_TRAIN_DEPTH)
            if res:
                self.res = (1, 0)
                return

        self.res = self.game.get_result()

    def play(self):

        run = True
        option = 0

        self.chessboard.draw(self.game)

        while run and option == 0:
            pygame.time.delay(100)

            self.make_move()

            self.chessboard.draw(self.game)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    print(self.chessboard.get_clicked_mask(mouse_pos))

            pygame.display.update()

