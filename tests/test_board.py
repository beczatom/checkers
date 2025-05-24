import copy

import pytest
import numpy as np

from checkers_sem.game.board import Board, make_gen, is_color
from checkers_sem.game.move import Move
from checkers_sem.game.constants import BitBoard, Color, MoveType, PROMOTION, Piece, EVEN_ROW, TAKE

def dummy_fun_make_gen_test(bitboard : BitBoard) -> list[int] :

    assert bitboard.bit_count() == 1

    if (bitboard % 3) == 1: return []

    return [1]

@pytest.mark.parametrize('gen_range, color', [
    (range(32), BitBoard(0x00000001)),
    (range(32), BitBoard(0x0000000f)),
    (range(16), BitBoard(0xf0000000)),
    (range(7), BitBoard(0xf0000040)),
    (range(3), BitBoard(0x000f0000))
])
def test_make_gen(gen_range : range, color : BitBoard):

    # range_mask will be an unsigned integer with zeros and ones repetition
    # on first len(range) positions
    # the used dummy function, returns something in every second iteration through range
    # and the generator enables the function when bit in color is true
    # so the length of generator must be the bit count of bitwise and
    range_mask = BitBoard(0)
    i = len(gen_range)
    while i > 0:
        i -= 1
        if i % 2 == 0: continue
        range_mask |= (1 << i)

    iterations = 0
    for x in make_gen(gen_range, color, dummy_fun_make_gen_test):
        assert x == 1
        iterations += 1
    assert iterations == (range_mask & color).bit_count()

@pytest.mark.parametrize('mask, color, true_val', [
    (BitBoard(0x00000001), BitBoard(0xffffffff), True),
    (BitBoard(0x00000000), BitBoard(0xffffffff), False),
    (BitBoard(0x10000000), BitBoard(0x12345678), True),
    (BitBoard(0x01000000), BitBoard(0x12345678), False),
    (BitBoard(0x00100000), BitBoard(0x12345678), True),
    (BitBoard(0x00010000), BitBoard(0x12345678), False),
    (BitBoard(0x00001000), BitBoard(0x12345678), True),
    (BitBoard(0x00000100), BitBoard(0x12345678), False),
    (BitBoard(0x00000010), BitBoard(0x12345678), True),
    (BitBoard(0x00000001), BitBoard(0x12345678), False),
    (BitBoard(0x40000000), BitBoard(0x9abcdef0), False),
    (BitBoard(0x04000000), BitBoard(0x9abcdef0), False),
    (BitBoard(0x00400000), BitBoard(0x9abcdef0), False),
    (BitBoard(0x00040000), BitBoard(0x9abcdef0), True),
    (BitBoard(0x00004000), BitBoard(0x9abcdef0), True),
    (BitBoard(0x00000400), BitBoard(0x9abcdef0), True),
    (BitBoard(0x00000040), BitBoard(0x9abcdef0), True),
    (BitBoard(0x00000004), BitBoard(0x9abcdef0), False),
])
def test_is_color(mask : BitBoard, color : BitBoard, true_val : bool):
    assert bool(is_color(mask, color)) == true_val

@pytest.mark.parametrize('turn, pawns, mask, target_mask, true_val',[
    (Color.WHITE, BitBoard(0xf0000001), BitBoard(0x00000001), BitBoard(0x00000010), False),
    (Color.BLACK, BitBoard(0xf0000001), BitBoard(0x00000001), BitBoard(0x00000010), False),
    (Color.WHITE, BitBoard(0xe000000f), BitBoard(0x10000000), BitBoard(0x01000000), False),
    (Color.BLACK, BitBoard(0xe000000f), BitBoard(0x80000000), BitBoard(0x08000000), False),
    (Color.WHITE, BitBoard(0x0400f000), BitBoard(0x04000000), BitBoard(0x40000000), True),
    (Color.BLACK, BitBoard(0x0400f000), BitBoard(0x02000000), BitBoard(0x20000000), False),
    (Color.WHITE, BitBoard(0x00f00040), BitBoard(0x00000080), BitBoard(0x00000008), False),
    (Color.BLACK, BitBoard(0x00f00040), BitBoard(0x00000040), BitBoard(0x00000004), True),
    (Color.WHITE, BitBoard(0x0ff00000), BitBoard(0x00100000), BitBoard(0x20000000), True),
    (Color.BLACK, BitBoard(0x00000ff0), BitBoard(0x00000100), BitBoard(0x00000002), True),
])
def test_is_promotion(turn : bool, pawns : BitBoard, mask : BitBoard, target_mask : BitBoard, true_val : bool):
    board = Board()
    board.pawns = pawns
    board.turn = turn

    assert bool(board.is_promotion(mask, target_mask)) == true_val

@pytest.mark.parametrize('white, black, mask, true_val',[
    (BitBoard(0x01234567), BitBoard(0x10180008), BitBoard(0x10000000), False),
    (BitBoard(0x01234567), BitBoard(0x10180008), BitBoard(0x01000000), False),
    (BitBoard(0x01234567), BitBoard(0x10180008), BitBoard(0x00000001), False),
    (BitBoard(0x01234567), BitBoard(0x10180008), BitBoard(0x00080000), False),
    (BitBoard(0x01234567), BitBoard(0x10180008), BitBoard(0x80000000), True),
    (BitBoard(0x89abcdef), BitBoard(0x12000000), BitBoard(0x20000000), True),
    (BitBoard(0x89abcdef), BitBoard(0x12000000), BitBoard(0x00100000), True),
    (BitBoard(0x89abcdef), BitBoard(0x12000000), BitBoard(0x00000004), False),
    (BitBoard(0x89abcdef), BitBoard(0x12000000), BitBoard(0x00040000), True),
    (BitBoard(0x89abcdef), BitBoard(0x12000000), BitBoard(0x00000010), True),
])
def test_is_free(white: BitBoard, black : BitBoard, mask : BitBoard, true_val : bool):
    board = Board()
    board.white = white
    board.black = black

    assert bool(board.is_free(mask)) == true_val

