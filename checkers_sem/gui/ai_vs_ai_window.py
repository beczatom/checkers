import pygame

from checkers_sem.gui.game_window import GameWindow
from checkers_sem.constants import *
from checkers_sem.player.player import AIPlayer
from threading import Thread


class AIVSAIWindow(GameWindow):
    def __init__(self, surface : pygame.surface, players : tuple[AIPlayer, AIPlayer]):
        super().__init__(surface, players)
        self.move_thread = None

    def show(self):
        run = True

        self.chessboard.draw()
        pygame.display.update()

        while run:
            pygame.time.delay(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.move_table.handle_event(event)
                    for button in self.game_control_buttons:
                        button.handle_event(event)

            if self.move_thread is None and self.res is None:
                self.move_thread = Thread(target=self.make_move)
                self.move_thread.start()

            if self.move_thread is not None and not self.move_thread.is_alive():
                self.move_thread.join()
                self.move_thread = None
                self.move_table.set_move_texts(self.game.get_move_history())
                self.chessboard.draw()

            self.white_timer.draw(self.white.get_time_left())
            self.black_timer.draw(self.black.get_time_left())
            pygame.display.update()