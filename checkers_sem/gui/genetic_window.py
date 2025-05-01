import queue

import pygame

from checkers_sem.gui.utils.window import *

from checkers_sem.genetic.genetic import Genetic
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.bar import Bar
from checkers_sem.state import *
from threading import Thread
from checkers_sem.helper import *
from checkers_sem.genetic.genetic_player import GeneticPlayer

class GeneticWindow(Window):
    def __init__(self, surface : pygame.surface):
        super().__init__(surface)
        self.surface.fill(BACKGROUND_COLOR)
        self.genetic = Genetic()
        self.average_coefs = self.genetic.get_average_coefs()
        self.current_generation = 0
        self.completed = False
        self.genetic_thread = Thread(target=do_one_generation_thread, args=(self.genetic,))
        self.genetic_thread.start()
        self.init_setting_options()
        self.average_coefs_text, self.coefs_header = self.init_average_texts()
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

    def init_bar(self) -> Bar:
        margin_x = self.surface.get_rect().width // 8

        margin_y_top = 3 * self.surface.get_rect().height // 8
        margin_y_bottom = 4 * self.surface.get_rect().height // 8

        size_x = self.surface.get_rect().width - 2 * margin_x
        size_y = self.surface.get_rect().height - margin_y_bottom - margin_y_top

        bar_rect = pygame.Rect(margin_x, margin_y_top, size_x, size_y)
        bar = Bar(self.surface.subsurface(bar_rect), (margin_x, margin_y_top), 0)
        bar.draw()
        return bar

    def init_average_texts(self) -> tuple[list[Text], Text]:
        texts = []

        margin_x_right = self.surface.get_rect().width // 16
        margin_x_left = 7 * self.surface.get_rect().width // 16

        margin_y_top = 3 * self.surface.get_rect().height // 5
        margin_y_bottom = self.surface.get_rect().height // 5

        padding_between = (self.surface.get_rect().height - margin_y_top - margin_y_bottom) // 10

        size_x = self.surface.get_rect().width - margin_x_right - margin_x_left
        size_y = (self.surface.get_rect().height - margin_y_top - margin_y_bottom - 4 * padding_between) // 6

        text_rect = pygame.Rect(margin_x_left, margin_y_top, size_x, DEFAULT_FONT_SIZE)
        header_text = AVERAGE_GENETIC_COEFICIENTS_TEXT + ' pri inicializácii'
        coefs_header = Text(self.surface.subsurface(text_rect), (margin_x_left, margin_y_top), header_text)
        coefs_header.draw()

        margin_y_top += 2 * DEFAULT_FONT_SIZE

        for i, stat_name in enumerate(STAT_TEXTS):
            top = margin_y_top + i * padding_between + i * size_y
            padding_x = size_x // 10

            left = margin_x_left

            font_size = 4 * DEFAULT_FONT_SIZE // 5

            text_rect = pygame.Rect(margin_x_left, top, 5 * (size_x - padding_x) // 8, size_y)
            Text(self.surface.subsurface(text_rect), (margin_x_left, top), stat_name, font_size=font_size).draw()

            left += text_rect.width + padding_x

            option_value_text_rect = pygame.Rect(left, top, 3 * (size_x - padding_x) // 8, size_y)
            texts.append(Text(self.surface.subsurface(option_value_text_rect), (left, top),
                         round(self.average_coefs[i], 3), font_size=font_size))
            texts[-1].draw()

        return texts, coefs_header

    def init_setting_options(self) -> None:

        margin_x_left = self.surface.get_rect().width // 16
        margin_x_right = 9 * self.surface.get_rect().width // 16
        margin_y_top = 3 * self.surface.get_rect().height // 5
        margin_y_bottom = self.surface.get_rect().height // 5

        padding_between = (self.surface.get_rect().height - margin_y_top - margin_y_bottom) // 10

        size_x = self.surface.get_rect().width - margin_x_right - margin_x_left
        size_y = (self.surface.get_rect().height - margin_y_top - margin_y_bottom - 4 * padding_between) // 5

        text_rect = pygame.Rect(margin_x_left, margin_y_top, size_x, DEFAULT_FONT_SIZE)
        Text(self.surface.subsurface(text_rect), (margin_x_left, margin_y_top), GENETIC_SETTINGS_TEXT).draw()

        margin_y_top += 2 * DEFAULT_FONT_SIZE

        for i, setting_val in enumerate(state.get_genetic_settings()):
            if i > 3:
                setting_val *= 100
            text, _, _, _ = SLIDER_PROPERTIES[i]
            top = margin_y_top + i * padding_between + i * size_y
            padding_x = size_x // 10

            left = margin_x_left

            font_size = 4 * DEFAULT_FONT_SIZE // 5

            text_rect = pygame.Rect(margin_x_left, top, 5 * (size_x - padding_x) // 8, size_y)
            Text(self.surface.subsurface(text_rect), (margin_x_left, top), text, font_size = font_size).draw()

            left += text_rect.width + padding_x

            option_value_text_rect = pygame.Rect(left, top, 3 * (size_x - padding_x) // 8, size_y)
            Text(self.surface.subsurface(option_value_text_rect), (left, top), setting_val, font_size = font_size).draw()


    def show(self):
        run = True
        print(state.POPULATION_SIZE, state.GENERATIONS, state.MAX_TRAIN_DEPTH, state.CROSSOVER_PCT, state.MUTATION_PCT)

        while run:
            pygame.time.delay(10)
            self.check_thread()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