@pytest.mark.parametrize('pawns, mask, true_val',[
    (BitBoard(0x01234567), BitBoard(0x10000000), Piece.KING),
    (BitBoard(0x01234567), BitBoard(0x01000000), Piece.PAWN),
    (BitBoard(0x01234567), BitBoard(0x00100000), Piece.KING),
    (BitBoard(0x01234567), BitBoard(0x00010000), Piece.PAWN),
    (BitBoard(0x01234567), BitBoard(0x00001000), Piece.KING),
])
def test_get_fig_type(pawns: BitBoard, mask : BitBoard, true_val : bool):
    board = Board()
    board.pawns = pawns

    assert board.get_fig_type(mask) == true_val

def test_is_valid_attacking_move():
    board = Board()
    board.white = BitBoard(0x0000200f)
    board.black = BitBoard(0x000204c0)
    board.pawns = BitBoard(0x0002204f)

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x p x _ x
    # x _ x _ x P x _
    # _ x k x _ x _ x
    # x k x p x _ x _
    # P x P x P x P x

    assert board.is_valid_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000008), BitBoard(0x00000400)), MoveType(), BitBoard(0x00000080)),
        board.black, EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000800)), MoveType(), BitBoard(0x00000080)),
        board.black, EVEN_ROW) == True

    assert board.is_valid_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000400)), MoveType(), BitBoard(0x00000040)),
        board.black, EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000100)), MoveType(), BitBoard(0x00000020)),
        board.black, EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000200)), MoveType(), BitBoard(0x00000020)),
        board.black, EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType(), BitBoard(0x00000000)),
        board.white, ~EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000004)), MoveType(), BitBoard(0x00000000)),
        board.white, ~EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00010000)), MoveType(), BitBoard(0x00008000)),
        board.white, ~EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00004000)), MoveType(), BitBoard(0x00000400)),
        board.white, ~EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000040), BitBoard(0x00000002)), MoveType(), BitBoard(0x00000000)),
        board.white, ~EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000040), BitBoard(0x00000004)), MoveType(), BitBoard(0x00000000)),
        board.white, ~EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00010000)), MoveType(), BitBoard(0x00010000)),
        board.black, ~EVEN_ROW) == False

    assert board.is_valid_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00004000)), MoveType(), BitBoard(0x00020000)),
        board.black, ~EVEN_ROW) == True

    assert board.is_valid_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00000100)), MoveType(), BitBoard(0x00002000)),
        board.white, EVEN_ROW) == True

    assert board.is_valid_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00000400)), MoveType(), BitBoard(0x00004000)),
        board.white, EVEN_ROW) == False

def test_validate_attacking_move():
    board = Board()
    board.white = BitBoard(0x0080200f)
    board.black = BitBoard(0x040204c0)
    board.pawns = BitBoard(0x0482204f)

    # x _ x _ x _ x _
    # _ x p x _ x _ x
    # x P x _ x _ x _
    # _ x _ x p x _ x
    # x _ x _ x P x _
    # _ x k x _ x _ x
    # x k x p x _ x _
    # P x P x P x P x

    assert board.validate_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000008), BitBoard(0x00000400)), MoveType(), BitBoard(0x00000080)),
        board.black, EVEN_ROW) is None

    possible_move = Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000800)), MoveType(), BitBoard(0x00000080))
    true_validated_move = copy.deepcopy(possible_move)
    true_validated_move.move_type = MoveType() | TAKE | Piece.KING

    assert possible_move != true_validated_move

    assert board.validate_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000800)), MoveType(), BitBoard(0x00000080)),
        board.black, EVEN_ROW) == true_validated_move

    assert board.validate_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000400)), MoveType(), BitBoard(0x00000040)),
        board.black, EVEN_ROW) is None

    assert board.validate_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000100)), MoveType(), BitBoard(0x00000020)),
        board.black, EVEN_ROW) is None

    assert board.validate_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000200)), MoveType(), BitBoard(0x00000020)),
        board.black, EVEN_ROW) is None

    assert board.validate_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType(), BitBoard(0x00000000)),
        board.white, ~EVEN_ROW) is None

    assert board.validate_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000004)), MoveType(), BitBoard(0x00000000)),
        board.white, ~EVEN_ROW) is None

    assert board.validate_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00010000)), MoveType(), BitBoard(0x00008000)),
        board.white, ~EVEN_ROW) is None

    assert board.validate_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00004000)), MoveType(), BitBoard(0x00000400)),
        board.white, ~EVEN_ROW) is None

    assert board.validate_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000040), BitBoard(0x00000002)), MoveType(), BitBoard(0x00000000)),
        board.white, ~EVEN_ROW) is None

    assert board.validate_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000040), BitBoard(0x00000004)), MoveType(), BitBoard(0x00000000)),
        board.white, ~EVEN_ROW) is None

    assert board.validate_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00010000)), MoveType(), BitBoard(0x00010000)),
        board.black, ~EVEN_ROW) is None

    possible_move = Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00400000)), MoveType(), BitBoard(0x00020000))
    true_validated_move = copy.deepcopy(possible_move)
    true_validated_move.move_type = MoveType() | TAKE | Piece.PAWN

    assert possible_move != true_validated_move

    assert board.validate_attacking_move(possible_move, board.black, ~EVEN_ROW) == true_validated_move

    possible_move = Move(Color.BLACK, (BitBoard(0x00002000), BitBoard(0x00000100)), MoveType(), BitBoard(0x00002000))
    true_validated_move = copy.deepcopy(possible_move)
    true_validated_move.move_type = MoveType() | TAKE | Piece.PAWN

    assert possible_move != true_validated_move

    assert board.validate_attacking_move(possible_move, board.white, EVEN_ROW) == true_validated_move

    assert board.validate_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00000400)), MoveType(), BitBoard(0x00004000)),
        board.white, EVEN_ROW) is None


    possible_move = Move(Color.WHITE, (BitBoard(0x00800000), BitBoard(0x40004000)), MoveType(), BitBoard(0x04000000))
    true_validated_move = copy.deepcopy(possible_move)
    true_validated_move.move_type = MoveType() | TAKE | PROMOTION | Piece.PAWN

    assert possible_move != true_validated_move

    assert board.validate_attacking_move(possible_move, board.black, ~EVEN_ROW) == true_validated_move

    possible_move = Move(Color.BLACK, (BitBoard(0x04000000), BitBoard(0x00080000)), MoveType(), BitBoard(0x00800000))
    true_validated_move = copy.deepcopy(possible_move)
    true_validated_move.move_type = MoveType() | TAKE | Piece.PAWN

    assert possible_move != true_validated_move

    assert board.validate_attacking_move(possible_move, board.white, EVEN_ROW) == true_validated_move

