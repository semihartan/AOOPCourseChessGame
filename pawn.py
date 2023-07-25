import chesspiece
from piecetype import PieceType


class Pawn(chesspiece.ChessPiece):

    def __init__(self, is_white, coordinates):
        super().__init__(is_white, coordinates)
        self.has_moved_only_two = False

    def _name(self):
        return "Pawn"

    def build_moves(self, move_layout):
        i, j = self.coordinates
        t = self._translation_vector

        stop = move_layout.add_move_by_coordinate((i, j + t * 1), can_capture=False)
        move_layout.add_move_by_coordinate((i - 1, j + t * 1), only_capture=True)
        move_layout.add_move_by_coordinate((i + 1, j + t * 1), only_capture=True)
        if not stop and self.__is_at_initial_position:
            move_layout.add_move_by_coordinate((i, j + t * 2), can_capture=False)
            return

    @property
    def piece_type(self):
        return PieceType.PAWN

    def can_move(self):

        chessboard = super().chess_board
        i, j = self.coordinates
        t = self._translation_vector
        if self.__is_valid_move((i, j + t * 1), only_capture=False, can_capture=False):
            return True
        elif self.__is_valid_move((i - 1, j + t * 1), only_capture=True, can_capture=True):
            return True
        elif self.__is_valid_move((i + 1, j + t * 1), only_capture=True, can_capture=True):
            return True

        if self.__is_at_initial_position:
            if self.__is_valid_move((i, j + t * 2), only_capture=True, can_capture=True):
                return True
        return False

    @property
    def __is_at_initial_position(self):
        i, j = self.coordinates
        if (self.is_white and j == 6) or (not self.is_white and j == 1):
            return True
        return False

    def clone(self):
        pawn = Pawn(self.is_white, self.coordinates)
        pawn.game_controller = self.game_controller
        pawn.chess_board = self.chess_board
        return pawn