import pytest
from checkers_sem.game.move import Move
from checkers_sem.constants import TAKE, PROMOTION, BitBoard, MoveType, Color, Piece


tested_moves = [
    Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(),                                 BitBoard(0x00000000)),
    Move(Color.WHITE, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(),                                 BitBoard(0x00000000)),
    Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000200)), MoveType() | TAKE | Piece.KING,             BitBoard(0x00000040)),
    Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000200)), MoveType() | TAKE | Piece.PAWN,             BitBoard(0x00000040)),
    Move(Color.BLACK, (BitBoard(0x08000000), BitBoard(0x80000000)), MoveType(),                                 BitBoard(0x00000000)),
    Move(Color.WHITE, (BitBoard(0x08000000), BitBoard(0x80000000)), MoveType() | PROMOTION,                     BitBoard(0x00000000)),
    Move(Color.BLACK, (BitBoard(0x00000020), BitBoard(0x00000002)), MoveType() | PROMOTION,                     BitBoard(0x00000000)),
    Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00000002)), MoveType(),                                 BitBoard(0x00000000)),
    Move(Color.BLACK, (BitBoard(0x00800000), BitBoard(0x40000000)), MoveType() | TAKE | Piece.PAWN,             BitBoard(0x04000000)),
    Move(Color.WHITE, (BitBoard(0x00800000), BitBoard(0x40000000)), MoveType() | PROMOTION | TAKE | Piece.KING, BitBoard(0x04000000)),
]

@pytest.mark.parametrize('move, true_val', [
    (tested_moves[i], true_val) for i, true_val in enumerate([False, False, True, True, False, False, False, False, True, True])
])
def test_is_taking(move : Move, true_val : bool):
    assert bool(move.is_taking()) == true_val

@pytest.mark.parametrize('move, true_val', [
    (tested_moves[i], true_val) for i, true_val in enumerate([False, False, False, False, False, True, True, False, False, True])
])
def test_is_promoting(move : Move, true_val : bool):
    assert bool(move.is_promoting()) == true_val

@pytest.mark.parametrize('move', tested_moves)
def test_revert(move : Move):
    reverted = move.revert()

    assert reverted.turn == move.turn
    assert reverted.from_mask == move.to_mask
    assert reverted.to_mask == move.from_mask
    assert reverted.move_type == move.move_type
    assert reverted.took_mask == move.took_mask
