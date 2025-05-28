"""
This module does the genetic training and shows the partial results
"""

import pygame

from app.gui.utils.window import Window
from app.gui.utils.text import Text
from app.gui.utils.progress_bar import ProgressBar
from app.gui.utils.pos import Pos
from app.state import state
from app.helper import get_coefs_header_text
from app.gui.constants import BACKGROUND_COLOR, BEST_GENETIC_COEFICIENTS_TEXT, \
    AVERAGE_GENETIC_COEFICIENTS_TEXT, DEFAULT_FONT_SIZE, STAT_TEXTS, GENETIC_SETTINGS_TEXT, SLIDER_PROPERTIES
from app.gui.genetic_window.genetic_helper import GeneticHelper


class GeneticWindow(Window):
    """
    This class shows the user how the genetic training is going
    """

    def __init__(self, surface: pygame.surface):
        """
        Initializes the window
        Parameters
        ----------
        surface : pygame.surface
            the window surface
        """
        super().__init__(surface)
        self.surface.fill(BACKGROUND_COLOR)
        pygame.display.flip()

        self.genetic_helper = GeneticHelper()
        self.settings = self.init_setting_options()
        self.coefs = self.init_average_texts()
        self.progress_bar = self.init_bar()

    def init_bar(self) -> ProgressBar:
        """
        Inits progress bar.
        Returns
        -------
        progress_bar : ProgressBar
            initialized progress bar
        """
        progress_bar = ProgressBar(self.surface,
                                   Pos((0.7, 0.15), (0.15, 0.15, 0.7, 0.15)),
                                   value=0)
        return progress_bar

    def init_average_texts(self) -> tuple[Text, list[Text], list[Text]]:
        """
        Initializes average coefficients texts.
        Returns
        -------
        header, text_val_header, text_val : tuple[Text, list[Text], list[Text]]
            header of the block, header of coefficient and the coefficient itself
        """
        header_text = AVERAGE_GENETIC_COEFICIENTS_TEXT + ' pri inicializácii'
        coefs_header = Text(self.surface,
                            Pos((0.45, 0.1), (0.35, 0.05, 0.55, 0.5)),
                            text=header_text)

        coefs_val_headers = []
        coefs_vals = []
        for i, stat_name in enumerate(STAT_TEXTS):
            font_size = 4 * DEFAULT_FONT_SIZE // 5

            coefs_val_headers.append(Text(self.surface,
                                          Pos((0.275, 0.075), (0.475 + i * 0.075, 0.05, 0.45 - i * 0.075, 0.55)),
                                          text=stat_name, font_size=font_size))

            coefs_vals.append(Text(self.surface,
                                   Pos((0.125, 0.075), (0.475 + i * 0.075, 0.05, 0.45 - i * 0.075, 0.8)),
                                   text=self.genetic_helper.get_coefs()[i], font_size=font_size))

        return coefs_header, coefs_val_headers, coefs_vals

    def init_setting_options(self) -> tuple[Text, list[Text], list[Text]]:
        """
        Initializes setting texts.
        Returns
        -------
        header, text_val_header, text_val : tuple[Text, list[Text], list[Text]]
            header of the block, header of setting and the setting itself
        """
        header = Text(self.surface,
                      Pos((0.45, 0.1), (0.35, 0.5, 0.55, 0.05)),
                      text=GENETIC_SETTINGS_TEXT)
        setting_val_headers = []
        setting_val_texts = []

        for i, setting_val in enumerate(state.get_genetic_settings()):
            if i > 3:
                setting_val *= 100
            text, _, _, _ = SLIDER_PROPERTIES[i]
            font_size = 4 * DEFAULT_FONT_SIZE // 5

            setting_val_headers.append(Text(self.surface,
                                            Pos((0.275, 0.075), (0.475 + i * 0.075, 0.675, 0.45 - i * 0.075, 0.05)),
                                            text=text, font_size=font_size))

            setting_val_texts.append(Text(self.surface,
                                          Pos((0.125, 0.075), (0.475 + i * 0.075, 0.55, 0.45 - i * 0.075, 0.325)),
                                          text=setting_val, font_size=font_size))

        return header, setting_val_headers, setting_val_texts

    def update_coefs(self) -> None:
        """
        Update average or final coefficients of training.
        """
        if self.genetic_helper.best_player is None:
            self.coefs[0].set_text(get_coefs_header_text(self.genetic_helper.current_generation))
        else:
            self.coefs[0].set_text(BEST_GENETIC_COEFICIENTS_TEXT)

        self.coefs[0].draw()
        for i, text in enumerate(self.coefs[2]):
            text.set_text(self.genetic_helper.get_coefs()[i])
            text.draw()

    def update_bar(self) -> None:
        """
        Updates progress bar.
        """
        completed_pct = self.genetic_helper.get_completed_pct()
        self.progress_bar.set_value(completed_pct)
        self.progress_bar.draw()

    def refresh(self) -> None:
        """
        Redraws the window
        """
        self.genetic_helper.check_thread()
        self.update_coefs()
        self.update_bar()
        self.settings[0].draw()
        for i, header in enumerate(self.settings[1]):
            header.draw()
            self.settings[2][i].draw()

        self.coefs[0].draw()
        for i in range(len(self.coefs[1])):
            self.coefs[1][i].draw()
            self.coefs[2][i].draw()
