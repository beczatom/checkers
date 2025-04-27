import pygame

from checkers_sem.gui.utils.window import Window
from checkers_sem.gui.utils.slider import Slider
from checkers_sem.gui.utils.text import Text
from checkers_sem.gui.utils.button import Button
from checkers_sem.constants import *

# TODO make more real
def get_awaited_train_time(population : int, generations : int, depth : int) -> int:
    evolving_time = population * generations * depth
    choosing_best = int((population - 1) * (population - 2) / 2 * depth)
    return evolving_time + choosing_best

def time_to_text(seconds : int) -> str:
    string = str()
    hours = seconds // 3600

    if hours == 1:
        string += '1 hodina '
    elif 1 < hours < 5:
        string += f'{hours} hodiny '
    elif 5 < hours:
        string += f'{hours} hodín '

    minutes = (seconds % 3600) // 60

    if minutes == 1:
        string += '1 minúta '
    elif 1 < minutes < 5:
        string += f'{minutes} minúty '
    elif 5 <= minutes:
        string += f'{minutes} minút '

    seconds = seconds % 60

    if seconds == 1:
        string += '1 sekunda'
    elif 1 < seconds < 5:
        string += f'{seconds} sekundy'
    elif 5 <= seconds:
        string += f'{seconds} sekúnd'

    return string

class GeneticSettingWindow(Window):
    def __init__(self, surface):
        super().__init__(surface)
        self.slider_text_vals, self.sliders = self.init_sliders()
        self.awaited_time = self.init_awaited_time()
        self.start_button = self.init_start_button()
        self.start = False


    def init_start_button(self):
        margin_x = 6 * self.surface.get_rect().width // 8

        space_y = self.surface.get_rect().height - self.awaited_time.get_screen_bottom()
        margin_y = self.awaited_time.get_screen_bottom() + space_y // 4
        size_y = space_y // 3
        size_x = margin_x // 6

        button_rect = pygame.Rect(margin_x, margin_y, size_x, size_y)

        def on_start_click():
            self.start = True

        button = Button(self.surface.subsurface(button_rect), (margin_x, margin_y),
                        START_TRAIN_BUTTON_TEXT, on_start_click)
        return button

    def get_time_text_from_sliders(self):
        values = [self.sliders[i].get_value() for i in range(3)]
        seconds = get_awaited_train_time(*values)
        return time_to_text(seconds)

    def init_awaited_time(self):
        margin_x = self.surface.get_rect().width // 8
        padding_x = self.surface.get_rect().width // 14

        space_y = self.surface.get_rect().height - self.sliders[-1].get_screen_bottom()
        margin_y = self.sliders[-1].get_screen_bottom() + space_y // 4
        size_y = space_y // 6
        size_x = (self.surface.get_rect().width - 2 * margin_x - padding_x) // 2

        text_rect = pygame.Rect(margin_x, margin_y, size_x, size_y)
        text = Text(self.surface.subsurface(text_rect), (margin_x, margin_y), AWAITED_TIME_TRAIN_TEXT)
        text.draw()

        margin_x += size_x + padding_x

        text_rect = pygame.Rect(margin_x, margin_y, size_x, size_y)

        text = Text(self.surface.subsurface(text_rect), (margin_x, margin_y), self.get_time_text_from_sliders())
        text.draw()
        return text

    def init_sliders(self) -> tuple[list[Text], list[Slider]]:
        sliders = []
        slider_text_vals = []

        margin_x = self.surface.get_rect().width // 8
        margin_y_top = self.surface.get_rect().height // 5
        margin_y_bottom = self.surface.get_rect().height // 3

        padding_between = (self.surface.get_rect().height - margin_y_top - margin_y_bottom) // 10

        size_x = self.surface.get_rect().width - 2 * margin_x
        size_y = (self.surface.get_rect().height -  margin_y_top - margin_y_bottom - 4 * padding_between) // 5

        for i in range(5):
            text, min_val, max_val, initial_val = SLIDER_PROPERTIES[i]
            top = margin_y_top + i * padding_between + i * size_y
            padding_x = size_x // 10

            left = margin_x

            text_rect = pygame.Rect(margin_x, top, 6 * (size_x - 2 * padding_x) // 16, size_y)
            Text(self.surface.subsurface(text_rect), (margin_x, top), text).draw()

            left += text_rect.width + padding_x

            slider_text_rect = pygame.Rect(left, top, (size_x - 2 * padding_x) // 16, size_y)
            slider_text_vals.append(Text(self.surface.subsurface(slider_text_rect), (left, top), initial_val))
            slider_text_vals[-1].draw()

            left += slider_text_rect.width + padding_x

            slider_rect = pygame.Rect(left, top, 9 * (size_x - 2 * padding_x) // 16, size_y)
            sliders.append(Slider(self.surface.subsurface(slider_rect), (left, top), min_val, max_val, initial_val))

            sliders[-1].draw()
        return slider_text_vals, sliders

    def show(self):
        run = True

        while run and not self.start:
            pygame.time.delay(10)
            for event in pygame.event.get():
                self.start_button.handle_event(event)
                if event.type == pygame.QUIT:
                    run = False

                for i, slider in enumerate(self.sliders):
                    slider.handle_event(event)
                    self.slider_text_vals[i].set_string(slider.get_value())
                    self.slider_text_vals[i].draw()

                self.awaited_time.set_string(self.get_time_text_from_sliders())
                self.awaited_time.draw()

            pygame.display.update()