def test_attacking_moves_in_direction():
    board = Board()
    board.white = BitBoard(0x0000000f)
    board.black = BitBoard(0x00000000)
    board.pawns = board.white | board.black

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # P x P x P x P x

    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000008), moves, board.black, True)
    assert moves == []
    board.attacking_moves_in_direction(BitBoard(0x00000004), moves, board.black, True)
    assert moves == []
    board.attacking_moves_in_direction(BitBoard(0x00000002), moves, board.black, True)
    assert moves == []
    board.attacking_moves_in_direction(BitBoard(0x00000001), moves, board.black, True)
    assert moves == []

    board.black = BitBoard(0x00000040)
    board.pawns = board.white | board.black

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x p x _ x _
    # P x P x P x P x

    board.attacking_moves_in_direction(BitBoard(0x00000008), moves, board.black, True)
    assert moves == []

    board.attacking_moves_in_direction(BitBoard(0x00000004), moves, board.black, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000200)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000002), moves, board.black, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000001), moves, board.black, True)
    assert moves == []

    board.black = BitBoard(0x000800d0)
    board.white = BitBoard(0x0000800f)
    board.pawns = BitBoard(0x0008805f)

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # p x _ x _ x _ x
    # x P x _ x _ x _
    # _ x _ x _ x _ x
    # x k x p x _ x p
    # P x P x P x P x

    board.attacking_moves_in_direction(BitBoard(0x00000008), moves, board.black, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000008), BitBoard(0x00000400)), MoveType() | TAKE | Piece.KING, BitBoard(0x00000080))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000004), moves, board.black, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000200)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040)),
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000800)), MoveType() | TAKE | Piece.KING, BitBoard(0x00000080))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000002), moves, board.black, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000001), moves, board.black, True)

    assert moves == []

    board.turn = Color.BLACK
    board.attacking_moves_in_direction(BitBoard(0x00080000), moves, board.white, False)
    assert moves == [Move(Color.BLACK, (BitBoard(0x00080000), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00008000))]
    moves = []


    board.black = BitBoard(0x00000d00)
    board.white = BitBoard(0x000000f0)
    board.pawns = BitBoard(0x000009f0)

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x _ x _ x _ x

    board.turn = Color.WHITE

    board.attacking_moves_in_direction(BitBoard(0x00000080), moves, board.black, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00004000)), MoveType() | TAKE | Piece.KING, BitBoard(0x00000400))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000040), moves, board.black, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000040), BitBoard(0x00008000)), MoveType() | TAKE | Piece.KING, BitBoard(0x00000400))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000020), moves, board.black, True)
    assert moves == [ Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00001000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000010), moves, board.black, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000010), BitBoard(0x00002000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100))]
    moves = []

    board.turn = Color.BLACK

    board.attacking_moves_in_direction(BitBoard(0x00000800), moves, board.white, False)
    assert moves == [Move(Color.BLACK, (BitBoard(0x00000800), BitBoard(0x00000004)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000080))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000400), moves, board.white, False)
    assert moves == [Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000002)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040)),
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080))]
    moves = []

    board.attacking_moves_in_direction(BitBoard(0x00000100), moves, board.white, False)
    assert moves == [Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020))]
    moves = []

