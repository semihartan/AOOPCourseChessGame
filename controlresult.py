from enum import Enum


class ControlResult(Enum):
    CHECK, CHECKMATE, STALEMATE, UNKNOWN = range(0, 4)
