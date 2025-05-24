from checkers_sem.gui.utils.window import Window

from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.progress_bar import ProgressBar
from checkers_sem.gui.utils.pos import Pos
from checkers_sem.state import state
from threading import Thread
from checkers_sem.helper import do_one_generation_thread, get_coefs_header_text, get_genetic_completion, choose_best_thread
from checkers_sem.genetic.genetic import Genetic
import queue
import pygame

from checkers_sem.gui.constants import BACKGROUND_COLOR, BEST_GENETIC_COEFICIENTS_TEXT, AVERAGE_GENETIC_COEFICIENTS_TEXT, DEFAULT_FONT_SIZE, STAT_TEXTS, GENETIC_SETTINGS_TEXT, SLIDER_PROPERTIES

class GeneticWindow(Window):
    def __init__(self, surface : pygame.surface):
        super().__init__(surface)
        self.surface.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        self.genetic = Genetic()
        self.average_coefs = self.genetic.get_average_coefs()
        self.current_generation = 0
        self.completed = False
        self.genetic_thread = Thread(target=do_one_generation_thread, args=(self.genetic,))
        self.genetic_thread.start()
        self.setting_header, self.setting_val_headers, self.setting_values = self.init_setting_options()
        self.coefs_header, self.average_coefs_headers, self.average_coefs_text  = self.init_average_texts()
        self.bar = self.init_bar()
        self.best_queue = queue.Queue()
        self.best_player = None

    def update_coefs(self):
        if self.best_player is None:
            self.coefs_header.set_string(get_coefs_header_text(self.current_generation + 1))
            self.coefs_header.draw()
            for i, text in enumerate(self.average_coefs_text):
                text.set_string(round(self.average_coefs[i], 3))
                text.draw()
            return

        self.coefs_header.set_string(BEST_GENETIC_COEFICIENTS_TEXT)
        self.coefs_header.draw()
        for i, text in enumerate(self.average_coefs_text):
            text.set_string(round(self.best_player.coefs[i], 3))
            text.draw()

    def update_bar(self):
        completed_pct = 1 if self.completed else get_genetic_completion(self.current_generation)
        self.bar.set_value(completed_pct)
        self.bar.draw()

    def check_thread(self):
        if self.completed: return
        if self.genetic_thread.is_alive(): return

        self.genetic_thread.join()

        # we were choosing best
        if self.current_generation == state.GENERATIONS:
            self.best_player = self.best_queue.get()
            self.completed = True

        self.average_coefs = self.genetic.get_average_coefs()
        self.update_coefs()

        if self.best_player is not None:
            self.update_bar()
            return

        self.current_generation += 1
        if self.current_generation < state.GENERATIONS:
            self.genetic_thread = Thread(target=do_one_generation_thread, args=(self.genetic,))
        else:
            self.genetic_thread = Thread(target=choose_best_thread, args=(self.genetic, self.best_queue))

        self.genetic_thread.start()
        self.update_bar()

    def init_bar(self) -> ProgressBar:
        bar = ProgressBar(self.surface,
                  Pos((0.7, 0.15), (0.15, 0.15, 0.7, 0.15)),
                  value = 0)
        return bar

    def init_average_texts(self) -> tuple[Text, list[Text], list[Text]]:
        header_text = AVERAGE_GENETIC_COEFICIENTS_TEXT + ' pri inicializácii'
        coefs_header = Text(self.surface,
                            Pos((0.45, 0.1), (0.35, 0.05, 0.55, 0.5)),
                            text = header_text)

        coefs_val_headers = []
        coefs_vals = []
        for i, stat_name in enumerate(STAT_TEXTS):
            font_size = 4 * DEFAULT_FONT_SIZE // 5

            coefs_val_headers.append(Text(self.surface,
                                          Pos((0.275, 0.075), (0.475 + i * 0.075, 0.05, 0.45 - i * 0.075, 0.55)),
                                          text = stat_name, font_size=font_size))

            coefs_vals.append(Text(self.surface,
                                   Pos((0.125, 0.075), (0.475 + i * 0.075, 0.05, 0.45 - i * 0.075, 0.8)),
                                   text = round(self.average_coefs[i], 3), font_size=font_size))

        return coefs_header, coefs_val_headers, coefs_vals

    def init_setting_options(self) -> tuple[Text, list[Text], list[Text]]:
        header = Text(self.surface,
                      Pos((0.45, 0.1), (0.35, 0.5, 0.55, 0.05)),
                      text = GENETIC_SETTINGS_TEXT)
        setting_val_headers = []
        setting_val_texts = []

        for i, setting_val in enumerate(state.get_genetic_settings()):
            if i > 3:
                setting_val *= 100
            text, _, _, _ = SLIDER_PROPERTIES[i]
            font_size = 4 * DEFAULT_FONT_SIZE // 5

            setting_val_headers.append(Text(self.surface,
                                            Pos((0.275, 0.075), (0.475 + i * 0.075, 0.675, 0.45 - i * 0.075, 0.05)),
                                            text = text, font_size = font_size))

            setting_val_texts.append(Text(self.surface,
                                          Pos((0.125, 0.075), (0.475 + i * 0.075, 0.55, 0.45 - i * 0.075, 0.325)),
                                          text = setting_val, font_size = font_size))

        return header, setting_val_headers, setting_val_texts

    def handle_event(self, event : pygame.event.Event):
        super().handle_event(event)

    def refresh(self):
        self.check_thread()
        self.setting_header.draw()
        for i in range(len(self.setting_val_headers)):
            self.setting_val_headers[i].draw()
            self.setting_values[i].draw()

        self.coefs_header.draw()
        for i in range(len(self.average_coefs)):
            self.average_coefs_headers[i].draw()
            self.average_coefs_text[i].draw()