def test_is_valid_not_attacking_move():
    board = Board()
    board.black = BitBoard(0xf1410240)
    board.white = BitBoard(0x040000bf)
    board.pawns = board.white | board.black

    # x p x p x p x p
    # _ x P x _ x p x
    # x _ x p x _ x _
    # _ x _ x _ x p x
    # x _ x _ x _ x _
    # _ x _ x p x _ x
    # x P x p x P x P
    # P x P x P x P x

    board.turn = Color.BLACK

    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x80000000), BitBoard(0x08000000)), MoveType()), ~EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x40000000), BitBoard(0x02000000)), MoveType()), ~EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x20000000), BitBoard(0x02000000)), MoveType()), ~EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType()), ~EVEN_ROW) == False
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x10000000), BitBoard(0x00800000)), MoveType()), ~EVEN_ROW) == False

    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x01000000), BitBoard(0x00100000)), MoveType()), EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x01000000), BitBoard(0x00200000)), MoveType()), EVEN_ROW) == True

    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00400000), BitBoard(0x00040000)), MoveType()), ~EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00400000), BitBoard(0x00020000)), MoveType()), ~EVEN_ROW) == True

    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00010000), BitBoard(0x00001000)), MoveType()), EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00010000), BitBoard(0x00002000)), MoveType()), EVEN_ROW) == True

    board.turn = Color.WHITE

    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x80000000)), MoveType()), EVEN_ROW) == False
    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x40000000)), MoveType()), EVEN_ROW) == False

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x k x _ x
    # x _ x _ x P x _
    # _ x P x _ x _ x
    # x K x _ x _ x _
    # _ x _ x _ x k x

    board.black = BitBoard(0x00020001)
    board.white = BitBoard(0x00002480)
    board.pawns = BitBoard(0x00002400)

    board.turn = Color.BLACK

    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00200000)), MoveType()), EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00400000)), MoveType()), EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00004000)), MoveType()), EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00002000)), MoveType()), EVEN_ROW) == False

    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000001), BitBoard(0x00000010)), MoveType()), EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000001), BitBoard(0x00000020)), MoveType()), EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.BLACK, (BitBoard(0x00000001), BitBoard(0x00000000)), MoveType()), EVEN_ROW) == False

    board.turn = Color.WHITE

    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00010000)), MoveType()), ~EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00020000)), MoveType()), ~EVEN_ROW) == False

    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000400), BitBoard(0x00004000)), MoveType()), EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000400), BitBoard(0x00008000)), MoveType()), EVEN_ROW) == True

    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType()), ~EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType()), ~EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000004)), MoveType()), ~EVEN_ROW) == True
    assert board.is_valid_not_attacking_move(
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000400)), MoveType()), ~EVEN_ROW) == False

def test_validate_not_attacking_move():
    board = Board()

    # x _ x _ x _ x _
    # K x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x k x _ x
    # x _ x _ x P x _
    # _ x P x _ x _ x
    # x K x _ x _ x _
    # _ x _ x _ x k x

    board.black = BitBoard(0x00020001)
    board.white = BitBoard(0x0c002480)
    board.pawns = BitBoard(0x04002400)

    possible_move = Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00010000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, ~EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00020000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, ~EVEN_ROW) is None

    possible_move = Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType())
    assert board.validate_not_attacking_move(possible_move, ~EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType())
    assert board.validate_not_attacking_move(possible_move, ~EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000004)), MoveType())
    assert board.validate_not_attacking_move(possible_move, ~EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000400)), MoveType())
    assert board.validate_not_attacking_move(possible_move, ~EVEN_ROW) is None

    possible_move = Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x40000000)), MoveType())
    true_validated_move = Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x40000000)), MoveType() | PROMOTION)
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) == true_validated_move

    possible_move = Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x80000000)), MoveType())
    true_validated_move = Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x80000000)), MoveType() | PROMOTION)
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) == true_validated_move

    possible_move = Move(Color.WHITE, (BitBoard(0x08000000), BitBoard(0x00000000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) is None

    possible_move = Move(Color.WHITE, (BitBoard(0x08000000), BitBoard(0x80000000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x08000000), BitBoard(0x00800000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x08000000), BitBoard(0x01000000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) is None

    board.turn = Color.BLACK

    possible_move = Move(Color.WHITE, (BitBoard(0x00020000), BitBoard(0x00200000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x00020000), BitBoard(0x00400000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x00020000), BitBoard(0x00004000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x00020000), BitBoard(0x00002000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) is None

    possible_move = Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000010)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000020)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) == possible_move

    possible_move = Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000000)), MoveType())
    assert board.validate_not_attacking_move(possible_move, EVEN_ROW) is None

def test_not_attacking_moves_in_direction():
    board = Board()

    # x _ x _ x _ x _
    # K x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x k x _ x
    # x _ x _ x P x _
    # _ x P x _ x _ x
    # x K x _ x _ x _
    # _ x _ x _ x k x

    board.black = BitBoard(0x00020001)
    board.white = BitBoard(0x0c002480)
    board.pawns = BitBoard(0x04002400)

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x00002000), moves,True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00010000)), MoveType())]

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x00000080), moves, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType())]

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x00000080), moves, False)
    assert moves == [Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType()),
                     Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000004)), MoveType())]

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x04000000), moves, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x40000000)), MoveType() | PROMOTION),
                     Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x80000000)), MoveType() | PROMOTION)]

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x08000000), moves, True)
    assert moves == [Move(Color.WHITE, (BitBoard(0x08000000), BitBoard(0x80000000)), MoveType())]

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x08000000), moves, False)
    assert moves == [Move(Color.WHITE, (BitBoard(0x08000000), BitBoard(0x00800000)), MoveType())]

    board.turn = Color.BLACK

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x00020000), moves, True)
    assert moves == [Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00200000)), MoveType()),
                     Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00400000)), MoveType())]

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x00020000), moves, False)
    assert moves == [Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00004000)), MoveType())]

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x00000001), moves, True)
    assert moves == [Move(Color.BLACK, (BitBoard(0x00000001), BitBoard(0x00000010)), MoveType()),
                     Move(Color.BLACK, (BitBoard(0x00000001), BitBoard(0x00000020)), MoveType())]

    moves = []
    board.not_attacking_moves_in_direction(BitBoard(0x00000001), moves, False)
    assert moves == []

