"""
This module helps GameWindow with taking care of chessboard, timers and evaluation.
"""

from threading import Thread

import pygame

from app.gui.utils.widget import Widget
from app.game.game import Game
from app.gui.utils.chessboard import ChessBoard
from app.gui.utils.timer import Timer
from app.gui.utils.text import Text
from app.state import state
from app.gui.utils.pos import Pos
from app.game.constants import Color, GameEnd
from app.gui.game_window.eval_helper import EvalHelper


class GameDisplay(Widget):
    """
    This class helps GameWindow with taking care of chessboard, timers and evaluation.
    """

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
        Returns
        -------
        move_made : bool
            true if move was made
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

        self.time_over_check()

        if self.res == (None, None):
            self.res = (self.chessboard.game.get_result(), self.chessboard.game.get_end_type())

        if self.res != (None, None):
            self.chessboard.reset_best_move()
            self.timers[Color.WHITE].time_stop()
            self.timers[Color.BLACK].time_stop()

    def move_ai(self) -> bool:
        """
        Defines move changes for AI player
        Returns
        -------
        move_made : bool
            true if move was made
        """
        if self.active_thread is None and self.res == (None, None):
            self.active_thread = Thread(target=self.make_move)
            self.active_thread.start()

        if self.active_thread is not None and not self.active_thread.is_alive():
            self.active_thread.join()
            self.turn = self.chessboard.game.board.turn
            if self.res[1] == GameEnd.NO_TIME:
                self.chessboard.game.pop()

            # if self.res == (None, None):
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
        timers = {}
        timers[Color.BLACK] = Timer(self.surface,
                                    Pos((0.25, 0.08), (0, 0, 0.92, 0.75)),
                                    self.left_top)

        timers[Color.WHITE] = Timer(self.surface,
                                    Pos((0.25, 0.08), (0.92, 0, 0, 0.75)),
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
                          Pos((1, 0.78), (0.11, 0, 0.11, 0), center=True),
                          self.screen_left_top,
                          game=Game())

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
                                       Pos((0.25, 0.08), (0, 0, 0.91, 0), center=True),
                                       self.left_top,
                                       text='')

        eval_texts[Color.WHITE] = Text(self.surface,
                                       Pos((0.25, 0.08), (0.91, 0, 0, 0), center=True),
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

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Does nothing.
        Parameters
        ----------
        event : pygame.event.Event
        """

    def draw(self) -> None:
        """
        Does nothing.
        """
