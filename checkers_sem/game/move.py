from checkers_sem.constants import *

class Move:
    def __init__(self, turn : Turn, from_mask : BitBoard, to_mask : BitBoard, move_type: MoveType, took_mask : BitBoard = BitBoard(0)):
        self.turn = turn
        self.from_mask = BitBoard(from_mask)
        self.to_mask = BitBoard(to_mask)
        self.move_type = MoveType(move_type)
        self.took_mask = BitBoard(took_mask)

    def revert(self):
        return Move(self.turn, self.to_mask, self.from_mask, self.move_type, self.took_mask)

    def is_taking(self) -> bool:
        return self.move_type & TAKE

    def is_promoting(self) -> bool:
        return self.move_type & PROMOTION

    # ciste na testovanie
    def __eq__(self, other):
        return (self.turn == other.turn and self.from_mask == other.from_mask and self.to_mask == other.to_mask
                and self.move_type == other.move_type and self.took_mask == other.took_mask)

    def __str__(self):
        return f'{self.turn} {self.from_mask:08x} {self.to_mask:08x} {self.move_type:02x} {self.took_mask:08x}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.turn, self.from_mask, self.to_mask, self.move_type, self.took_mask))