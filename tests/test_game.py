from checkers_sem.game.game import Game, three_fold_repetition
import copy

import pytest
from collections import deque

from checkers_sem.game.board import Board
from checkers_sem.game.move import Move
from checkers_sem.game.constants import BitBoard, TAKE, GameEnd, MoveType, Color, Piece, PROMOTION

@pytest.mark.parametrize('move_stack, repetition', [
    (deque([]), False),
    (deque([
        (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 0),
        (Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)), 1),
        (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 2),
        (Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType(), BitBoard(0x00000000)), 3),
        (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 4),
        (Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)), 5),
     ]), True),
    (deque([
        (Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType(), BitBoard(0x00000000)), 0),
        (Move(Color.BLACK, (BitBoard(0x08000000), BitBoard(0x00800000)), MoveType(), BitBoard(0x00000000)), 1),
        (Move(Color.WHITE, (BitBoard(0x00000800), BitBoard(0x00008000)), MoveType(), BitBoard(0x00000000)), 2),
        (Move(Color.BLACK, (BitBoard(0x00800000), BitBoard(0x00040000)), MoveType(), BitBoard(0x00000000)), 3),
        (Move(Color.WHITE, (BitBoard(0x00008000), BitBoard(0x00400000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00040000)), 0),
        (Move(Color.BLACK, (BitBoard(0x04000000), BitBoard(0x00020000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00400000)), 0),
     ]), False),
    (deque([
        (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(), BitBoard(0x00000000)), 0),
        (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 1),
        (Move(Color.BLACK, (BitBoard(0x00000040), BitBoard(0x00000004)), MoveType(), BitBoard(0x00000000)), 2),
        (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 3),
        (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 4),
        (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)), 5),
    ]), False),
])
def test_three_fold_repetition(move_stack : deque[tuple[Move, int]], repetition : bool):
    assert three_fold_repetition(move_stack) == repetition

moves_and_ref_list = [
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        [Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00800000))],
        (BitBoard(0x040040f4), BitBoard(0x00008d00), BitBoard(0x0400c9f4)),
        0
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        [
            Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080)),
            Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00800000))
        ],
        (BitBoard(0x04004074), BitBoard(0x00008908), BitBoard(0x0400c974)),
        0
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        [
            Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN,
                 BitBoard(0x00000080)),
            Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN,
                 BitBoard(0x00800000)),
            Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020))
        ],
        (BitBoard(0x04004054), BitBoard(0x0000880a), BitBoard(0x0400c854)),
        0
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        [
            Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN,
                 BitBoard(0x00000080)),
            Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN,
                 BitBoard(0x00800000)),
            Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)),
                 MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020)),
            Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)),
        ],
        (BitBoard(0x040040d0), BitBoard(0x0000880a), BitBoard(0x0400c8d0)),
        1
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        [
            Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN,
                 BitBoard(0x00000080)),
            Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN,
                 BitBoard(0x00800000)),
            Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)),
                 MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020)),
            Move(Color.WHITE, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)),
            Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000400)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080)),
            Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00020000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00004000)),
        ],
        (BitBoard(0x04000050), BitBoard(0x00028802), BitBoard(0x04008850)),
        0
    ),
    (
        (BitBoard(0x04000050), BitBoard(0x00028802), BitBoard(0x04008850)),
        [Move(Color.WHITE, (BitBoard(0x04000000), BitBoard(0x80000000)), MoveType(0x01), BitBoard(0x00000000))],
        (BitBoard(0x80000050), BitBoard(0x00028802), BitBoard(0x00008850)),
        1
    ),
    (
        (BitBoard(0x00800000), BitBoard(0x06000000), BitBoard(0x06800000)),
        [Move(Color.WHITE, (BitBoard(0x00800000), BitBoard(0x40000000)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x04000000))],
        (BitBoard(0x40000000), BitBoard(0x02000000), BitBoard(0x02000000)),
        0
    ),
]

@pytest.mark.parametrize('board_init, moves, board_fin, last_take', moves_and_ref_list)
def test_push(board_init : tuple[BitBoard, BitBoard, BitBoard], moves : list[Move], board_fin : tuple[BitBoard, BitBoard, BitBoard], last_take : int):
    board = Board()
    board.white = board_init[0]
    board.black = board_init[1]
    board.pawns = board_init[2]
    board.turn = moves[0].turn

    game = Game()
    game.board = board
    game.turn = moves[0].turn

    for move in moves:
        game.push(move)

    assert game.board.white == board_fin[0]
    assert game.board.black == board_fin[1]
    assert game.board.pawns == board_fin[2]
    assert len(game.moves_stack) == len(moves)
    assert game.moves_stack[-1][1] == last_take

