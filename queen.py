import chesspiece
from piecetype import PieceType


class Queen(chesspiece.ChessPiece):

    def _name(self):
        return "Queen"

    def build_moves(self, move_layout):
        moves = []
        i, j = self.coordinates
        t_values = [-1, -1, 1, -1, -1, 1, 1, 1]
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

        for k in range(0, 8, 2):
            tx, ty = t_values[k], t_values[k + 1]
            for r in range(1, 7):
                mx, my = i + tx * r, j + ty * r
                if move_layout.add_move_by_coordinate((mx, my)):
                    break
        return moves

    @property
    def piece_type(self):
        return PieceType.QUEEN

    def can_move(self):
        i, j = self.coordinates
        t_values = [-1, -1, 1, -1, -1, 1, 1, 1]
        if self.__is_valid_move((i, j + 1), only_capture=False, can_capture=True):
            return True
        elif self.__is_valid_move((i, j - 1), only_capture=False, can_capture=True):
            return True
        elif self.__is_valid_move((i + 1, j), only_capture=False, can_capture=True):
            return True
        elif self.__is_valid_move((i - 1, j), only_capture=False, can_capture=True):
            return True
        for k in range(0, 8, 2):
            tx, ty = t_values[k], t_values[k + 1]
            for r in range(1, 7):
                mx, my = i + tx * r, j + ty * r
                if self.__is_valid_move((mx, my), only_capture=False, can_capture=True):
                    return True

            return False

    def clone(self):
        return Queen(self.is_white, self.coordinates)