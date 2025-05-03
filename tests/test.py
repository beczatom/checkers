from checkers_sem.game.game import *
import copy

def test_not_attacking_moves():
    board = Board()
    board.white = BitBoard(0x0000000f)
    board.black = BitBoard(0x00000000)
    board.pawns = board.white | board.black
    # ________
    # ________
    # ________
    # ________
    # ________
    # ________
    # ________
    # P_P_P_P_

    assert (board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == [
        Move(Turn.WHITE, BitBoard(0x00000008), BitBoard(0x00000080), MoveType())])
    assert (board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Turn.WHITE, BitBoard(0x00000004), BitBoard(0x00000040), MoveType()),
        Move(Turn.WHITE, BitBoard(0x00000004), BitBoard(0x00000080), MoveType())])
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Turn.WHITE, BitBoard(0x00000002), BitBoard(0x00000020), MoveType()),
        Move(Turn.WHITE, BitBoard(0x00000002), BitBoard(0x00000040), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == [
        Move(Turn.WHITE, BitBoard(0x00000001), BitBoard(0x00000010), MoveType()),
        Move(Turn.WHITE, BitBoard(0x00000001), BitBoard(0x00000020), MoveType())]

    board.black = BitBoard(0x00000040)
    board.pawns = board.white | board.black
    # ________
    # ________
    # ________
    # ________
    # ________
    # ________
    # ___p____
    # P_P_P_P_

    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == [
        Move(Turn.WHITE, BitBoard(0x00000008), BitBoard(0x00000080), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Turn.WHITE, BitBoard(0x00000004), BitBoard(0x00000080), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Turn.WHITE, BitBoard(0x00000002), BitBoard(0x00000020), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == [
        Move(Turn.WHITE, BitBoard(0x00000001), BitBoard(0x00000010), MoveType()),
        Move(Turn.WHITE, BitBoard(0x00000001), BitBoard(0x00000020), MoveType())]

    board.white = BitBoard(0x0000008f)
    board.pawns = board.white | board.black
    # ________
    # ________
    # ________
    # ________
    # ________
    # ________
    # _P_p____
    # P_P_P_P_
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Turn.WHITE, BitBoard(0x00000002), BitBoard(0x00000020), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == [
        Move(Turn.WHITE, BitBoard(0x00000001), BitBoard(0x00000010), MoveType()),
        Move(Turn.WHITE, BitBoard(0x00000001), BitBoard(0x00000020), MoveType())]

    board.white = BitBoard(0x000000bf)
    board.black = BitBoard(0x00000240)
    board.pawns = board.white | board.black
    # ________
    # ________
    # ________
    # ________
    # ________
    # ____p___
    # _P_p_P_P
    # P_P_P_P_
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Turn.WHITE, BitBoard(0x00000080), BitBoard(0x00000800), MoveType()),
        Move(Turn.WHITE, BitBoard(0x00000080), BitBoard(0x00000400), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000020)) == [
        Move(Turn.WHITE, BitBoard(0x00000020), BitBoard(0x00000100), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000010)) == [
        Move(Turn.WHITE, BitBoard(0x00000010), BitBoard(0x00000100), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x10000000)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000040)) == []

    board.black = BitBoard(0xf1410240)
    board.white = BitBoard(0x040000bf)
    board.pawns = board.white | board.black
    # _p_p_p_p
    # __P___p_
    # ___p____
    # ______p_
    # ________
    # ____p___
    # _P_p_P_P
    # P_P_P_P_

    board.turn = Turn.BLACK

    assert board.not_attacking_moves_from_pos(BitBoard(0x80000000)) == [
        Move(Turn.BLACK, BitBoard(0x80000000), BitBoard(0x08000000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x40000000)) == [
        Move(Turn.BLACK, BitBoard(0x40000000), BitBoard(0x02000000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x20000000)) == [
        Move(Turn.BLACK, BitBoard(0x20000000), BitBoard(0x02000000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x10000000)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x01000000)) == [
        Move(Turn.BLACK, BitBoard(0x01000000), BitBoard(0x00100000), MoveType()),
        Move(Turn.BLACK, BitBoard(0x01000000), BitBoard(0x00200000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00400000)) == [
        Move(Turn.BLACK, BitBoard(0x00400000), BitBoard(0x00040000), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00400000), BitBoard(0x00020000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00010000)) == [
        Move(Turn.BLACK, BitBoard(0x00010000), BitBoard(0x00001000), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00010000), BitBoard(0x00002000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x04000000)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000800)) == []

    # x_______
    # _______x
    # x___x___
    # ___xkx_x
    # x_x_xPx_
    # _xPx_x_x
    # xKx_____
    # _x____kx
    board.black = BitBoard(0x00020001)
    board.white = BitBoard(0x00002480)
    board.pawns = BitBoard(0x00002400)

    assert board.not_attacking_moves_from_pos(BitBoard(0x00020000)) == [
        Move(Turn.BLACK, BitBoard(0x00020000), BitBoard(0x00200000), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00020000), BitBoard(0x00400000), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00020000), BitBoard(0x00004000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000001)) == [
        Move(Turn.BLACK, BitBoard(0x00000001), BitBoard(0x00000010), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00000001), BitBoard(0x00000020), MoveType())]

    board.turn = Turn.WHITE

    assert board.not_attacking_moves_from_pos(BitBoard(0x00002000)) == [
        Move(Turn.WHITE, BitBoard(0x00002000), BitBoard(0x00010000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000400)) == [
        Move(Turn.WHITE, BitBoard(0x00000400), BitBoard(0x00004000), MoveType()),
        Move(Turn.WHITE, BitBoard(0x00000400), BitBoard(0x00008000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Turn.WHITE, BitBoard(0x00000080), BitBoard(0x00000800), MoveType()),
        Move(Turn.WHITE, BitBoard(0x00000080), BitBoard(0x00000008), MoveType()),
        Move(Turn.WHITE, BitBoard(0x00000080), BitBoard(0x00000004), MoveType())]

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
        Move(Turn.WHITE, BitBoard(0x08000000), BitBoard(0x80000000), MoveType() | PROMOTION)]
    assert board.not_attacking_moves_from_pos(BitBoard(0x02000000)) == [
        Move(Turn.WHITE, BitBoard(0x02000000), BitBoard(0x20000000), MoveType() | PROMOTION)]
    assert board.not_attacking_moves_from_pos(BitBoard(0x01000000)) == [
        Move(Turn.WHITE, BitBoard(0x01000000), BitBoard(0x10000000), MoveType() | PROMOTION),
        Move(Turn.WHITE, BitBoard(0x01000000), BitBoard(0x20000000), MoveType() | PROMOTION)
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Turn.WHITE, BitBoard(0x00000002), BitBoard(0x00000020), MoveType())]

    board.turn = Turn.BLACK

    assert board.not_attacking_moves_from_pos(BitBoard(0x40000000)) == [
        Move(Turn.BLACK, BitBoard(0x40000000), BitBoard(0x04000000), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Turn.BLACK, BitBoard(0x00000080), BitBoard(0x00000800), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00000080), BitBoard(0x00000400), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00000080), BitBoard(0x00000008), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00000080), BitBoard(0x00000004), MoveType())]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000040)) == [
        Move(Turn.BLACK, BitBoard(0x00000040), BitBoard(0x00000004), MoveType() | PROMOTION)]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000010)) == [
        Move(Turn.BLACK, BitBoard(0x00000010), BitBoard(0x00000001), MoveType() | PROMOTION)]