@pytest.mark.parametrize('board_init, moves, board_fin, last_take', moves_and_ref_list)
def test_pop(board_init : tuple[BitBoard, BitBoard, BitBoard], moves : list[Move], board_fin : tuple[BitBoard, BitBoard, BitBoard], last_take : int):
    board = Board()
    board.white = board_init[0]
    board.black = board_init[1]
    board.pawns = board_init[2]
    board.turn = moves[0].turn

    game = Game()
    game.board = board
    game.turn = moves[0].turn

    for move in moves:
        game_before = copy.deepcopy(game)
        game.push(move)
        game.pop()
        assert game_before == game
        game.push(move)

    assert game.board.white == board_fin[0]
    assert game.board.black == board_fin[1]
    assert game.board.pawns == board_fin[2]
    assert len(game.moves_stack) == len(moves)
    assert game.moves_stack[-1][1] == last_take

@pytest.mark.parametrize('board_init, moves, board_fin, last_take', moves_and_ref_list)
def test_push_from_popped(board_init : tuple[BitBoard, BitBoard, BitBoard], moves : list[Move], board_fin : tuple[BitBoard, BitBoard, BitBoard], last_take : int):
    board = Board()
    board.white = board_init[0]
    board.black = board_init[1]
    board.pawns = board_init[2]
    board.turn = moves[0].turn

    game = Game()
    game.board = board
    game.turn = moves[0].turn

    for move in moves:
        game.push(move)
        game_before = copy.deepcopy(game)
        game.pop()
        game.push_from_popped()
        assert game_before == game


    assert game.board.white == board_fin[0]
    assert game.board.black == board_fin[1]
    assert game.board.pawns == board_fin[2]
    assert len(game.moves_stack) == len(moves)
    assert game.moves_stack[-1][1] == last_take

@pytest.mark.parametrize('board_init, moves, board_fin, last_take', moves_and_ref_list)
def test_peek(board_init : tuple[BitBoard, BitBoard, BitBoard], moves : list[Move], board_fin : tuple[BitBoard, BitBoard, BitBoard], last_take : int):
    board = Board()
    board.white = board_init[0]
    board.black = board_init[1]
    board.pawns = board_init[2]
    board.turn = moves[0].turn

    game = Game()
    game.board = board
    game.turn = moves[0].turn

    for move in moves:
        game.push(move)
        assert game.peek() == move

    assert game.board.white == board_fin[0]
    assert game.board.black == board_fin[1]
    assert game.board.pawns == board_fin[2]
    assert len(game.moves_stack) == len(moves)
    assert game.moves_stack[-1][1] == last_take

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
def test_get_moves(init_board_tuple : tuple[BitBoard, BitBoard, BitBoard], white_ref_set : set[Move], black_ref_set : set[Move]):
    board = Board()
    board.white = init_board_tuple[0]
    board.black = init_board_tuple[1]
    board.pawns = init_board_tuple[2]

    game = Game()
    game.board = board

    moves = set()
    for move in game.get_moves():
        moves.add(move)

    assert moves == white_ref_set

    board.turn = Color.BLACK

    moves = set()
    for move in game.get_moves():
        moves.add(move)

    assert moves == black_ref_set

@pytest.mark.parametrize('init_board, white_ref_positions, black_ref_positions',[
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        {BitBoard(0x00000080), BitBoard(0x00000040), BitBoard(0x00000020), BitBoard(0x00000010)},
        {BitBoard(0x08000000), BitBoard(0x04000000), BitBoard(0x02000000), BitBoard(0x01000000)}
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        {BitBoard(0x00080000), BitBoard(0x00000020), BitBoard(0x00000010)},
        {BitBoard(0x00000400), BitBoard(0x00000100)}
    ),

])
def test_get_moves_from_mask(init_board : tuple[BitBoard, BitBoard, BitBoard], white_ref_positions : set[BitBoard], black_ref_positions : set[BitBoard]):
    board = Board()
    board.white = init_board[0]
    board.black = init_board[1]
    board.pawns = init_board[2]

    game = Game()
    game.board = board

    moves = set(game.get_moves_from_mask())

    assert moves == white_ref_positions

    board.turn = Color.BLACK

    moves = set(game.get_moves_from_mask())

    assert moves == black_ref_positions

