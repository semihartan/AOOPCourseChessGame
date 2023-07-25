from enum import Flag


class MoveType(Flag):
    Move = 0x0
    Capture = 0x1
    Castling = 0x2
    Promotion = 0x4
    EnPassant = 0x8
