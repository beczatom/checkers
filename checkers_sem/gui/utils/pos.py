

class Pos:
    def __init__(self, size : tuple[float, float],
                 margin : tuple[float, float, float, float] = (0, 0, 0, 0),
                 center : bool = False):
        """
        # TODO

        Parameters
        ----------
        size
        margin : tuple[float, float, float, float]
            defined as margin from top, right, bottom, left.
        center
        """
        self.size = size
        self.left_top = (margin[3], margin[0])

        if center:
            left = margin[3] + (1 - margin[1] - margin[3] - size[0]) / 2
            top = margin[0] + (1 - margin[0] - margin[2] - size[1]) / 2

            if left < 0 or top < 0:
                raise ValueError("Too large size for given margin")

            self.left_top = (left, top)

    def __str__(self):
        return f'{self.size}, {self.left_top}'