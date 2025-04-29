import pygame

from checkers_sem.game.game import Game
from checkers_sem.player.player import Player
from checkers_sem.constants import *
from checkers_sem.gui.utils.chessboard import ChessBoard
from checkers_sem.gui.utils.timer import Timer
from checkers_sem.gui.utils.window import Window
from checkers_sem.gui.utils.move_table import MoveTable
from checkers_sem.gui.utils.button import ImageButton


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

        self.move_table = self.init_move_table()

        self.game_control_buttons = self.init_game_control_buttons()

    def get_button_control_function(self, i : int):
        match i:
            case 0:
                def undo_move_button_onclick():
                    self.game.pop()
                return undo_move_button_onclick
            case 1:
                def do_move_button_onclick():
                    self.game.push_from_popped()
                return do_move_button_onclick
            case 2:
                def reset_game_button_onclick():
                    # TODO expand class to three
                    self.__init__(self.surface, (self.white, self.black))
                return reset_game_button_onclick
            case _:
                raise NotImplementedError()

    def init_game_control_buttons(self) -> list[ImageButton]:
        top = self.move_table.get_screen_bottom()
        top += self.move_table.get_height() // 16

        padding_x = self.move_table.get_width() // 5
        button_size = (self.move_table.get_width() - 2 * padding_x) // 3

        left = self.move_table.get_screen_left()

        game_control_buttons = []
        for i, button_img in enumerate(GAME_CONTROL_BUTTON_IMAGES):

            game_control_button_rect = pygame.Rect(left, top, button_size, button_size)
            game_control_button = ImageButton(self.surface.subsurface(game_control_button_rect), (left, top),
                                              button_img, self.get_button_control_function(i))
            game_control_buttons.append(game_control_button)
            game_control_buttons[-1].draw()
            left += padding_x + button_size

        return game_control_buttons

    def init_move_table(self) -> MoveTable:
        top = self.chessboard.get_screen_top()
        bottom = 3 * self.surface.get_height() // 8
        size_y = self.surface.get_height() - top - bottom

        left = 11 * self.surface.get_width() // 16
        right = 2 * self.surface.get_width() // 16
        size_x = self.surface.get_width() - left - right

        move_table_rect = pygame.Rect(left, top, size_x, size_y)

        move_table = MoveTable(self.surface.subsurface(move_table_rect), (left, top))
        move_table.draw()
        return move_table

    def init_timers(self) -> tuple[Timer, Timer]:

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
        left = self.surface.get_width() // 16

        chessboard_rect = pygame.Rect(left, top, size, size)

        return ChessBoard(self.surface.subsurface(chessboard_rect), (left, top), self.game)

    def __start_times(self):
        if self.res is not None: return
        if self.game.board.turn == Turn.WHITE and not self.white.time_going:
            self.white.time_start()
        elif self.game.board.turn == Turn.WHITE and not self.white.time_going:
            self.white.time_start()

    def make_move(self) -> None:
        if self.res is not None: return

        self.__start_times()
        if self.game.board.turn == Turn.WHITE:
            if self.white.move(MAX_TRAIN_DEPTH):
                self.res = (0, 1)
                return
        else:
            if self.black.move(MAX_TRAIN_DEPTH):
                self.res = (1, 0)
                return
        self.res = self.game.get_result()

        self.__start_times()
        # if self.res is not None:
        #     if self.game.board.turn == Turn.WHITE and not self.white.time_going:
        #         self.white.time_start()
        #     elif self.game.board.turn == Turn.BLACK and not self.black.time_going:
        #         self.black.time_start()


    def show(self):
        run = True

        self.chessboard.draw()
        pygame.display.update()

        while run:
            clicked = False
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    self.move_table.handle_event(event)
                    self.chessboard.handle_event(event)
                    for button in self.game_control_buttons:
                        button.handle_event(event)

            if clicked:
                self.make_move()
                self.move_table.set_move_texts(self.game.get_move_history())
                self.chessboard.draw()
            self.white_timer.draw(self.white.get_time_left())
            self.black_timer.draw(self.black.get_time_left())
            pygame.display.update()