@pytest.mark.parametrize('init_board, turn, from_mask, ref_to_masks',[
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        True,
        BitBoard(0x00000080),
        {BitBoard(0x00000800), BitBoard(0x00000400)}
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        True,
        BitBoard(0x00000040),
        {BitBoard(0x00000400), BitBoard(0x00000200)}
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        True,
        BitBoard(0x00000020),
        {BitBoard(0x00000200), BitBoard(0x00000100)}
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        True,
        BitBoard(0x00000010),
        {BitBoard(0x00000100)}
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        False,
        BitBoard(0x08000000),
        {BitBoard(0x00800000)}
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        False,
        BitBoard(0x04000000),
        {BitBoard(0x00800000), BitBoard(0x00400000)}
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        False,
        BitBoard(0x02000000),
        {BitBoard(0x00400000), BitBoard(0x00200000)}
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        False,
        BitBoard(0x01000000),
        {BitBoard(0x00200000), BitBoard(0x00100000)}
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        True,
        BitBoard(0x00080000),
        {BitBoard(0x04000000)}
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        True,
        BitBoard(0x00000020),
        {BitBoard(0x00001000)}
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        True,
        BitBoard(0x00000010),
        {BitBoard(0x00002000)}
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        False,
        BitBoard(0x00000400),
        {BitBoard(0x00020000), BitBoard(0x00000002), BitBoard(0x00000008)}
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        False,
        BitBoard(0x00000100),
        {BitBoard(0x00000002)}
    ),
])
def test_get_moves_to_mask(init_board : tuple[BitBoard, BitBoard, BitBoard], turn : bool, from_mask : BitBoard, ref_to_masks : set[BitBoard]):
    board = Board()
    board.white = init_board[0]
    board.black = init_board[1]
    board.pawns = init_board[2]
    board.turn = turn

    game = Game()
    game.board = board
    game.turn = turn

    moves = set(game.get_moves_to_mask(from_mask))

    assert moves == ref_to_masks

@pytest.mark.parametrize('init_board, from_mask, to_mask, ref_move', [
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x00000080),
        BitBoard(0x00000800),
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000800)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x00000080),
        BitBoard(0x00000400),
        Move(Color.WHITE, (BitBoard(0x00000080), BitBoard(0x00000400)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x00000040),
        BitBoard(0x00000400),
        Move(Color.WHITE, (BitBoard(0x00000040), BitBoard(0x00000400)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x00000040),
        BitBoard(0x00000200),
        Move(Color.WHITE, (BitBoard(0x00000040), BitBoard(0x00000200)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x00000020),
        BitBoard(0x00000200),
        Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00000200)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x00000020),
        BitBoard(0x00000100),
        Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00000100)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x00000010),
        BitBoard(0x00000100),
        Move(Color.WHITE, (BitBoard(0x00000010), BitBoard(0x00000100)), MoveType(), BitBoard(0x00000000))
    ),

    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x08000000),
        BitBoard(0x00800000),
        Move(Color.BLACK, (BitBoard(0x08000000), BitBoard(0x00800000)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x04000000),
        BitBoard(0x00800000),
        Move(Color.BLACK, (BitBoard(0x04000000), BitBoard(0x00800000)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x04000000),
        BitBoard(0x00400000),
        Move(Color.BLACK, (BitBoard(0x04000000), BitBoard(0x00400000)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x02000000),
        BitBoard(0x00200000),
        Move(Color.BLACK, (BitBoard(0x02000000), BitBoard(0x00200000)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x02000000),
        BitBoard(0x00400000),
        Move(Color.BLACK, (BitBoard(0x02000000), BitBoard(0x00400000)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x01000000),
        BitBoard(0x00200000),
        Move(Color.BLACK, (BitBoard(0x01000000), BitBoard(0x00200000)), MoveType(), BitBoard(0x00000000))
    ),
    (
        (BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)),
        BitBoard(0x01000000),
        BitBoard(0x00100000),
        Move(Color.BLACK, (BitBoard(0x01000000), BitBoard(0x00100000)), MoveType(), BitBoard(0x00000000))
    ),

    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        BitBoard(0x00080000),
        BitBoard(0x04000000),
        Move(Color.WHITE, (BitBoard(0x00080000), BitBoard(0x04000000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00800000)),
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        BitBoard(0x00000020),
        BitBoard(0x00001000),
        Move(Color.WHITE, (BitBoard(0x00000020), BitBoard(0x00001000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100)),
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        BitBoard(0x00000010),
        BitBoard(0x00002000),
        Move(Color.WHITE, (BitBoard(0x00000010), BitBoard(0x00002000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000100))
    ),

    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        BitBoard(0x00000400),
        BitBoard(0x00020000),
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00020000)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00004000))
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        BitBoard(0x00000400),
        BitBoard(0x00000002),
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000002)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000040)),
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        BitBoard(0x00000400),
        BitBoard(0x00000008),
        Move(Color.BLACK, (BitBoard(0x00000400), BitBoard(0x00000008)), MoveType() | TAKE | Piece.PAWN, BitBoard(0x00000080)),
    ),
    (
        (BitBoard(0x000840f4), BitBoard(0x00808d00), BitBoard(0x0088c9f4)),
        BitBoard(0x00000100),
        BitBoard(0x00000002),
        Move(Color.BLACK, (BitBoard(0x00000100), BitBoard(0x00000002)), MoveType() | PROMOTION | TAKE | Piece.PAWN, BitBoard(0x00000020))
    )
])
def test_get_move_from_to(init_board : tuple[BitBoard, BitBoard, BitBoard], from_mask : BitBoard, to_mask : BitBoard, ref_move : Move):
    board = Board()
    board.white = init_board[0]
    board.black = init_board[1]
    board.pawns = init_board[2]
    board.turn = ref_move.turn

    game = Game()
    game.board = board
    game.turn = ref_move.turn

    assert game.get_move_from_to(from_mask, to_mask) == ref_move

