import chesspiece
from piecetype import PieceType


class Bishop(chesspiece.ChessPiece):

    def _name(self):
        return "Bishop"

    def build_moves(self, move_layout):
        moves = []
        i, j = self.coordinates
        t_values = [-1, -1, 1, -1, -1, 1, 1, 1]
        for k in range(0, 8, 2):
            tx, ty = t_values[k], t_values[k + 1]
            for r in range(1, 7):
                mx, my = i + tx * r, j + ty * r
                if move_layout.add_move_by_coordinate((mx, my)):
                    break

        return moves

    def can_move(self):
        i, j = self.coordinates
        t_values = [-1, -1, 1, -1, -1, 1, 1, 1]
        for k in range(0, 8, 2):
            tx, ty = t_values[k], t_values[k + 1]
            for r in range(1, 7):
                mx, my = i + tx * r, j + ty * r
                if self.__is_valid_move((mx, my), only_capture=False, can_capture=True):
                    return True

        return False

    @property
    def piece_type(self):
        return PieceType.BISHOP

    def clone(self):
        bishop = Bishop(self.is_white, self.coordinates)
        bishop.game_controller = self.game_controller
        bishop.chess_board = self.chess_board
        return bishop