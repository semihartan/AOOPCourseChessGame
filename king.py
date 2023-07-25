import chesspiece
from piecetype import PieceType


class King(chesspiece.ChessPiece):

    def _name(self):
        return "King"

    def build_moves(self, move_layout):
        i, j = self.coordinates
        t_values = [-1, -1, 0, -1, 1, -1,
                    -1, 0, 1, 0,
                    -1, 1, 0, 1, 1, 1]
        for k in range(0, 16, 2):
            tx, ty = t_values[k], t_values[k + 1]
            mx, my = i + tx, j + ty
            move_layout.add_move_by_coordinate((mx, my))

    @property
    def piece_type(self):
        return PieceType.KING

    def can_move(self):
        i, j = self.coordinates
        t_values = [-1, -1, 0, -1, 1, -1,
                    -1, 0, 1, 0,
                    -1, 1, 0, 1, 1, 1]
        for k in range(0, 16, 2):
            tx, ty = t_values[k], t_values[k + 1]
            mx, my = i + tx, j + ty
            if self.__is_valid_move((mx, my), only_capture=False, can_capture=True):
                return True

        return False

    def clone(self):
        king = King(self.is_white, self.coordinates)
        king.game_controller = self.game_controller
        king.chess_board = self.chess_board
        return king