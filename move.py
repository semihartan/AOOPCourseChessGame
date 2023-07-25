from chesssettings import ChessSettings
from movetype import MoveType
from piecetype import PieceType


class Move:

    def __init__(self, move_layout, move_type, coordinates):
        self.__coordinates = coordinates
        self.__move_type = move_type
        self.castling_rook = None
        self.en_passant_coord = None
        self.move_layout = move_layout

    @property
    def move_type(self):
        return self.__move_type

    @move_type.setter
    def move_type(self, value):
        self.__move_type = value

    @property
    def coordinates(self):
        return self.__coordinates

    def execute(self):
        chessboard = self.move_layout.chess_board
        owner = self.move_layout.owner
        if self.move_type == MoveType.Move:
            owner.move(self.coordinates)
        elif self.move_type & MoveType.Capture == MoveType.Capture:
            if self.move_type & MoveType.EnPassant == MoveType.EnPassant:
                self.move_layout.captured_piece = chessboard.get_chessboard_state().get_piece(self.en_passant_coord)
            else:
                self.move_layout.captured_piece = chessboard.get_chessboard_state().get_piece(self.coordinates)

            owner.move(self.coordinates)
        elif self.move_type == MoveType.Castling:
            owner.move(self.coordinates)
            if self.coordinates[0] < self.castling_rook.coordinates[0]:
                self.castling_rook.move((self.coordinates[0] - 1, self.coordinates[1]))
            else:
                self.castling_rook.move((self.coordinates[0] + 1, self.coordinates[1]))
        elif self.move_type & MoveType.Promotion == MoveType.Promotion:
            self.move_type = self.move_type & ~MoveType.Promotion

    @staticmethod
    def is_valid_coords(coords):
        return 0 <= coords[0] <= 7 and 0 <= coords[1] <= 7