@pytest.mark.parametrize('init_board, turn, move_stack, ref_res',
[
    ((BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)), Color.WHITE, deque([]), None),
    ((BitBoard(0x000000ff), BitBoard(0x00000000), BitBoard(0x000000ff)), Color.WHITE, deque([]), 1),

    (
        (BitBoard(0x10000000), BitBoard(0x00000008), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 0),
            (Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)), 1),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 2),
            (Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType(), BitBoard(0x00000000)), 3),
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 4),
            (Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)), 5),
        ]),
        0
    ),
    (
        (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 0),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(), BitBoard(0x00000000)), 1),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 2),
            (Move(Color.BLACK, (BitBoard(0x00000040), BitBoard(0x00000004)), MoveType(), BitBoard(0x00000000)), 3),
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 4),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)), 5),
        ]),
        None
    ),

    (
        (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 50),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(), BitBoard(0x00000000)), 51),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 52)
        ]),
        0
    ),
    (
        (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 30),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(), BitBoard(0x00000000)), 31),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 32)
        ]),
        0
    ),
    (
        (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 20),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(), BitBoard(0x00000000)), 21),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 22)
        ]),
        None
    ),
])
def test_get_result_train(init_board : tuple[BitBoard, BitBoard, BitBoard], turn : bool, move_stack : deque[tuple[Move, int]], ref_res : int):
    board = Board()
    board.white = init_board[0]
    board.black = init_board[1]
    board.pawns = init_board[2]
    board.turn = turn

    game = Game()
    game.board = board
    game.moves_stack = move_stack
    game.turn = turn

    if len(move_stack):
        game.last_take = game.moves_stack[-1][1]

    if ref_res is None:
        assert game.get_result_train() is None

    else:
        assert game.get_result_train() == ref_res

@pytest.mark.parametrize('init_board, turn, move_stack, ref_res',
[
    ((BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)), Color.WHITE, deque([]), None),
    ((BitBoard(0x000000ff), BitBoard(0x00000000), BitBoard(0x000000ff)), Color.WHITE, deque([]), 1),

    (
        (BitBoard(0x10000000), BitBoard(0x00000008), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 0),
            (Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)), 1),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 2),
            (Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType(), BitBoard(0x00000000)), 3),
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 4),
            (Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)), 5),
        ]),
        0
    ),
    (
        (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 0),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(), BitBoard(0x00000000)), 1),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 2),
            (Move(Color.BLACK, (BitBoard(0x00000040), BitBoard(0x00000004)), MoveType(), BitBoard(0x00000000)), 3),
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 4),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType(), BitBoard(0x00000000)), 5),
        ]),
        None
    ),

    (
        (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 50),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(), BitBoard(0x00000000)), 51),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 52)
        ]),
        0
    ),
    (
        (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 30),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(), BitBoard(0x00000000)), 31),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 32)
        ]),
        None
    ),
    (
        (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
            (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(), BitBoard(0x00000000)), 20),
            (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(), BitBoard(0x00000000)), 21),
            (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(), BitBoard(0x00000000)), 22)
        ]),
        None
    ),
])
def test_get_result(init_board : tuple[BitBoard, BitBoard, BitBoard], turn : bool, move_stack : deque[tuple[Move, int]], ref_res : int):
    board = Board()
    board.white = init_board[0]
    board.black = init_board[1]
    board.pawns = init_board[2]
    board.turn = turn

    game = Game()
    game.board = board
    game.moves_stack = move_stack
    game.turn = turn

    if len(move_stack):
        game.last_take = game.moves_stack[-1][1]

    if ref_res is None:
        assert game.get_result() is None

    else:
        assert game.get_result() == ref_res

