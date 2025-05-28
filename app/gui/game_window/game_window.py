"""
This module defines main game window.
"""

from typing import Callable
from abc import abstractmethod

import pygame

from app.player.player import Player
from app.gui.utils.text import Text
from app.gui.utils.window import Window
from app.gui.utils.move_table import MoveTable
from app.gui.utils.button import ImageButton
from app.gui.utils.result import Result
from app.gui.utils.checkbox import CheckBox
from app.gui.utils.pos import Pos
from app.gui.constants import SHOW_BEST_MOVES_TEXT, LEFT_ARROW_IMAGE, RIGHT_ARROW_IMAGE, BACKGROUND_COLOR, RESTART_ARROW_IMAGE
from app.game.constants import Color
from app.gui.game_window.game_display import GameDisplay

class GameWindow(Window):
    """
    This class implements the main game window.
    """
    def __init__(self, surface : pygame.surface, players : tuple[Player, Player]):
        super().__init__(surface)

        self.players = players
        self.game_display = self.init_game_display()

        self.move_table = self.init_move_table()

        self.game_control_buttons = self.init_game_control_buttons()

        self.turn = Color.WHITE

        self.res_window = None
        self.res_window_showed = False

    def init_game_display(self) -> GameDisplay:
        """
        Initializes game display.
        """
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

    def check_game_end(self) -> None:
        """
        Checks if game is over and does corresponding actions.
        """
        self.game_display.check_game_end()
        if self.res_window_showed or self.game_display.res == (None, None) or self.game_display.active_thread:
            return
        self.res_window = self.init_result_window()

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
