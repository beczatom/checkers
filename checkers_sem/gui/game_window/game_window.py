import pygame

from checkers_sem.game.game import Game
from checkers_sem.player.player import Player, AIPlayer
from checkers_sem.gui.utils.chessboard import ChessBoard
from checkers_sem.gui.utils.timer import Timer
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.window import Window
from checkers_sem.gui.utils.move_table import MoveTable
from checkers_sem.gui.utils.button import ImageButton
from checkers_sem.gui.utils.result import Result
from checkers_sem.gui.utils.checkbox import CheckBox
from checkers_sem.state import state
import copy

from checkers_sem.gui.utils.pos import Pos

from checkers_sem.gui.constants import SHOW_BEST_MOVES_TEXT, LEFT_ARROW_IMAGE, RIGHT_ARROW_IMAGE, BACKGROUND_COLOR, RESTART_ARROW_IMAGE
from checkers_sem.game.constants import Color, GameEnd

from threading import Thread


class GameWindow(Window):
    def __init__(self, surface : pygame.surface, players : tuple[Player, Player]):
        super().__init__(surface)

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

        self.turn = Color.WHITE

        self.res_window = None
        self.res_window_showed = False

        self.eval_values = {Color.BLACK: None, Color.WHITE: None}
        self.eval_texts = self.init_eval_texts()
        self.evaluation_start_hash = hash(None)
        self.evaluating = False
        self.best_move = None

    def checkbox_on_uncheck(self):
        self.chessboard.reset_best_move()
        self.chessboard.draw()

    def checkbox_on_check(self):
        self.evaluation_start_hash = hash(None)

    def init_best_move_checkbox(self) -> tuple[Text, CheckBox]:
        text = Text(self.surface,
                    Pos((0.21, 0.057), (0.778, 0, 0, 0.74)),
                    text=SHOW_BEST_MOVES_TEXT)

        checkbox = CheckBox(self.surface,
                            Pos((0.04, 0.057), (0.778, 0, 0, 0.7)),
                            on_check=self.checkbox_on_check,
                            on_uncheck=self.checkbox_on_uncheck)
        return text, checkbox

    def init_eval_texts(self) -> dict[bool, Text]:
        eval_texts = {}

        eval_texts[Color.BLACK] = Text(self.surface,
                                       Pos((0.1, 0.075), (0.067, 0.65, 0.858, 0.25), center=True),
                                       text='')

        eval_texts[Color.WHITE] = Text(self.surface,
                                       Pos((0.1, 0.075), (0.858, 0.65, 0.067, 0.25), center=True),
                                       text='')

        return eval_texts

    def update_eval_texts(self):
        for color in [Color.BLACK, Color.WHITE]:
            if self.eval_values[color] is not None:
                self.eval_texts[color].set_string(f'{self.eval_values[color]:.3f}')
            self.eval_texts[color].draw()

    def get_button_control_function(self, i : int):
        match i:
            case 0:
                def undo_move_button_onclick():
                    if self.active_thread is not None:
                        return
                    self.game.pop()
                    self.turn = self.game.board.turn
                    self.chessboard.draw()
                    self.move_table.set_move_texts(self.game.get_move_history())
                return undo_move_button_onclick
            case 1:
                def do_move_button_onclick():
                    if self.active_thread is not None:
                        return
                    self.game.push_from_popped()
                    self.turn = self.game.board.turn
                    self.chessboard.draw()
                    self.move_table.set_move_texts(self.game.get_move_history())
                return do_move_button_onclick
            case 2:
                def reset_game_button_onclick():
                    if self.active_thread is not None:
                        self.active_thread.join()
                    self.__init__(self.surface, (self.white, self.black))
                return reset_game_button_onclick
            case _:
                raise NotImplementedError()

    def init_game_control_buttons(self) -> list[ImageButton]:
        game_control_buttons = []
        for i, button_img in enumerate([LEFT_ARROW_IMAGE, RIGHT_ARROW_IMAGE, RESTART_ARROW_IMAGE]):

            game_control_button = ImageButton(self.surface,
                                              Pos((0.05, 0.07), (0.675, 0, 0, 0.7 + i * 0.1)),
                                              background_image=button_img, onclick=self.get_button_control_function(i))
            game_control_buttons.append(game_control_button)
            game_control_buttons[-1].draw()

        return game_control_buttons

    def init_move_table(self) -> MoveTable:
        move_table = MoveTable(self.surface,
                               Pos((0.25, 0.5), (0.142, 0.05, 0.358, 0.7), center = True))
        move_table.draw()
        return move_table

    def init_timers(self) -> tuple[Timer, Timer]:
        black_timer = Timer(self.surface,
                            Pos((0.125, 0.075), (0.067, 0.45, 0.858, 0.425)))

        white_timer = Timer(self.surface,
                            Pos((0.125, 0.075), (0.858, 0.45, 0.067, 0.425)))
        return white_timer, black_timer

    def init_chessboard(self) -> ChessBoard:

        return ChessBoard(self.surface,
                          Pos((0.5, 0.715), (0.142, 0.45, 0.142, 0.05), center=True),
                          game = self.game)

    def start_times(self):
        if self.res is not None: return
        if self.turn == Color.WHITE:
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
        return Result(self.surface,
                      Pos((0.5, 0.5), (0, 0, 0, 0), center=True),
                      res = self.res, game_end_type = self.game_end_type, onclick = self.result_onclick)

    def make_move(self) -> None:
        if self.res is not None: return

        if not self.black_timer.time_going and not self.white_timer.time_going:
            self.start_times()

        was_performed = False
        if self.turn == Color.WHITE:
            no_moves, was_performed, best = self.white.move(state.DEPTH_WHITE)
        else:
            no_moves, was_performed, best = self.black.move(state.DEPTH_BLACK)

        if no_moves:
            self.res = -1 if self.turn == Color.WHITE else 1
            self.game_end_type = GameEnd.NO_MOVES
            self.res_window = self.__init_result_window()
            return

        if was_performed:
            if best is not None:
                self.eval_values[self.turn] = best[1]
            self.turn = self.game.board.turn
            self.move_table.set_move_texts(self.game.get_move_history())
            self.start_times()

        self.res = self.game.get_result()
        if self.res is not None:
            self.game_end_type = self.game.get_end_type()

    def check_game_end(self):
        if self.res_window_showed or self.active_thread is not None: return
        if self.res is None:
            self.res = self.game.get_result()
        if self.res is not None:
            self.chessboard.reset_best_move()
            self.white_timer.time_stop()
            self.black_timer.time_stop()
            if self.game_end_type is None:
                self.game_end_type = self.game.get_end_type()
            self.res_window = self.__init_result_window()


    def move_ai(self):
        if self.active_thread is None and self.res is None:
            self.active_thread = Thread(target=self.make_move)
            self.active_thread.start()

        if self.active_thread is not None and not self.active_thread.is_alive():
            self.active_thread.join()
            self.turn = self.game.board.turn
            if self.game_end_type == GameEnd.NO_TIME:
                self.game.pop()
            self.active_thread = None

            if self.res is None:
                self.chessboard.draw()

    def handle_event(self, event : pygame.event.Event):
        super().handle_event(event)
        if self.res_window is not None:
            self.res_window.handle_event(event)

    def time_over_check(self):
        if self.white_timer.time_is_over():
            self.res = -1
            self.game_end_type = GameEnd.NO_TIME
        elif self.black_timer.time_is_over():
            self.res = 1
            self.game_end_type = GameEnd.NO_TIME

    def update_timers(self):
        self.white_timer.draw()
        self.black_timer.draw()
        self.time_over_check()


    def evaluating_thread(self, game: Game):
        player = AIPlayer(state.COEFS_BLACK)
        player.set_game(game)
        _, _, best = player.move(state.DEPTH_BLACK)
        game.pop()
        self.eval_values[Color.BLACK] = best[1]
        if best[0] is not None:
            self.best_move = (best[0].from_mask, best[0].to_mask)


    def evaluating_thread_check(self):
        if self.res is not None: return
        if self.active_thread is None and self.evaluation_start_hash != hash(self.game.board) and not self.evaluating:
            self.evaluation_start_hash = hash(self.game.board)
            self.evaluating = True
            self.active_thread = Thread(target=self.evaluating_thread, args=(copy.deepcopy(self.game),))
            self.active_thread.start()

        if self.active_thread is not None and not self.active_thread.is_alive() and self.evaluating:
            self.active_thread.join()
            self.evaluating = False
            if self.evaluation_start_hash == hash(self.game.board):
                self.chessboard.set_best_move(self.best_move)
            if self.res is None:
                self.chessboard.draw()
            self.active_thread = None

