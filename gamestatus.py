from enum import Enum


class GameStatus(Enum):
    Active, BlackWin, WhiteWin, Forfeit, Stalemate, Resignation = range(0, 6)
    