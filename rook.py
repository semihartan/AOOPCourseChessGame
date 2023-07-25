import chesspiece
from piecetype import PieceType


class Rook(chesspiece.ChessPiece):

    def _name(self):
        return "Rook"

    def build_moves(self, move_layout):
        i, j = self.coordinates
        for k in range(j - 1, -1, -1):
            if move_layout.add_move_by_coordinate((i, k)):
                break
        for k in range(j + 1, 8):
            if move_layout.add_move_by_coordinate((i, k)):
                break
        for k in range(i - 1, -1, -1):
            if move_layout.add_move_by_coordinate((k, j)):
                break
        for k in range(i + 1, 8):
            if move_layout.add_move_by_coordinate((k, j)):
                break

    @property
    def piece_type(self):
        return PieceType.ROOK

    def can_move(self):
        i, j = self.coordinates
        if self.__is_valid_move((i, j + 1), only_capture=False, can_capture=True):
            return True
        elif self.__is_valid_move((i, j - 1), only_capture=False, can_capture=True):
            return True
        elif self.__is_valid_move((i + 1, j), only_capture=False, can_capture=True):
            return True
        elif self.__is_valid_move((i-1, j), only_capture=False, can_capture=True):
            return True

        return False

    def clone(self):
        return Rook(self.is_white, self.coordinates)