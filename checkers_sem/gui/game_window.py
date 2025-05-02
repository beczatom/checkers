import pygame

from checkers_sem.game.game import Game
from checkers_sem.player.player import Player
from checkers_sem.constants import *
from checkers_sem.gui.utils.chessboard import ChessBoard
from checkers_sem.gui.utils.timer import Timer
from checkers_sem.gui.utils.window import Window
from checkers_sem.gui.utils.move_table import MoveTable
from checkers_sem.gui.utils.button import Button, ImageButton
from checkers_sem.gui.utils.result import Result
from checkers_sem.state import *

from threading import Thread


class GameWindow(Window):
    def __init__(self, surface : pygame.surface, players : tuple[Player, Player]):
        super().__init__(surface)
        self.surface.fill(BACKGROUND_COLOR, self.surface.get_rect())
        pygame.display.flip()

        self.game = Game()
        self.chessboard = self.init_chessboard()

        self.white = players[0]
        self.black = players[1]
        self.white.set_chessboard(self.chessboard)
        self.black.set_chessboard(self.chessboard)

        self.white_timer, self.black_timer = self.init_timers()

        self.res = None
        self.game_end_type = None

        self.move_table = self.init_move_table()

        self.game_control_buttons = self.init_game_control_buttons()

        self.turn = Turn.WHITE

        self.move_thread = None
        self.run = True
        self.menu_button = self.init_menu_button()


    def init_menu_button(self):
        size_x = self.surface.get_width() // 12
        size_y = self.surface.get_height() // 12

        top = self.surface.get_height() // 16
        left = self.surface.get_width() // 16

        def menu_button_onclick():
            print('menu button pressed')
            if self.move_thread is not None:
                self.move_thread.join()
            self.run = False

        menu_button_rect = pygame.Rect(left, top, size_x, size_y)
        menu_button = Button(self.surface.subsurface(menu_button_rect), (left, top),
                             MENU_BUTTON_TEXT, menu_button_onclick)
        menu_button.draw()
        return menu_button


    def get_button_control_function(self, i : int):
        match i:
            case 0:
                def undo_move_button_onclick():
                    self.game.pop()
                    self.chessboard.draw()
                    self.move_table.set_move_texts(self.game.get_move_history())
                return undo_move_button_onclick
            case 1:
                def do_move_button_onclick():
                    self.game.push_from_popped()
                    self.chessboard.draw()
                    self.move_table.set_move_texts(self.game.get_move_history())
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
        for i, button_img in enumerate([LEFT_ARROW_IMAGE, RIGHT_ARROW_IMAGE, RESTART_ARROW_IMAGE]):

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

        black_timer = Timer(self.surface.subsurface(timer_rect), (left, top))

        top = self.chessboard.get_screen_bottom() + self.chessboard.get_height() // 8 - height

        timer_rect = pygame.Rect(left, top, width, height)

        white_timer = Timer(self.surface.subsurface(timer_rect), (left, top))
        return white_timer, black_timer


    def init_chessboard(self) -> ChessBoard:
        size = self.surface.get_width() // 2 // 8 * 8
        top = (self.surface.get_height() - size) // 2
        left = self.surface.get_width() // 16

        chessboard_rect = pygame.Rect(left, top, size, size)

        return ChessBoard(self.surface.subsurface(chessboard_rect), (left, top), self.game)

    def start_times(self):
        if self.res is not None: return
        if self.turn == Turn.WHITE:
            self.black_timer.time_stop()
            self.white_timer.time_start()
        else:
            self.black_timer.time_start()
            self.white_timer.time_stop()

    def result_onclick(self):
        self.res_window = None
        self.surface.fill(BACKGROUND_COLOR)
        self.chessboard.draw()
        self.move_table.clear_indexes()
        self.move_table.draw()
        self.menu_button.draw()
        for button in self.game_control_buttons:
            button.draw()

    def __init_result_window(self) -> Result:
        self.res_window_showed = True
        top = self.surface.get_height() // 4
        left = self.surface.get_width() // 4
        result_rect = pygame.Rect(left, top, self.surface.get_width() // 2, self.surface.get_height() // 2)
        return Result(self.surface.subsurface(result_rect), (left, top), self.res, self.game_end_type, self.result_onclick)

    def make_move(self) -> None:
        if self.res is not None: return

        if not self.black_timer.time_going and not self.white_timer.time_going:
            self.start_times()

        was_performed = False
        if self.turn == Turn.WHITE:
            no_moves, was_performed = self.white.move(state.DEPTH_WHITE)
        else:
            no_moves, was_performed = self.black.move(state.DEPTH_BLACK)

        if no_moves:
            self.res = (0, 1) if self.turn == Turn.WHITE else (1, 0)
            self.game_end_type = GameEnd.NO_MOVES
            self.res_window = self.__init_result_window()
            return

        if was_performed:
            self.turn = self.game.board.turn
            self.move_table.set_move_texts(self.game.get_move_history())
            pygame.display.update(self.move_table.screen_rect)
            self.start_times()

        self.res = self.game.get_result()
        if self.res is not None:
            self.game_end_type = self.game.get_end_type()

    def check_game_end(self):
        if self.res_window_showed or self.active_thread is not None: return
        if self.res is None:
            self.res = self.game.get_result()
        if self.res is not None:
            self.white_timer.time_stop()
            self.black_timer.time_stop()
            if self.game_end_type is None:
                self.game_end_type = self.game.get_end_type()
            self.res_window = self.__init_result_window()


    def move_ai(self):
        if self.move_thread is None and self.res is None:
            self.move_thread = Thread(target=self.make_move)
            self.move_thread.start()

        if self.active_thread is not None and not self.active_thread.is_alive():
            self.active_thread.join()
            if self.game_end_type == GameEnd.NO_TIME:
                self.game.pop()
            self.active_thread = None
            self.chessboard.draw()

            self.check_game_end()
            # self.move_table.set_move_texts(self.game.get_move_history())

    def handle_event(self, event : pygame.event.Event):
        super().handle_event(event)
        if self.res_window is not None:
            self.res_window.handle_event(event)

    def time_over_check(self):
        if self.white_timer.time_is_over():
            self.res = (0, 1)
            self.game_end_type = GameEnd.NO_TIME
        elif self.black_timer.time_is_over():
            self.res = (1, 0)
            self.game_end_type = GameEnd.NO_TIME

    def update_timers(self):
        self.white_timer.draw()
        self.black_timer.draw()
        self.time_over_check()

