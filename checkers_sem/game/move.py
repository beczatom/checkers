"""
This module takes care of elementary unit of a game - move.
"""

from checkers_sem.game.constants import BitBoard, MoveType, TAKE, PROMOTION


class Move:
    """
    Class to represent a move on the board.
    Holds information about who made the move, from when, to where,
    if it was promotion or taking, if so, then also what was the taken piece type.
    """

    def __init__(self, turn: bool, pos_change: tuple[BitBoard, BitBoard], move_type: MoveType,
                 took_mask: BitBoard = BitBoard(0)):
        self.turn = turn
        self.from_mask = BitBoard(pos_change[0])
        self.to_mask = BitBoard(pos_change[1])
        self.move_type = MoveType(move_type)
        self.took_mask = BitBoard(took_mask)

    def revert(self):
        """
        Changes the from and to mask.

        Returns
        -------
        move : Move
            reverted move
        """

        return Move(self.turn, (self.to_mask, self.from_mask), self.move_type, self.took_mask)

    def is_taking(self) -> bool:
        """
        Returns True if the move is taking.

        Returns
        -------
        is_taking : bool
            True, if the move is taking, false otherwise
        """
        return self.move_type & TAKE

    def is_promoting(self) -> bool:
        """
        Returns True if the move is promoting.

        Returns
        -------
        is_taking : bool
            True, if the move is promoting, false otherwise
        """
        return self.move_type & PROMOTION

    def __eq__(self, other) -> bool:
        """
        Straightforward equality.

        Parameters
        ----------
        other : Move

        Returns
        -------
        eq : bool
            True, if the two moves are equal
        """
        return (self.turn == other.turn and self.from_mask == other.from_mask and self.to_mask == other.to_mask
                and self.move_type == other.move_type and self.took_mask == other.took_mask)

    def __str__(self) -> str:
        """
        Straightforward to string.

        Returns
        -------
        string : str
            Every attribute in one string
        """
        return f'{self.turn} {self.from_mask:08x} {self.to_mask:08x} {self.move_type:02x} {self.took_mask:08x}'

    def __repr__(self) -> str:
        """
        Straightforward repr.

        Returns
        -------
        string : str
            Every attribute in one string
        """
        return self.__str__()

    def __hash__(self):
        """
        Straightforward hash.

        Returns
        -------
        hash : int
            Hash of class as tuple of its attributes
        """
        return hash((self.turn, self.from_mask, self.to_mask, self.move_type, self.took_mask))
