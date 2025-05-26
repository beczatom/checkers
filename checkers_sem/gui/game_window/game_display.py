
import copy
from threading import Thread
from typing import Callable
from abc import abstractmethod

import pygame

from checkers_sem.gui.utils.widget import Widget
from checkers_sem.game.game import Game, BitBoard
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

class GameDisplay(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.chessboard = self.init_chessboard()
        self.chessboard.draw()

        self.players = kwargs.get('players')
        self.players[0].set_chessboard(self.chessboard)
        self.players[1].set_chessboard(self.chessboard)

        self.timers = self.init_timers()

        self.res = (None, None)

        self.turn = Color.WHITE

        self.eval_helper = EvalHelper(self.chessboard, self.init_eval_texts())

        self.active_thread = None


    def make_move(self) -> bool:
        """
        Takes care of move making on displayed chessboard.
        """
        if self.res != (None, None):
            return False

        if not self.timers[Color.WHITE].time_going and not self.timers[Color.BLACK].time_going:
            self.start_times()

        was_performed = False
        if self.turn == Color.WHITE:
            no_moves, was_performed, best = self.players[0].move(state.DEPTH_WHITE)
        else:
            no_moves, was_performed, best = self.players[1].move(state.DEPTH_BLACK)

        if no_moves:
            self.res = (-1 if self.turn == Color.WHITE else 1, GameEnd.NO_MOVES)
            return False

        if was_performed:
            if best is not None:
                self.eval_helper.set_eval(best[1], self.turn)
            self.turn = self.chessboard.game.board.turn
            self.start_times()

        self.res = (self.chessboard.game.get_result(), self.chessboard.game.get_end_type())
        return was_performed

    def check_game_end(self) -> None:
        """
        Checks if game is over and does corresponding actions.
        """
        if self.active_thread is not None:
            return
        if self.res == (None, None):
            self.res = (self.chessboard.game.get_result(), self.chessboard.game.get_end_type())
        if self.res != (None, None):
            self.chessboard.reset_best_move()
            self.timers[Color.WHITE].time_stop()
            self.timers[Color.BLACK].time_stop()


    def move_ai(self) -> bool:
        """
        Defines move changes for AI player
        """
        if self.active_thread is None and self.res == (None, None):
            self.active_thread = Thread(target=self.make_move)
            self.active_thread.start()

        if self.active_thread is not None and not self.active_thread.is_alive():
            self.active_thread.join()
            self.turn = self.chessboard.game.board.turn
            if self.res != (None, None):
                self.chessboard.game.pop()

            if self.res == (None, None):
                self.chessboard.draw()
            self.active_thread = None
            return True
        return False


    def start_times(self) -> None:
        """
        Starts that timer, which player is on turn
        """
        if self.res != (None, None):
            return
        if self.turn == Color.WHITE:
            self.timers[Color.WHITE].time_start()
            self.timers[Color.BLACK].time_stop()
        else:
            self.timers[Color.WHITE].time_stop()
            self.timers[Color.BLACK].time_start()

    def init_timers(self) -> dict[bool, Timer]:
        """
        Initializes timers.
        Returns
        -------
        timers : dict[bool, Timer]
            timers
        """
        timers = dict()
        timers[Color.BLACK] = Timer(self.surface,
                            Pos((0.2, 0.075), (0, 0, 0.858, 0.8)),
                                    self.left_top)

        timers[Color.WHITE] = Timer(self.surface,
                            Pos((0.2, 0.075), (0.858, 0, 0, 0.8)),
                                    self.left_top)
        return timers

    def init_chessboard(self) -> ChessBoard:
        """
        Initializes chessboard.
        Returns
        -------
        chessboard : ChessBoard
            the chessboard
        """
        return ChessBoard(self.surface,
                          Pos((1, 0.8), (0.1, 0, 0.1, 0), center=True),
                          self.screen_left_top,
                          game = Game())

    def init_eval_texts(self) -> dict[bool, Text]:
        """
        Initializes evaluation texts dictionary for both of players.
        Returns
        -------
        eval_dict : dict[bool, Text]
            white and black eval_text
        """
        eval_texts = {}

        eval_texts[Color.BLACK] = Text(self.surface,
                                       Pos((0.2, 0.075), (0, 0, 0.858, 0), center=True),
                                       self.left_top,
                                       text='')

        eval_texts[Color.WHITE] = Text(self.surface,
                                       Pos((0.2, 0.075), (0.8, 0, 0, 0), center=True),
                                       self.left_top,
                                       text='')

        return eval_texts

    def time_over_check(self) -> None:
        """
        Checks if time is over.
        """
        if self.timers[Color.WHITE].time_is_over():
            self.res = (-1, GameEnd.NO_TIME)
        elif self.timers[Color.BLACK].time_is_over():
            self.res = (1, GameEnd.NO_TIME)

    def handle_event(self, event: pygame.event.Event):
        pass

    def draw(self) -> None:
        pass

class EvalHelper:
    def __init__(self, chessboard : ChessBoard, texts : dict[bool, Text]):
        self.chessboard = chessboard
        self.texts = texts
        self.eval_values = {Color.BLACK: 0.0, Color.WHITE: 0.0}
        self.evaluation_start_hash = hash(None)
        self.best_move = None
        self.active_thread = None

    def get_eval(self) -> tuple[dict[bool, float], tuple[BitBoard, BitBoard]]:
        # if we are working and have result
        if self.active_thread is not None and not self.active_thread.is_alive():
            self.active_thread.join()
            if self.evaluation_start_hash != hash(self.chessboard.game):
                self.chessboard.reset_best_move()
                self.best_move = None
            self.active_thread = None

        # if something changed and we are not working on it
        if self.active_thread is None and self.evaluation_start_hash != hash(self.chessboard.game):
            self.evaluation_start_hash = hash(self.chessboard.game)
            self.active_thread = Thread(target=self.evaluating_thread, args=(copy.deepcopy(self.chessboard.game),))
            self.active_thread.start()

        return self.eval_values, self.best_move

    def set_eval(self, evaluation : float, color : bool):
        self.eval_values[color] = evaluation
        self.evaluation_start_hash = hash(self.chessboard.game)
        # self.best_move = None

    def update_eval(self):
        self.get_eval()
        for color in [Color.WHITE, Color.BLACK]:
            if self.eval_values[color] is not None:
                self.texts[color].set_text(f'{self.eval_values[color]:.3f}')
                self.texts[color].draw()

    def update_best_move(self):
        if self.chessboard.best_move is None and self.evaluation_start_hash == hash(self.chessboard.game) and \
                self.active_thread is None:
            self.get_eval()
            self.chessboard.set_best_move(self.best_move)
            self.chessboard.draw()

    def evaluating_thread(self, game: Game) -> None:
        """
        Function for thread to evaluate the game.
        Parameters
        ----------
        game : Game
            game to evaluate
        """
        player = AIPlayer(state.COEFS_BLACK)
        player.set_game(game)
        _, _, best = player.move(state.DEPTH_BLACK)
        game.pop()
        self.eval_values[Color.BLACK] = best[1]
        self.best_move = (best[0].from_mask, best[0].to_mask)

