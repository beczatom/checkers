"""
This module takes care of defining where to place widgets.
"""


class Pos:
    """
    Position class.
    """

    def __init__(self, size: tuple[float, float],
                 margin: tuple[float, float, float, float] = (0, 0, 0, 0),
                 center: bool = False):
        """
        Takes care of positioning the widgets.
        Parameters
        ----------
        size : tuple[float, float]
            relative size of the widget
        margin : tuple[float, float, float, float]
            relative margin from top, right, bottom, left.
        center : bool
            if we need to recalculate the margins,
            so the rectangle of given size would be in center

        Raises
        ------
        error : ValueError
            if the size doesn't fit to margins
        """
        self.size = size
        self.left_top = (margin[3], margin[0])

        if center:
            left = margin[3] + (1 - margin[1] - margin[3] - size[0]) / 2
            top = margin[0] + (1 - margin[0] - margin[2] - size[1]) / 2

            if left < 0 or top < 0:
                raise ValueError("Too large size for given margin")

            self.left_top = (left, top)

    def get_size(self) -> tuple[float, float]:
        """
        Gets size.
        Absolutely useless, because can be directly accessed,
        but pylint wouldn't survive if there wasn't two public methods.
        Returns
        -------
        size : tuple[float, float]
            relative size of the widget
        """
        return self.size

    def get_left_top(self) -> tuple[float, float]:
        """
        Gets left_top.
        Absolutely useless, because can be directly accessed,
        but pylint wouldn't survive if there wasn't two public methods.
        Returns
        -------
        left_top : tuple[float, float]
            relative left_top of the widget
        """
        return self.left_top
