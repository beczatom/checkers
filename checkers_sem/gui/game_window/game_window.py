"""
This module defines main game window.
"""

import copy
from threading import Thread
from typing import Callable
from abc import abstractmethod

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
from checkers_sem.gui.utils.pos import Pos
from checkers_sem.gui.constants import SHOW_BEST_MOVES_TEXT, LEFT_ARROW_IMAGE, RIGHT_ARROW_IMAGE, BACKGROUND_COLOR, RESTART_ARROW_IMAGE
from checkers_sem.game.constants import Color, GameEnd
from checkers_sem.gui.game_window.game_display import GameDisplay

class GameWindow(Window):
    """
    This class implements the main game window.
    """
    def __init__(self, surface : pygame.surface, players : tuple[Player, Player]):
        super().__init__(surface)

        # self.chessboard = self.init_chessboard()
        # self.chessboard.draw()
        #
        self.players = players
        # self.players[0].set_chessboard(self.chessboard)
        # self.players[1].set_chessboard(self.chessboard)
        #
        # self.timers = self.init_timers()
        #
        # self.res = None
        # self.game_end_type = None

        self.game_display = self.init_game_display()

        self.move_table = self.init_move_table()

        self.game_control_buttons = self.init_game_control_buttons()

        self.turn = Color.WHITE

        self.res_window = None
        self.res_window_showed = False

        # self.eval_values = {Color.BLACK: None, Color.WHITE: None}
        # self.eval_texts = self.init_eval_texts()
        # self.evaluation_start_hash = hash(None)
        # self.evaluating = False
        # self.best_move = None

    def init_game_display(self) -> GameDisplay:
        game_display = GameDisplay(self.surface,
                    Pos((0.5, 0.916), (0.042, 0.45, 0.042, 0.05)),
                    players = self.players)
        return game_display

    def checkbox_on_uncheck(self) -> None:
        """
        Defines checkbox uncheck.
        """
        self.game_display.chessboard.reset_best_move()
        self.game_display.chessboard.draw()

    def checkbox_on_check(self):
        """
        Defines checkbox check.
        """
        self.game_display.eval_helper.evaluation_start_hash = hash(None)

    def init_best_move_checkbox(self) -> tuple[Text, CheckBox]:
        """
        Initializes title and checkbox for showing best moves.
        Returns
        -------
        title, checkbox : tuple[Text, CheckBox]
            Title and checkbox for showing best moves.
        """
        text = Text(self.surface,
                    Pos((0.21, 0.057), (0.778, 0, 0, 0.74)),
                    text=SHOW_BEST_MOVES_TEXT)

        checkbox = CheckBox(self.surface,
                            Pos((0.04, 0.057), (0.778, 0, 0, 0.7)),
                            on_check=self.checkbox_on_check,
                            on_uncheck=self.checkbox_on_uncheck)
        return text, checkbox

    # def init_eval_texts(self) -> dict[bool, Text]:
    #     """
    #     Initializes evaluation texts dictionary for both of players.
    #     Returns
    #     -------
    #     eval_dict : dict[bool, Text]
    #         white and black eval_text
    #     """
    #     eval_texts = {}
    #
    #     eval_texts[Color.BLACK] = Text(self.surface,
    #                                    Pos((0.1, 0.075), (0.067, 0.65, 0.858, 0.25), center=True),
    #                                    text='')
    #
    #     eval_texts[Color.WHITE] = Text(self.surface,
    #                                    Pos((0.1, 0.075), (0.858, 0.65, 0.067, 0.25), center=True),
    #                                    text='')
    #
    #     return eval_texts

    # def update_eval_texts(self) -> None:
    #     """
    #     Updates evaluation texts.
    #     """
    #     for color in [Color.BLACK, Color.WHITE]:
    #         if self.eval_values[color] is not None:
    #             self.eval_texts[color].set_text(f'{self.eval_values[color]:.3f}')
    #         self.eval_texts[color].draw()

    def get_button_control_function(self, i : int) -> Callable[[], None]:
        """
        Returns control button functions.
        Parameters
        ----------
        i : int
            which button

        Returns
        -------
        onclick : Callable[[], None]
            control button onclick
        """
        match i:
            case 0:
                def undo_move_button_onclick():
                    if self.game_display.active_thread is not None:
                        return
                    self.game_display.chessboard.game.pop()
                    self.turn = self.game_display.chessboard.game.board.turn
                    self.game_display.chessboard.draw()
                    self.move_table.set_move_texts(self.game_display.chessboard.game.get_move_history())
                return undo_move_button_onclick
            case 1:
                def do_move_button_onclick():
                    if self.game_display.active_thread is not None:
                        return
                    self.game_display.chessboard.game.push_from_popped()
                    self.turn = self.game_display.chessboard.game.board.turn
                    self.game_display.chessboard.draw()
                    self.move_table.set_move_texts(self.game_display.chessboard.game.get_move_history())
                return do_move_button_onclick
            case 2:
                def reset_game_button_onclick():
                    if self.active_thread is not None:
                        self.active_thread.join()
                    self.reset()
                return reset_game_button_onclick
            case _:
                raise NotImplementedError()

    def init_game_control_buttons(self) -> list[ImageButton]:
        """
        Initializes game control buttons.
        Returns
        -------
        control_buttons : list[ImageButton]
            game control buttons
        """
        game_control_buttons = []
        for i, button_img in enumerate([LEFT_ARROW_IMAGE, RIGHT_ARROW_IMAGE, RESTART_ARROW_IMAGE]):

            game_control_button = ImageButton(self.surface,
                                              Pos((0.05, 0.07), (0.675, 0, 0, 0.7 + i * 0.1)),
                                              background_image=button_img, onclick=self.get_button_control_function(i))
            game_control_buttons.append(game_control_button)
            game_control_buttons[-1].draw()

        return game_control_buttons

    def init_move_table(self) -> MoveTable:
        """
        Initializes move table.
        Returns
        -------
        move_table : MoveTable
            the move table
        """
        move_table = MoveTable(self.surface,
                               Pos((0.25, 0.5), (0.142, 0.05, 0.358, 0.7), center = True))
        move_table.draw()
        return move_table

    # def init_timers(self) -> tuple[Timer, Timer]:
    #     """
    #     Initializes timers.
    #     Returns
    #     -------
    #     white_timer, black_timer : tuple[Timer, Timer]
    #         timers
    #     """
    #     black_timer = Timer(self.surface,
    #                         Pos((0.125, 0.075), (0.067, 0.45, 0.858, 0.425)))
    #
    #     white_timer = Timer(self.surface,
    #                         Pos((0.125, 0.075), (0.858, 0.45, 0.067, 0.425)))
    #     return white_timer, black_timer
    #
    # def init_chessboard(self) -> ChessBoard:
    #     """
    #     Initializes chessboard.
    #     Returns
    #     -------
    #     chessboard : ChessBoard
    #         the chessboard
    #     """
    #     return ChessBoard(self.surface,
    #                       Pos((0.5, 0.715), (0.142, 0.45, 0.142, 0.05), center=True),
    #                       game = Game())
    #
    # def start_times(self) -> None:
    #     """
    #     Starts that timer, which player is on turn
    #     """
    #     if self.res is not None:
    #         return
    #     if self.turn == Color.WHITE:
    #         self.timers[0].time_start()
    #         self.timers[1].time_stop()
    #     else:
    #         self.timers[0].time_stop()
    #         self.timers[1].time_start()
    #
    def result_onclick(self) -> None:
        """
        Defines onclick for result widget
        """
        self.res_window = None
        self.surface.fill(BACKGROUND_COLOR)
        self.game_display.chessboard.draw()
        self.move_table.clear_indexes()
        self.game_display.chessboard.reset_best_move()
        self.move_table.draw()
        self.menu_button.draw()
        for button in self.game_control_buttons:
            button.draw()

    def init_result_window(self) -> Result:
        """
        Initializes result window.
        Returns
        -------
        result : Result
            result window
        """
        self.res_window_showed = True
        return Result(self.surface,
                      Pos((0.5, 0.5), (0, 0, 0, 0), center=True),
                      res = self.game_display.res, onclick = self.result_onclick)
    #
    # def make_move(self) -> None:
    #     """
    #     Takes care of move making on displayed chessboard.
    #     """
    #     if self.res is not None:
    #         return
    #
    #     if not self.timers[0].time_going and not self.timers[1].time_going:
    #         self.start_times()
    #
    #     was_performed = False
    #     if self.turn == Color.WHITE:
    #         no_moves, was_performed, best = self.players[0].move(state.DEPTH_WHITE)
    #     else:
    #         no_moves, was_performed, best = self.players[1].move(state.DEPTH_BLACK)
    #
    #     if no_moves:
    #         self.res = -1 if self.turn == Color.WHITE else 1
    #         self.game_end_type = GameEnd.NO_MOVES
    #         self.res_window = self.init_result_window()
    #         return
    #
    #     if was_performed:
    #         if best is not None:
    #             self.eval_values[self.turn] = best[1]
    #         self.turn = self.chessboard.game.board.turn
    #         self.move_table.set_move_texts(self.chessboard.game.get_move_history())
    #         self.start_times()
    #
    #     self.res = self.chessboard.game.get_result()
    #     if self.res is not None:
    #         self.game_end_type = self.chessboard.game.get_end_type()
    #
    def check_game_end(self) -> None:
        """
        Checks if game is over and does corresponding actions.
        """
        if self.res_window_showed or self.game_display.res == (None, None):
            return
        # if self.res is None:
        #     self.res = self.chessboard.game.get_result()
        # if self.res is not None:
        # self.chessboard.reset_best_move()
        # self.timers[0].time_stop()
        # self.timers[1].time_stop()
        # if self.game_end_type is None:
        #     self.game_end_type = self.chessboard.game.get_end_type()
        self.res_window = self.init_result_window()
    #
    #
    # def move_ai(self) -> None:
    #     """
    #     Defines move changes for AI player
    #     """
    #     if self.active_thread is None and self.res is None:
    #         self.active_thread = Thread(target=self.make_move)
    #         self.active_thread.start()
    #
    #     if self.active_thread is not None and not self.active_thread.is_alive():
    #         self.active_thread.join()
    #         self.turn = self.chessboard.game.board.turn
    #         if self.game_end_type == GameEnd.NO_TIME:
    #             self.chessboard.game.pop()
    #         self.active_thread = None
    #
    #         if self.res is None:
    #             self.chessboard.draw()

    def handle_event(self, event : pygame.event.Event) -> None:
        """
        Handles events.
        Parameters
        ----------
        event : pygame.event.Event
            event to handle
        """
        super().handle_event(event)
        if self.res_window is not None:
            self.res_window.handle_event(event)

    # def time_over_check(self) -> None:
    #     """
    #     Checks if time is over.
    #     """
    #     if self.timers[0].time_is_over():
    #         self.res = -1
    #         self.game_end_type = GameEnd.NO_TIME
    #     elif self.timers[1].time_is_over():
    #         self.res = 1
    #         self.game_end_type = GameEnd.NO_TIME
    #
    # def evaluating_thread(self, game: Game) -> None:
    #     """
    #     Function for thread to evaluate the game.
    #     Parameters
    #     ----------
    #     game : Game
    #         game to evaluate
    #     """
    #     player = AIPlayer(state.COEFS_BLACK)
    #     player.set_game(game)
    #     _, _, best = player.move(state.DEPTH_BLACK)
    #     game.pop()
    #     self.eval_values[Color.BLACK] = best[1]
    #     if best[0] is not None:
    #         self.best_move = (best[0].from_mask, best[0].to_mask)
    #
    # def evaluating_thread_check(self) -> None:
    #     """
    #     Checks if thread finished evaluating.
    #     Or if it is necessary to start it.
    #     """
    #     if self.res is not None:
    #         return
    #     if self.active_thread is None and self.evaluation_start_hash != hash(self.chessboard.game.board) and not self.evaluating:
    #         self.evaluation_start_hash = hash(self.chessboard.game.board)
    #         self.evaluating = True
    #         self.active_thread = Thread(target=self.evaluating_thread, args=(copy.deepcopy(self.chessboard.game),))
    #         self.active_thread.start()
    #
    #     if self.active_thread is not None and not self.active_thread.is_alive() and self.evaluating:
    #         self.active_thread.join()
    #         self.evaluating = False
    #         if self.evaluation_start_hash == hash(self.chessboard.game.board):
    #             self.chessboard.set_best_move(self.best_move)
    #         if self.res is None:
    #             self.chessboard.draw()
    #         self.active_thread = None

    @abstractmethod
    def refresh(self) -> None:
        """
        Abstract method to refresh the window.
        Raises
        ------
        error : NotImplementedError
            if the child class doesn't implement this method.
        """
        raise NotImplementedError()

    @abstractmethod
    def reset(self) -> None:
        """
        Abstract method to reset the window.
        Raises
        ------
        error : NotImplementedError
            if the child class doesn't implement this method.
        """
        raise NotImplementedError()
