import pygame

from checkers_sem.gui.game_window import GameWindow
from checkers_sem.player.player import AIPlayer


class AIVSAIWindow(GameWindow):
    def __init__(self, surface : pygame.surface, players : tuple[AIPlayer, AIPlayer]):
        super().__init__(surface, players)
        self.run = True
        self.chessboard.draw()

    def handle_event(self, event : pygame.event.Event):
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.move_table.handle_event(event)
            for button in self.game_control_buttons:
                button.handle_event(event)

    def refresh(self):
        self.move_ai()
        self.update_eval_texts()
        self.update_timers()
        self.check_game_end()