@pytest.mark.parametrize('white, black, pawns, true_stats', [
    (BitBoard(0x0000000f), BitBoard(0x00000000), BitBoard(0x00000004), [1, 3, 0, 1, 4, 0]),
    (BitBoard(0x0000000f), BitBoard(0x11111110), BitBoard(0x01000004), [0, -3, 0, -3, 3, 0]),
    (BitBoard(0x0000000f), BitBoard(0x11151110), BitBoard(0x00040004), [0, -4, 0, -3, 3, -1]),
    (BitBoard(0x0100000f), BitBoard(0x88888880), BitBoard(0x09000004), [1, -3, 1, -2, 3, 0]),
])
def test_stats(white : BitBoard, black : BitBoard, pawns : BitBoard, true_stats : np.array):
    board = Board()
    board.white = white
    board.black = black
    board.pawns = pawns

    assert np.array_equal(board.stats(), np.array(true_stats))

@pytest.mark.parametrize('init_board_tuple, move, ref_board_tuple', [
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00800000)),
        (BitBoard(0x040040f4), BitBoard(0x00008d00), BitBoard(0x0400c9f4))
    ),
    (
        (BitBoard(0x040040f4), BitBoard(0x00008d00), BitBoard(0x0400c9f4)),
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080)),
        (BitBoard(0x04004074), BitBoard(0x00008908), BitBoard(0x0400c974))
    ),
    (
        (BitBoard(0x04004074), BitBoard(0x00008908), BitBoard(0x0400c974)),
        Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020)),
        (BitBoard(0x04004054), BitBoard(0x0000880a), BitBoard(0x0400c854))
    ),
    (
        (BitBoard(0x04004054), BitBoard(0x0000880a), BitBoard(0x0400c854)),
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)),
        (BitBoard(0x040040d0), BitBoard(0x0000880a), BitBoard(0x0400c8d0))
    ),
    (
        (BitBoard(0x040040d0), BitBoard(0x0000880a), BitBoard(0x0400c8d0)),
        Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080)),
        (BitBoard(0x04004050), BitBoard(0x00008c02), BitBoard(0x0400c850))
    ),
    (
        (BitBoard(0x04004050), BitBoard(0x00008c02), BitBoard(0x0400c850)),
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00020000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00004000)),
        (BitBoard(0x04000050), BitBoard(0x00028802), BitBoard(0x04008850))
    ),
    (
        (BitBoard(0x04000050), BitBoard(0x00028802), BitBoard(0x04008850)),
        Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x80000000)), MoveType(0x01), BitBoard(0x00000000)),
        (BitBoard(0x80000050), BitBoard(0x00028802), BitBoard(0x00008850))
    ),
    (
        (BitBoard(0x00800000), BitBoard(0x06000000), BitBoard(0x06800000)),
        Move(Color.WHITE, (BitBoard(0x00800000), BitBoard(0x40000000)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x04000000)),
        (BitBoard(0x40000000), BitBoard(0x02000000), BitBoard(0x02000000))
    ),
])
def test_make_move_changes(init_board_tuple : tuple[BitBoard, BitBoard, BitBoard], move,  ref_board_tuple : tuple[BitBoard, BitBoard, BitBoard]):
    board = Board()
    board.white = init_board_tuple[0]
    board.black = init_board_tuple[1]
    board.pawns = init_board_tuple[2]

    if move.turn == Color.WHITE:
        white, black = board.make_move_changes(move, board.white, board.black)
    else:
        black, white = board.make_move_changes(move, board.black, board.white)

    assert white == ref_board_tuple[0]
    assert black == ref_board_tuple[1]
    assert board.pawns == ref_board_tuple[2]

@pytest.mark.parametrize('init_board_tuple, white_ref_set, black_ref_set', [
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        {
            Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType(), BitBoard(0x00000000)),
            Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000400)), MoveType(), BitBoard(0x00000000)),
            Move(Color.WHITE, (BitBoard(0x00000040), BitBoard(0x00000400)), MoveType(), BitBoard(0x00000000)),
            Move(Color.WHITE, (BitBoard(0x00000040), BitBoard(0x00000200)), MoveType(), BitBoard(0x00000000)),
            Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00000200)), MoveType(), BitBoard(0x00000000)),
            Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00000100)), MoveType(), BitBoard(0x00000000)),
            Move(Color.WHITE, (BitBoard(0x00000010), BitBoard(0x00000100)), MoveType(), BitBoard(0x00000000)),
        },
        {
            Move(Color.BLACK, (BitBoard(0x08000000), BitBoard(0x00800000)), MoveType(), BitBoard(0x00000000)),
            Move(Color.BLACK, (BitBoard(0x04000000), BitBoard(0x00800000)), MoveType(), BitBoard(0x00000000)),
            Move(Color.BLACK, (BitBoard(0x04000000), BitBoard(0x00400000)), MoveType(), BitBoard(0x00000000)),
            Move(Color.BLACK, (BitBoard(0x02000000), BitBoard(0x00400000)), MoveType(), BitBoard(0x00000000)),
            Move(Color.BLACK, (BitBoard(0x02000000), BitBoard(0x00200000)), MoveType(), BitBoard(0x00000000)),
            Move(Color.BLACK, (BitBoard(0x01000000), BitBoard(0x00200000)), MoveType(), BitBoard(0x00000000)),
            Move(Color.BLACK, (BitBoard(0x01000000), BitBoard(0x00100000)), MoveType(), BitBoard(0x00000000))
        }
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        {
            Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00800000)),
            Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00001000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100)),
            Move(Color.WHITE, (BitBoard(0x00000010), BitBoard(0x00002000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100))
        },
        {
            Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00020000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00004000)),
            Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000002)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040)),
            Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080)),
            Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020))
        }
    ),
])
def test_get_legal_moves(init_board_tuple : tuple[BitBoard, BitBoard, BitBoard], white_ref_set : set[Move], black_ref_set : set[Move]):
    board = Board()
    board.white = init_board_tuple[0]
    board.black = init_board_tuple[1]
    board.pawns = init_board_tuple[2]


    moves = set()
    for move in board.get_legal_moves():
        moves.add(move)

    assert moves == white_ref_set

    board.turn = Color.BLACK

    moves = set()
    for move in board.get_legal_moves():
        moves.add(move)

    assert moves == black_ref_set