@pytest.mark.parametrize('init_board, turn, move_stack, game_end',
[
    ((BitBoard(0x000000ff), BitBoard(0xff000000), BitBoard(0xff0000ff)), Color.WHITE, deque([]), None),
    ((BitBoard(0x000000ff), BitBoard(0x00000000), BitBoard(0x000000ff)), Color.WHITE, deque([]), GameEnd.NO_FIGURES),

    (
        (BitBoard(0x10000000), BitBoard(0x00000008), BitBoard(0x00000000)),
        Color.WHITE,
        deque([
             (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(),
                   BitBoard(0x00000000)), 0),
             (Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(),
                   BitBoard(0x00000000)), 1),
             (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(),
                   BitBoard(0x00000000)), 2),
             (Move(Color.BLACK, (BitBoard(0x00000080), BitBoard(0x00000008)), MoveType(),
                   BitBoard(0x00000000)), 3),
             (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(),
                   BitBoard(0x00000000)), 4),
             (Move(Color.BLACK, (BitBoard(0x00000008), BitBoard(0x00000080)), MoveType(),
                   BitBoard(0x00000000)), 5),
        ]),
        GameEnd.THREEFOLD_REPETITION
    ),
    (
         (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
         Color.WHITE,
         deque([
             (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(),
                   BitBoard(0x00000000)), 0),
             (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(),
                   BitBoard(0x00000000)), 1),
             (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(),
                   BitBoard(0x00000000)), 2),
             (Move(Color.BLACK, (BitBoard(0x00000040), BitBoard(0x00000004)), MoveType(),
                   BitBoard(0x00000000)), 3),
             (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(),
                   BitBoard(0x00000000)), 4),
             (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000080)), MoveType(),
                   BitBoard(0x00000000)), 5),
         ]),
         None
    ),

    (
         (BitBoard(0x10000000), BitBoard(0x00000004), BitBoard(0x00000000)),
         Color.WHITE,
         deque([
             (Move(Color.WHITE, (BitBoard(0x10000000), BitBoard(0x01000000)), MoveType(),
                   BitBoard(0x00000000)), 50),
             (Move(Color.BLACK, (BitBoard(0x00000004), BitBoard(0x00000040)), MoveType(),
                   BitBoard(0x00000000)), 51),
             (Move(Color.WHITE, (BitBoard(0x01000000), BitBoard(0x10000000)), MoveType(),
                   BitBoard(0x00000000)), 52)
         ]),
         GameEnd.FIFTY_MOVES_WITHOUT_TAKE
    ),
])
def test_get_end_type(init_board : tuple[BitBoard, BitBoard, BitBoard], turn : bool, move_stack : deque[tuple[Move, int]], game_end : GameEnd):
    board = Board()
    board.white = init_board[0]
    board.black = init_board[1]
    board.pawns = init_board[2]
    board.turn = turn

    game = Game()
    game.board = board
    game.moves_stack = move_stack
    game.turn = turn
    if len(move_stack):
        game.last_take = game.moves_stack[-1][1]

    if game_end is None:
        assert game.get_end_type() is None

    else:
        assert game.get_end_type() == game_end

@pytest.mark.parametrize('board_init, moves, board_fin, last_take', moves_and_ref_list)
def test_get_move_history(board_init : tuple[BitBoard, BitBoard, BitBoard], moves : list[Move], board_fin : tuple[BitBoard, BitBoard, BitBoard], last_take : int):
    board = Board()
    board.white = board_init[0]
    board.black = board_init[1]
    board.pawns = board_init[2]
    board.turn = moves[0].turn

    game = Game()
    game.board = board
    game.turn = moves[0].turn

    for move in moves:
        game.push(move)

    assert game.board.white == board_fin[0]
    assert game.board.black == board_fin[1]
    assert game.board.pawns == board_fin[2]
    assert len(game.moves_stack) == len(moves)
    assert game.moves_stack[-1][1] == last_take
    assert game.get_move_history() == moves
