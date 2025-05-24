import pygame

from checkers_sem.gui.constants import BACKGROUND_COLOR, LEFT_ARROW_IMAGE, REFRESH_RATE_MS
from checkers_sem.gui.utils.button import ImageButton
from checkers_sem.gui.utils.pos import Pos

from abc import abstractmethod

class Window:
    def __init__(self, surface : pygame.surface):
        self.surface = surface
        self.surface.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        self.run = True
        self.menu_button = self.init_menu_button()

        self.active_thread = None

    def init_menu_button(self):

        def menu_button_onclick():
            if self.active_thread is not None:
                self.active_thread.join()
            self.run = False

        menu_button = ImageButton(self.surface,
                                  Pos((0.05, 0.05), (0.025, 0, 0, 0.025)),
                                  background_image = LEFT_ARROW_IMAGE, onclick = menu_button_onclick)
        menu_button.draw()
        return menu_button

    def handle_event(self, event : pygame.event.Event):
        if event.type == pygame.QUIT:
            raise StopIteration()
        self.menu_button.handle_event(event)

    @abstractmethod
    def refresh(self):
        raise NotImplementedError()

    def show(self):
        while self.run:
            pygame.time.delay(REFRESH_RATE_MS)
            self.menu_button.draw()

            for event in pygame.event.get():
                self.handle_event(event)

            if self.run: self.refresh()

            pygame.display.update()

        self.surface.fill(BACKGROUND_COLOR)