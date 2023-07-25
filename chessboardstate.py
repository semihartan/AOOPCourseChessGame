from piecetype import PieceType


class ChessBoardState:
    def __init__(self):
        self.__pieces = list()
        self.__iterator_position = 0

    def add_piece(self, piece):
        self.__pieces.append(piece)

    @property
    def pieces(self):
        return self.__pieces

    def get_white_king(self):
        return self.__get_king(True)

    def get_white_count(self):
        return len(self.get_white_pieces())

    def get_black_king(self):
        return self.__get_king(False)

    def get_black_count(self):
        return len(self.get_black_pieces())

    def __get_king(self, is_white):
        for piece in self.__pieces:
            if piece.piece_type == PieceType.KING and piece.is_white == is_white:
                return piece

    def get_white_pieces(self):
        return self.get_pieces(True)

    def get_black_pieces(self):
        return self.get_pieces(False)

    def get_pieces(self, is_white):
        pieces = list()
        for piece in self.__pieces:
            if piece.is_captured:
                continue
            if piece.is_white == is_white:
                pieces.append(piece)
        return pieces

    def get_piece(self, coordinates):
        for piece in self.__pieces:
            if piece.is_captured:
                continue
            i, j = piece.coordinates
            if i == coordinates[0] and j == coordinates[1]:
                return piece
        return None

    def get_pieces_at_rank(self, rank):
        pieces = list()
        for piece in self.__pieces:
            if piece.is_captured:
                continue
            if piece.coordinates[1] == rank:
                pieces.append(piece)
        return pieces

    def get_pieces_at_file(self, file):
        pieces = list()
        for piece in self.__pieces:
            if piece.is_captured:
                continue
            if piece.coordinates[0] == file:
                pieces.append(piece)
        return pieces

    def get_pieces_by_type(self, piece_type, is_white):
        pieces = list()
        for piece in self.__pieces:
            if piece.is_captured or piece.is_white != is_white:
                continue
            if piece.piece_type == piece_type:
                pieces.append(piece)
        return pieces

    def clone(self):
        clone_state = ChessBoardState()
        for piece in self.__pieces:
            clone_state.add_piece(piece.clone())
        return clone_state

    def __iter__(self):
        return self

    def __next__(self):
        if self.__iterator_position < len(self.__pieces):
            return self.__pieces[self.__iterator_position]
        else:
            raise StopIteration