def test_attacking_moves():
    board = Board()
    board.white = BitBoard(0x0000000f)
    board.black = BitBoard(0x00000000)
    board.pawns = board.white | board.black

    # ________
    # ________
    # ________
    # ________
    # ________
    # ________
    # ________
    # P_P_P_P_

    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000002)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000001)) == []

    board.black = BitBoard(0x00000040)
    board.pawns = board.white | board.black

    # ________
    # ________
    # ________
    # ________
    # ________
    # _ x _ x _ x _ x
    # x _ x p x _ x _
    # P x P x P x P x

    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Turn.WHITE, BitBoard(0x00000004), BitBoard(0x00000200), MoveType(0x06), BitBoard(0x00000040))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Turn.WHITE, BitBoard(0x00000002), BitBoard(0x00000400), MoveType(0x06), BitBoard(0x00000040))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000001)) == []

    board.black = BitBoard(0x000800d0)
    board.white = BitBoard(0x0000800f)
    board.pawns = BitBoard(0x0008805f)

    # ________
    # ________
    # ________
    # p x _ x _ x _ x
    # x P x _ x _ x _
    # _ x _ x _ x _ x
    # x k x p x _ x p
    # P x P x P x P x

    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == [
        Move(Turn.WHITE, BitBoard(0x00000008), BitBoard(0x00000400), MoveType(0x0a), BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Turn.WHITE, BitBoard(0x00000004), BitBoard(0x00000200), MoveType(0x06), BitBoard(0x00000040)),
        Move(Turn.WHITE, BitBoard(0x00000004), BitBoard(0x00000800), MoveType(0x0a), BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000002)) == [
        Move(Turn.WHITE, BitBoard(0x00000002), BitBoard(0x00000400), MoveType(0x06), BitBoard(0x00000040))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000001)) == []

    board.turn = Turn.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x00080000)) == [
        Move(Turn.BLACK, BitBoard(0x00080000), BitBoard(0x00000400), MoveType(0x06), BitBoard(0x00008000))]

    board.black = BitBoard(0x00000d00)
    board.white = BitBoard(0x000000f0)
    board.pawns = BitBoard(0x000009f0)

    # ________
    # ________
    # ________
    # _x_x_x_x
    # x_x_x_x_
    # pxkx_xpx
    # xPxPxPxP
    # _x_x_x_x

    board.turn = Turn.WHITE
    assert board.attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Turn.WHITE, BitBoard(0x00000080), BitBoard(0x00004000), MoveType(0x0a), BitBoard(0x00000400))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000040)) == [
        Move(Turn.WHITE, BitBoard(0x00000040), BitBoard(0x00008000), MoveType(0x0a), BitBoard(0x00000400))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000020)) == [
        Move(Turn.WHITE, BitBoard(0x00000020), BitBoard(0x00001000), MoveType(0x06), BitBoard(0x00000100))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000010)) == [
        Move(Turn.WHITE, BitBoard(0x00000010), BitBoard(0x00002000), MoveType(0x06), BitBoard(0x00000100))]

    board.turn = Turn.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x00000800)) == [
        Move(Turn.BLACK, BitBoard(0x00000800), BitBoard(0x00000004), MoveType(0x07), BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000400)) == [
        Move(Turn.BLACK, BitBoard(0x00000400), BitBoard(0x00000002), MoveType(0x06), BitBoard(0x00000040)),
        Move(Turn.BLACK, BitBoard(0x00000400), BitBoard(0x00000008), MoveType(0x06), BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000100)) == [
        Move(Turn.BLACK, BitBoard(0x00000100), BitBoard(0x00000002), MoveType(0x07), BitBoard(0x00000020))]

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

    board.turn = Turn.WHITE
    assert board.attacking_moves_from_pos(BitBoard(0x00800000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00080000)) == [
        Move(Turn.WHITE, BitBoard(0x00080000), BitBoard(0x04000000), MoveType(0x06), BitBoard(0x00800000))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000080)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000040)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000020)) == [
        Move(Turn.WHITE, BitBoard(0x00000020), BitBoard(0x00001000), MoveType(0x06), BitBoard(0x00000100))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000010)) == [
        Move(Turn.WHITE, BitBoard(0x00000010), BitBoard(0x00002000), MoveType(0x06), BitBoard(0x00000100))]

    board.turn = Turn.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x00000800)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000400)) == [
        Move(Turn.BLACK, BitBoard(0x00000400), BitBoard(0x00020000), MoveType(0x06), BitBoard(0x00004000)),
        Move(Turn.BLACK, BitBoard(0x00000400), BitBoard(0x00000002), MoveType(0x06), BitBoard(0x00000040)),
        Move(Turn.BLACK, BitBoard(0x00000400), BitBoard(0x00000008), MoveType(0x06), BitBoard(0x00000080))]
    assert board.attacking_moves_from_pos(BitBoard(0x00000100)) == [
        Move(Turn.BLACK, BitBoard(0x00000100), BitBoard(0x00000002), MoveType(0x07), BitBoard(0x00000020))]


    ##############################################SPEC##################################################################
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

    board.turn = Turn.WHITE
    assert board.attacking_moves_from_pos(BitBoard(0x00080000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00001000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000800)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000100)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000080)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000010)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == []

    assert board.not_attacking_moves_from_pos(BitBoard(0x00080000)) == [
        Move(Turn.WHITE, BitBoard(0x00080000), BitBoard(0x00800000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00001000)) == [
        Move(Turn.WHITE, BitBoard(0x00001000), BitBoard(0x00010000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000800)) == [
        Move(Turn.WHITE, BitBoard(0x00000800), BitBoard(0x00008000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000100)) == [
        Move(Turn.WHITE, BitBoard(0x00000100), BitBoard(0x00002000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Turn.WHITE, BitBoard(0x00000080), BitBoard(0x00000400), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000010)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == []


    board.turn = Turn.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x80000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x40000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x10000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x08000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00400000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00100000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00020000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == []

    assert board.not_attacking_moves_from_pos(BitBoard(0x80000000)) == [
        Move(Turn.BLACK, BitBoard(0x80000000), BitBoard(0x04000000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x40000000)) == [
        Move(Turn.BLACK, BitBoard(0x40000000), BitBoard(0x04000000), MoveType()),
        Move(Turn.BLACK, BitBoard(0x40000000), BitBoard(0x02000000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x10000000)) == [
        Move(Turn.BLACK, BitBoard(0x10000000), BitBoard(0x01000000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x08000000)) == [
        Move(Turn.BLACK, BitBoard(0x08000000), BitBoard(0x00800000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00400000)) == [
        Move(Turn.BLACK, BitBoard(0x00400000), BitBoard(0x00040000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00100000)) == [
        Move(Turn.BLACK, BitBoard(0x00100000), BitBoard(0x00010000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00020000)) == [
        Move(Turn.BLACK, BitBoard(0x00020000), BitBoard(0x00002000), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00020000), BitBoard(0x00004000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Turn.BLACK, BitBoard(0x00000004), BitBoard(0x00000040), MoveType())
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

    board.turn = Turn.WHITE
    assert board.attacking_moves_from_pos(BitBoard(0x00010000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000800)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000080)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000008)) == []

    assert board.not_attacking_moves_from_pos(BitBoard(0x00010000)) == [
        Move(Turn.WHITE, BitBoard(0x00010000), BitBoard(0x00200000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000800)) == [
        Move(Turn.WHITE, BitBoard(0x00000800), BitBoard(0x00008000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000080)) == [
        Move(Turn.WHITE, BitBoard(0x00000080), BitBoard(0x00000400), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000008)) == []

    board.turn = Turn.BLACK
    assert board.attacking_moves_from_pos(BitBoard(0x10000000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00400000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00100000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00040000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00002000)) == []
    assert board.attacking_moves_from_pos(BitBoard(0x00000004)) == []

    assert board.not_attacking_moves_from_pos(BitBoard(0x10000000)) == [
        Move(Turn.BLACK, BitBoard(0x10000000), BitBoard(0x01000000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00400000)) == [
        Move(Turn.BLACK, BitBoard(0x00400000), BitBoard(0x00020000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00100000)) == []
    assert board.not_attacking_moves_from_pos(BitBoard(0x00040000)) == [
        Move(Turn.BLACK, BitBoard(0x00040000), BitBoard(0x00004000), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00040000), BitBoard(0x00008000), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00002000)) == [
        Move(Turn.BLACK, BitBoard(0x00002000), BitBoard(0x00000200), MoveType()),
        Move(Turn.BLACK, BitBoard(0x00002000), BitBoard(0x00000100), MoveType())
    ]
    assert board.not_attacking_moves_from_pos(BitBoard(0x00000004)) == [
        Move(Turn.BLACK, BitBoard(0x00000004), BitBoard(0x00000040), MoveType())
    ]



def test_make_move():
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

    assert board.turn == Turn.WHITE

    board.make_move(Move(Turn.WHITE, BitBoard(0x00080000), BitBoard(0x04000000), MoveType(0x06), BitBoard(0x00800000)))

    assert board.black == BitBoard(0x00008d00)
    assert board.white == BitBoard(0x040040f4)
    assert board.pawns == BitBoard(0x0400c9f4)
    assert board.turn == Turn.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x P x _ x _ x

    board.make_move(Move(Turn.BLACK, BitBoard(0x00000400), BitBoard(0x00000008), MoveType(0x06), BitBoard(0x00000080)))

    assert board.black == BitBoard(0x00008908)
    assert board.white == BitBoard(0x04004074)
    assert board.pawns == BitBoard(0x0400c974)
    assert board.turn == Turn.WHITE


    board.turn = Turn.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x _ x _ x p x
    # x _ x P x P x P
    # k x P x _ x _ x

    board.make_move(Move(Turn.BLACK, BitBoard(0x00000100), BitBoard(0x00000002), MoveType(0x07), BitBoard(0x00000020)))

    assert board.black == BitBoard(0x0000880a)
    assert board.white == BitBoard(0x04004054)
    assert board.pawns == BitBoard(0x0400c854)
    assert board.turn == Turn.WHITE

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x _ x _ x _ x
    # x _ x P x _ x P
    # k x P x k x _ x

    board.make_move(Move(Turn.WHITE, BitBoard(0x00000004), BitBoard(0x00000080), MoveType(0x00), BitBoard(0x00000000)))

    assert board.black == BitBoard(0x0000880a)
    assert board.white == BitBoard(0x040040d0)
    assert board.pawns == BitBoard(0x0400c8d0)
    assert board.turn == Turn.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x _ x _ x _ x
    # x P x P x _ x P
    # k x _ x k x _ x

    board.make_move(Move(Turn.BLACK, BitBoard(0x00000008), BitBoard(0x00000400), MoveType(0x06), BitBoard(0x00000080)))

    assert board.black == BitBoard(0x00008c02)
    assert board.white == BitBoard(0x04004050)
    assert board.pawns == BitBoard(0x0400c850)
    assert board.turn == Turn.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x _ x
    # x _ x P x _ x P
    # _ x _ x k x _ x

    board.make_move(Move(Turn.BLACK, BitBoard(0x00000400), BitBoard(0x00020000), MoveType(0x06), BitBoard(0x00004000)))

    assert board.black == BitBoard(0x00028802)
    assert board.white == BitBoard(0x04000050)
    assert board.pawns == BitBoard(0x04008850)
    assert board.turn == Turn.WHITE

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x k x _ x
    # x p x _ x _ x _
    # p x _ x _ x _ x
    # x _ x P x _ x P
    # _ x _ x k x _ x

    board.make_move(Move(Turn.WHITE, BitBoard(0x04000000), BitBoard(0x80000000), MoveType(0x01), BitBoard(0x00000000)))

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
    assert board.turn == Turn.BLACK

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
    board.turn = Turn.WHITE

    board.make_move(Move(Turn.WHITE, BitBoard(0x00800000), BitBoard(0x40000000), MoveType(0x07), BitBoard(0x04000000)))

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
    assert board.turn == Turn.BLACK


def test_legal_moves():
    game = Game()

    while moves := game.get_moves():
        game_bef = copy.deepcopy(game)

        move = next(moves)

        game.push(move)
        game.pop()

        assert game_bef == game

        game.push(move)

        if game.get_result() is not None:
            break


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

    assert board.turn == Turn.WHITE

    board.make_move(Move(Turn.WHITE, BitBoard(0x00080000), BitBoard(0x04000000), MoveType(0x06), BitBoard(0x00800000)))

    assert board.black == BitBoard(0x00008d00)
    assert board.white == BitBoard(0x040040f4)
    assert board.pawns == BitBoard(0x0400c9f4)
    assert board.turn == Turn.BLACK

    # x _ x _ x _ x _
    # _ x P x _ x _ x
    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x P x _ x _ x

    board.undo_move(Move(Turn.BLACK, BitBoard(0x00080000), BitBoard(0x04000000), MoveType(0x06), BitBoard(0x00800000)))

    assert board.black == BitBoard(0x00808d00)
    assert board.white == BitBoard(0x000840f4)
    assert board.pawns == BitBoard(0x0088c9f4)
    assert board.turn == Turn.WHITE

    # x _ x _ x _ x _
    # _ x _ x _ x _ x
    # x p x _ x _ x _
    # P x _ x _ x _ x
    # x p x P x _ x _
    # p x k x _ x p x
    # x P x P x P x P
    # _ x P x _ x _ x