def test_not_attacking_moves_from_pos():
    board = Board()
    board.white = BitBoard(0x0000000f)
    board.black = BitBoard(0x00000000)
    board.pawns = board.white | board.black
    
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # P x P x P x P x

    assert (board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == [
        Move(Color.WHITE, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType())])
    assert (board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType())])
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000020)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000040)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == [
        Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000010)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000020)), MoveType())]

    board.black = BitBoard(0x00000040)
    board.pawns = board.white | board.black
    
    # x _ x _ x _ x _
    # _ x _ x _ x _ x 
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x p x _ x _
    # P x P x P x P x

    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == [
        Move(Color.WHITE, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000020)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == [
        Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000010)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000020)), MoveType())]

    board.white = BitBoard(0x0000008f)
    board.pawns = board.white | board.black
    
    # x _ x _ x _ x _
    # _ x _ x _ x _ x 
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x_ x _
    # _ x _ x _ x _ x
    # x P x p x _ x _
    # P x P x P x P x
    
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000020)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == [
        Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000010)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000001), BitBoard(0x00000020)), MoveType())]

    board.white = BitBoard(0x000000bf)
    board.black = BitBoard(0x00000240)
    board.pawns = board.white | board.black
    
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x p x _ x
    # x P x p x P x P
    # P x P x P x P x
    
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000400)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000020)) == [
        Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00000100)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000010)) == [
        Move(Color.WHITE, (BitBoard(0x00000010), BitBoard(0x00000100)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x10000000)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000040)) == []

    board.black = BitBoard(0xf1410240)
    board.white = BitBoard(0x040000bf)
    board.pawns = board.white | board.black
    
    # x p x p x p x p
    # _ x P x _ x p x
    # x _ x p x _ x _
    # _ x _ x _ x p x
    # x _ x _ x _ x _
    # _ x _ x p x _ x
    # x P x p x P x P
    # P x P x P x P x

    board.turn = Color.BLACK

    assert board.not_attacking_moves_from_pos(BitBoard(0x80000000)) == [
        Move(Color.BLACK, (BitBoard(0x80000000), BitBoard(0x08000000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x40000000)) == [
        Move(Color.BLACK, (BitBoard(0x40000000), BitBoard(0x02000000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x20000000)) == [
        Move(Color.BLACK, (BitBoard(0x20000000), BitBoard(0x02000000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x10000000)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x01000000)) == [
        Move(Color.BLACK, (BitBoard(0x01000000), BitBoard(0x00100000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x01000000), BitBoard(0x00200000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00400000)) == [
        Move(Color.BLACK, (BitBoard(0x00400000), BitBoard(0x00040000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00400000), BitBoard(0x00020000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00010000)) == [
        Move(Color.BLACK, (BitBoard(0x00010000), BitBoard(0x00001000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00010000), BitBoard(0x00002000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x04000000)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000800)) == []

    # x _ x _ x _ x _
    # _ x _ x _ x _ x 
    # x _ x _ x _ x _
    # _ x _ x k x _ x
    # x _ x _ x P x _
    # _ x P x _ x _ x
    # x K x _ x _ x _
    # _ x _ x _ x k x
    
    board.black = BitBoard(0x00020001)
    board.white = BitBoard(0x00002480)
    board.pawns = BitBoard(0x00002400)

    assert board.not_attacking_moves_from_pos(BitBoard(0x00020000)) == [
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00200000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00400000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00004000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == [
        Move(Color.BLACK, (BitBoard(0x00000001), BitBoard(0x00000010)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00000001), BitBoard(0x00000020)), MoveType())]

    board.turn = Color.WHITE

    assert board.not_attacking_moves_from_pos(BitBoard(0x00002000)) == [
        Move(Color.WHITE, (BitBoard(0x00002000), BitBoard(0x00010000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000400)) == [
        Move(Color.WHITE, (BitBoard(0x00000400), BitBoard(0x00004000)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000400), BitBoard(0x00008000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType()),
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000004)), MoveType())]

    # x _ x p x _ x _
    # P x _ x P x P x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x k x p x _ x p
    # _ x _ x P x _ x
    
    board.black = BitBoard(0x400000d0)
    board.white = BitBoard(0x0b000002)
    board.pawns = BitBoard(0x4b000052)


    assert board.not_attacking_moves_from_pos(BitBoard(0x08000000)) == [
        Move(Color.WHITE, (BitBoard(0x08000000), BitBoard(0x80000000)), MoveType() | PROMOTION)]
    assert board.not_attacking_moves_from_pos(BitBoard(0x02000000)) == [
        Move(Color.WHITE, (BitBoard(0x02000000), BitBoard(0x20000000)), MoveType() | PROMOTION)]
    assert board.not_attacking_moves_from_pos(BitBoard(0x01000000)) == [
        Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType() | PROMOTION),
        Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x20000000)), MoveType() | PROMOTION)
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000020)), MoveType())]

    board.turn = Color.BLACK

    assert board.not_attacking_moves_from_pos(BitBoard(0x40000000)) == [
        Move(Color.BLACK, (BitBoard(0x40000000), BitBoard(0x04000000)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000400)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000004)), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000040)) == [
        Move(Color.BLACK, (BitBoard(0x00000040), BitBoard(0x00000004)), MoveType() | PROMOTION)]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000010)) == [
        Move(Color.BLACK, (BitBoard(0x00000010), BitBoard(0x00000001)), MoveType() | PROMOTION)]

