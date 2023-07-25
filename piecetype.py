from enum import Enum


class PieceType(Enum):
    PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING, UNKNOWN = range(0, 7)