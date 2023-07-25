from chesspiece import *


class Knight(ChessPiece):

    def _name(self):
        return "Knight"

    def build_moves(self, move_layout):
        i, j = self.coordinates
        t_values = [-2, -1, -1, -2, 1, -2, 2, -1, -2, 1, -1, 2, 1, 2, 2, 1]
        for k in range(0, 16, 2):
            tx, ty = t_values[k], t_values[k + 1]
            mx, my = i + tx, j + ty
            move_layout.add_move_by_coordinate((mx, my))

    def can_move(self):
        i, j = self.coordinates
        t_values = [-2, -1, -1, -2, 1, -2, 2, -1, -2, 1, -1, 2, 1, 2, 2, 1]
        for k in range(0, 16, 2):
            tx, ty = t_values[k], t_values[k + 1]
            mx, my = i + tx, j + ty
            if self.__is_valid_move((mx, my), only_capture=False, can_capture=True):
                return True

        return False

    @property
    def piece_type(self):
        return PieceType.KNIGHT

    def clone(self):
        knight = Knight(self.is_white, self.coordinates)
        knight.game_controller = self.game_controller
        knight.chess_board = self.chess_board
        return knight