def test_attacking_moves_from_pos():
    board = Board()
    board.white = BitBoard(0x0000000f)
    board.black = BitBoard(0x00000000)
    board.pawns = board.white | board.black

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # P x P x P x P x

    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000002)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000001)) == []

    board.black = BitBoard(0x00000040)
    board.pawns = board.white | board.black

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _ 
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x p x _ x _
    # P x P x P x P x

    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000200)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000001)) == []

    board.black = BitBoard(0x000800d0)
    board.white = BitBoard(0x0000800f)
    board.pawns = BitBoard(0x0008805f)

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # p x _ x _ x _ x
    # x P x _ x _ x _
    # _ x _ x _ x _ x
    # x k x p x _ x p
    # P x P x P x P x

    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == [
        Move(Color.WHITE, (BitBoard(0x00000008), BitBoard(0x00000400)), MoveType() | TAKE | Piece.KING, BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000200)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040)),
        Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000800)), MoveType() | TAKE | Piece.KING, BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Color.WHITE, (BitBoard(0x00000002), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000001)) == []

    board.turn = Color.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x00080000)) == [
        Move(Color.BLACK, (BitBoard(0x00080000), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00008000))]

    board.black = BitBoard(0x00000d00)
    board.white = BitBoard(0x000000f0)
    board.pawns = BitBoard(0x000009f0)

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x _ x _ x _ x

    board.turn = Color.WHITE
    assert board.attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00004000)), MoveType() | TAKE | Piece.KING, BitBoard(0x00000400))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000040)) == [
        Move(Color.WHITE, (BitBoard(0x00000040), BitBoard(0x00008000)), MoveType() | TAKE | Piece.KING, BitBoard(0x00000400))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000020)) == [
        Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00001000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000010)) == [
        Move(Color.WHITE, (BitBoard(0x00000010), BitBoard(0x00002000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100))]

    board.turn = Color.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x00000800)) == [
        Move(Color.BLACK, (BitBoard(0x00000800), BitBoard(0x00000004)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000400)) == [
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000002)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040)),
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000100)) == [
        Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020))]

    board.black = BitBoard(0x00808d00)
    board.white = BitBoard(0x000840f4)
    board.pawns = BitBoard(0x0088c9f4)

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x _ x _ x _
    # P x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x P x _ x _ x

    board.turn = Color.WHITE
    assert board.attacking_moves_from_pos(BitBoard(0x00800000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00080000)) == [
        Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00800000))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000080)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000040)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000020)) == [
        Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00001000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000010)) == [
        Move(Color.WHITE, (BitBoard(0x00000010), BitBoard(0x00002000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100))]

    board.turn = Color.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x00000800)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000400)) == [
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00020000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00004000)),
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000002)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040)),
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000100)) == [
        Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020))]

    # x p x p x _ x p
    # p x _ x _ x _ x
    # x _ x p x _ x p
    # P x _ x p x _ x
    # x _ x _ x _ x P
    # P x _ x _ x P x
    # x P x _ x _ x P
    # P x k x _ x _ x

    board.black = BitBoard(0xd8520004)
    board.white = BitBoard(0x00081998)
    board.pawns = BitBoard(0xd85a1998)

    board.turn = Color.WHITE
    assert board.attacking_moves_from_pos(BitBoard(0x00080000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00001000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000800)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000100)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000080)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000010)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == []

    assert board.not_attacking_moves_from_pos(BitBoard(0x00080000)) == [
        Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x00800000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00001000)) == [
        Move(Color.WHITE, (BitBoard(0x00001000), BitBoard(0x00010000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000800)) == [
        Move(Color.WHITE, (BitBoard(0x00000800), BitBoard(0x00008000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000100)) == [
        Move(Color.WHITE, (BitBoard(0x00000100), BitBoard(0x00002000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000400)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000010)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == []


    board.turn = Color.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x80000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x40000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x10000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x08000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00400000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00100000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00020000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == []

    assert board.not_attacking_moves_from_pos(BitBoard(0x80000000)) == [
        Move(Color.BLACK, (BitBoard(0x80000000), BitBoard(0x04000000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x40000000)) == [
        Move(Color.BLACK, (BitBoard(0x40000000), BitBoard(0x04000000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x40000000), BitBoard(0x02000000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x10000000)) == [
        Move(Color.BLACK, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x08000000)) == [
        Move(Color.BLACK, (BitBoard(0x08000000), BitBoard(0x00800000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00400000)) == [
        Move(Color.BLACK, (BitBoard(0x00400000), BitBoard(0x00040000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00100000)) == [
        Move(Color.BLACK, (BitBoard(0x00100000), BitBoard(0x00010000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00020000)) == [
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00002000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00020000), BitBoard(0x00004000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType())
    ]

    # x _ x _ x _ x p
    # _ x _ x _ x _ x
    # x _ x p x _ x p
    # _ x p x _ x P x
    # x _ x _ x p x _
    # P x _ x _ x _ x
    # x P x _ x _ x _
    # P x k x _ x _ x

    board.black = BitBoard(0x10542004)
    board.white = BitBoard(0x00010888)
    board.pawns = BitBoard(0x10552888)

    board.turn = Color.WHITE
    assert board.attacking_moves_from_pos(BitBoard(0x00010000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000800)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000080)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == []

    assert board.not_attacking_moves_from_pos(BitBoard(0x00010000)) == [
        Move(Color.WHITE, (BitBoard(0x00010000), BitBoard(0x00200000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000800)) == [
        Move(Color.WHITE, (BitBoard(0x00000800), BitBoard(0x00008000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000400)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == []

    board.turn = Color.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x10000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00400000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00100000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00040000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00002000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == []

    assert board.not_attacking_moves_from_pos(BitBoard(0x10000000)) == [
        Move(Color.BLACK, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00400000)) == [
        Move(Color.BLACK, (BitBoard(0x00400000), BitBoard(0x00020000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00100000)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00040000)) == [
        Move(Color.BLACK, (BitBoard(0x00040000), BitBoard(0x00004000)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00040000), BitBoard(0x00008000)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00002000)) == [
        Move(Color.BLACK, (BitBoard(0x00002000), BitBoard(0x00000200)), MoveType()),
        Move(Color.BLACK, (BitBoard(0x00002000), BitBoard(0x00000100)), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType())
    ]

def test_make_move():
    board = Board()
    board.white = BitBoard(0x000840f4)
    board.black = BitBoard(0x00808d00)
    board.pawns = BitBoard(0x0088c9f4)

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x _ x _ x _
    # P x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x P x _ x _ x

    assert board.turn == Color.WHITE

    board.make_move(Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00800000)))

    assert board.white == BitBoard(0x040040f4)
    assert board.black == BitBoard(0x00008d00)
    assert board.pawns == BitBoard(0x0400c9f4)
    assert board.turn == Color.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x P x _ x _ x

    board.make_move(Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080)))

    assert board.black == BitBoard(0x00008908)
    assert board.white == BitBoard(0x04004074)
    assert board.pawns == BitBoard(0x0400c974)
    assert board.turn == Color.WHITE


    board.turn = Color.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x _ x _ x p x
    # x _ x P x P x P
    # k x P x _ x _ x

    board.make_move(Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020)))

    assert board.black == BitBoard(0x0000880a)
    assert board.white == BitBoard(0x04004054)
    assert board.pawns == BitBoard(0x0400c854)
    assert board.turn == Color.WHITE

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x _ x _ x _ x
    # x _ x P x _ x P
    # k x P x k x _ x

    board.make_move(Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType(0x00), BitBoard(0x00000000)))

    assert board.black == BitBoard(0x0000880a)
    assert board.white == BitBoard(0x040040d0)
    assert board.pawns == BitBoard(0x0400c8d0)
    assert board.turn == Color.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x _ x _ x _ x
    # x P x P x _ x P
    # k x _ x k x _ x

    board.make_move(Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080)))

    assert board.black == BitBoard(0x00008c02)
    assert board.white == BitBoard(0x04004050)
    assert board.pawns == BitBoard(0x0400c850)
    assert board.turn == Color.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x _ x
    # x _ x P x _ x P
    # _ x _ x k x _ x

    board.make_move(Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00020000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00004000)))

    assert board.black == BitBoard(0x00028802)
    assert board.white == BitBoard(0x04000050)
    assert board.pawns == BitBoard(0x04008850)
    assert board.turn == Color.WHITE

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x k x _ x
    # x p x _ x _ x _
    # p x _ x _ x _ x
    # x _ x P x _ x P
    # _ x _ x k x _ x

    board.make_move(Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x80000000)), MoveType(0x01), BitBoard(0x00000000)))

    # x _ x K x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x k x _ x
    # x p x _ x _ x _
    # p x _ x _ x _ x
    # x _ x P x _ x P
    # _ x _ x k x _ x

    assert board.black == BitBoard(0x00028802)
    assert board.white == BitBoard(0x80000050)
    assert board.pawns == BitBoard(0x00008850)
    assert board.turn == Color.BLACK

    # take after promotion is prohibited

    # x _ x _ x _ x _
    # _ x p x p x _ x
    # x P x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x

    board.black = BitBoard(0x06000000)
    board.white = BitBoard(0x00800000)
    board.pawns = BitBoard(0x06800000)
    board.turn = Color.WHITE

    board.make_move(Move(Color.WHITE, (BitBoard(0x00800000), BitBoard(0x40000000)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x04000000)))

    # x _ x K x _ x _
    # _ x _ x p x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x

    assert board.black == BitBoard(0x02000000)
    assert board.white == BitBoard(0x40000000)
    assert board.pawns == BitBoard(0x02000000)
    assert board.turn == Color.BLACK

def test_undo_move():
    board = Board()
    board.black = BitBoard(0x00808d00)
    board.white = BitBoard(0x000840f4)
    board.pawns = BitBoard(0x0088c9f4)

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x _ x _ x _
    # P x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x P x _ x _ x

    assert board.turn == Color.WHITE

    board.make_move(Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00800000)))

    assert board.black == BitBoard(0x00008d00)
    assert board.white == BitBoard(0x040040f4)
    assert board.pawns == BitBoard(0x0400c9f4)
    assert board.turn == Color.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x P x _ x _ x

    board.undo_move(Move(Color.BLACK, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00800000)))

    assert board.black == BitBoard(0x00808d00)
    assert board.white == BitBoard(0x000840f4)
    assert board.pawns == BitBoard(0x0088c9f4)
    assert board.turn == Color.WHITE

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x _ x _ x _
    # P x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x P x _ x _ x
