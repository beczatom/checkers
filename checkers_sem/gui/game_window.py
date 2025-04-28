import pygame

from checkers_sem.game.game import Game
from checkers_sem.player.player import Player
from checkers_sem.constants import *
from checkers_sem.gui.utils.chessboard import ChessBoard
from checkers_sem.gui.utils.timer import Timer
from checkers_sem.gui.utils.window import Window


class GameWindow(Window):
    def __init__(self, surface : pygame.surface, players : tuple[Player, Player]):
        super().__init__(surface)
        self.surface.fill(BACKGROUND_COLOR)

        self.game = Game()
        self.chessboard = self.init_chessboard()

        self.white = players[0]
        self.black = players[1]
        self.white.set_chessboard(self.chessboard)
        self.black.set_chessboard(self.chessboard)

        self.white_timer, self.black_timer = self.init_timers()

        self.res = None

        self.turn_before = Turn.BLACK

    def init_timers(self):

        height = self.chessboard.get_height() // 10
        width = self.chessboard.get_width() // 4

        top = self.chessboard.get_screen_top() - self.chessboard.get_height() // 8
        left = self.chessboard.get_screen_left() + 3 * self.chessboard.get_width() // 4

        timer_rect = pygame.Rect(left, top, width, height)

        black_timer = Timer(self.surface.subsurface(timer_rect), (left, top),
                            first_border=True, second_border=True, font_size=24)

        top = self.chessboard.get_screen_bottom() + self.chessboard.get_height() // 8 - height

        timer_rect = pygame.Rect(left, top, width, height)

        white_timer = Timer(self.surface.subsurface(timer_rect), (left, top),
                            first_border=True, second_border=True, font_size=24)
        return white_timer, black_timer


    def init_chessboard(self) -> ChessBoard:
        size = self.surface.get_width() // 2 // 8 * 8
        top = (self.surface.get_height() - size) // 2
        left = (self.surface.get_width() - size) // 5

        chessboard_rect = pygame.Rect(left, top, size, size)

        return ChessBoard(self.surface.subsurface(chessboard_rect), (left, top), self.game)


    def make_move(self, clicked_mouse_pos : tuple[int, int] = None) -> None:
        if self.res is not None: return

        if self.game.board.turn == Turn.WHITE:
            if self.turn_before == Turn.BLACK:
                self.white.time_start()
                self.turn_before = Turn.WHITE
            no_moves = self.white.move(MAX_TRAIN_DEPTH, clicked_mouse_pos)
            if no_moves:
                self.res = (0, 1)
                return
        else:
            if self.turn_before == Turn.WHITE:
                self.black.time_start()
                self.turn_before = Turn.BLACK

            no_moves = self.black.move(MAX_TRAIN_DEPTH, clicked_mouse_pos)
            if no_moves:
                self.res = (1, 0)
                return

        self.res = self.game.get_result()

    def show(self):
        run = True

        self.chessboard.draw()
        pygame.display.update()

        while run:
            before_chessboard = hash(self.chessboard.game)
            pygame.time.delay(10)
            mouse_pos = pygame.mouse.get_pos()
            clicked = False
            i = 0
            for event in pygame.event.get():
                i += 1
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    clicked = True

            if clicked:
                self.make_move(mouse_pos)
            else:
                self.make_move()

            if before_chessboard != hash(self.chessboard.game) or clicked:
                self.chessboard.draw()

            self.white_timer.draw(self.white.get_time_left())
            self.black_timer.draw(self.black.get_time_left())
            pygame.display.update()
