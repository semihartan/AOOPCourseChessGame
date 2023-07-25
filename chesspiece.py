from event import Event
from piecetype import PieceType
import util
from animationengine import AnimationEngine
from chesssettings import ChessSettings
from gameobject import *
from move import Move
from movelayout import MoveLayout
from movetype import MoveType
from resourcemanager import *
from animationvariable import AnimationVariable
from animation import Animation
from soundeffect import SoundEffect


class ChessPiece(GameObject):

    def __init__(self, is_white, coordinates):
        super().__init__()
        self.chess_board = None
        self.game_controller = None
        self.__coordinates = coordinates
        self.__initial_coordinates = coordinates
        self.__piece_type = None
        self.__new_coordinates = (0, 0)
        self.__position = (0, 0)
        self.__has_moved = False
        self.__is_captured = False
        self.__opacity = 255
        self._is_white = is_white
        self.__is_selected = False
        self.move_event = None
        self.move_start_event = Event()
        self.move_end_event = Event()
        if is_white:
            self._translation_vector = -1
        else:
            self._translation_vector = 1

        prefix = ""
        if is_white:
            prefix = "White"
        else:
            prefix = "Black"
        self.__image = ResourceManager.get_resource(prefix + self._name())
        self.__selected_background_image = ResourceManager.get_resource("PieceSelectedBackground")
        self.__animation_variable_x = AnimationVariable()
        self.__animation_variable_y = AnimationVariable()
        self.__animation = Animation(1.0, name="Move Animation")
        self.__animation.add_variable(self.__animation_variable_x)
        self.__animation.add_variable(self.__animation_variable_y)
        self.__animation.finished_event += self.__finished_event_handler
        self.__animation.animated_event += self.__animated_event_handler

    def draw(self, surface):
        if self.__is_selected:
            surface.blit(self.__selected_background_image, (self.__position[0], self.__position[1], 60, 60))
        surface.blit(self.__image, (self.__position[0], self.__position[1], 60, 60))

    def on_mouse_down(self, x, y):
        if self.chess_board.has_moving_piece:
            return
        move_layout = self.chess_board.move_layout

        if self.is_hit(x, y):
            self.__is_selected = True
            move_layout.is_visible = True
            move_layout.is_enabled = True
            # If there is moves previously added by another piece, delete them.
            move_layout.clear()

            move_layout.owner = self
            self.build_moves(move_layout)
            # Validate the moves built by the pieces' build_moves method.
            # This involves the remove of moves that cause the check or check mate.
            valid_moves = list()
            controller = self.game_controller
            for move in move_layout:
                chessboard_state = self.chess_board.get_chessboard_state().clone()
                clone_piece = chessboard_state.get_piece(self.coordinates)
                if move.move_type == MoveType.Capture:
                    captured_piece = chessboard_state.get_piece(move.coordinates)
                    captured_piece.is_captured = True
                clone_piece.coordinates = move.coordinates

                if controller.test_check(chessboard_state, self.is_white) is None:
                    valid_moves.append(move)

            move_layout.clear()
            move_layout.add_moves(valid_moves)

            if self.piece_type == PieceType.KING:
                # Check if the king can do castling move.
                # A player can only castle if all the conditions below are true:
                #   * The player has never moved the king or the rook.
                #   * There are no pieces between the king and the rook to the side where the player is castling.
                #   * The king is not in check.
                #   * The opponent is not attacking any of the squares between the king and where it will land.
                chessboard_state = self.chess_board.get_chessboard_state()
                rooks = chessboard_state.get_pieces_by_type(PieceType.ROOK, self.is_white)
                castling_moves = list()
                for rook in rooks:
                    move_layout = self.chess_board.move_layout
                    if self.has_moved or rook.has_moved:
                        continue
                    same_rank_pieces = chessboard_state.get_pieces_at_rank(self.coordinates[1])
                    has_piece_between = False
                    for piece in same_rank_pieces:
                        if piece.is_white:
                            if piece.piece_type == PieceType.KING or piece.piece_type == PieceType.ROOK:
                                continue
                        if (self.coordinates[0] < piece.coordinates[0] and piece.coordinates[0] < rook.coordinates[0])\
                            or \
                            (rook.coordinates[0] < piece.coordinates[0] and piece.coordinates[0] < self.coordinates[0]):
                            has_piece_between = True
                            break
                    if has_piece_between:
                        continue
                    controller = self.game_controller
                    if controller.test_check(self.chess_board.get_chessboard_state().clone(), self.is_white) is not None:
                        continue

                    if self.coordinates[0] > rook.coordinates[0]:
                        castling_coordinate = (self.coordinates[0] - 2, self.coordinates[1])
                    else:
                        castling_coordinate = (self.coordinates[0] + 2, self.coordinates[1])

                    virtual_move_layout = MoveLayout(self.chess_board, is_virtual=True)
                    opponent_pieces = chessboard_state.get_pieces(not self.is_white)
                    causing_check = False
                    for piece in opponent_pieces:
                        virtual_move_layout.owner = piece
                        virtual_move_layout.chess_board_state = chessboard_state
                        piece.build_moves(virtual_move_layout)
                        if virtual_move_layout.contains(castling_coordinate):
                            causing_check = True
                            break

                    if causing_check:
                        continue
                    castling_move = Move(move_layout, MoveType.Castling, castling_coordinate)
                    castling_move.castling_rook = rook
                    castling_moves.append(castling_move)
                move_layout.add_moves(castling_moves)

            elif self.piece_type == PieceType.PAWN:
                # Handle the pawn promotion case
                for move in move_layout:
                    if (self.is_white and move.coordinates[1] == 0) or\
                       (not self.is_white and move.coordinates[1] == 7):
                        move.move_type = move.move_type | MoveType.Promotion
                # Handle the en passant rule.
                if abs(self.__initial_coordinates[1] - self.coordinates[1]) == 3:
                    i, j = self.coordinates
                    en_passant_coords = ((i - 1, j), (i + 1, j))
                    for en_passant_coord in en_passant_coords:
                        piece = self.chess_board.get_chessboard_state().get_piece(en_passant_coord)
                        if piece is None:
                            continue
                        if self.is_opponent(piece):
                            if piece.piece_type == PieceType.PAWN and piece.has_moved_only_two:
                                move = Move(move_layout, MoveType.EnPassant | MoveType.Capture, (en_passant_coord[0], en_passant_coord[1] + self._translation_vector))
                                move.en_passant_coord = en_passant_coord
                                move_layout.add_move(move)
            # Return a True to indicate that we have handled this mouse message.
            return True
        else:
            self.__is_selected = False
            move_layout.is_visible = False
            move_layout.is_enabled = False
            return False

    def on_mouse_move(self, x, y):
        pass

    def on_mouse_up(self, x, y):
        pass

    def update(self):
        pass

    @property
    def is_captured(self):
        return self.__is_captured

    @is_captured.setter
    def is_captured(self, value):
        self.__is_captured = value
        self.is_visible = not value
        self.is_enabled = not value

    @property
    def coordinates(self):
        return self.__coordinates

    @property
    def piece_type(self):
        return PieceType.UNKNOWN

    @coordinates.setter
    def coordinates(self, value):
        self.__coordinates = value
        self.update_position()

    @property
    def has_moved(self):
        return self.__has_moved

    @property
    def is_white(self):
        return self._is_white

    def is_opponent(self, piece):
        return self._is_white != piece.is_white

    def is_opponent_at(self, coordinates):
        piece = self.chess_board.get_piece(coordinates)
        if piece is None:
            return True
        return self.is_opponent(piece)

    def is_hit(self, x, y):
        px, py = self.chess_board.position
        x -= px
        y -= py
        x //= 60
        y //= 60
        if x == self.__coordinates[0] and y == self.__coordinates[1]:
            return True
        return False
    @property
    def position(self):
        return self.__position

    @abstractmethod
    def build_moves(self, move_layout):
        pass

    # @abstractmethod
    # def get_capture_possible_moves(self):
    #    pass

    def move(self, coordinates):
        if not self.__has_moved:
            if self.piece_type == PieceType.PAWN and abs(self.coordinates[1] - coordinates[1]) == 2:
                self.has_moved_only_two = True
            self.__has_moved = True
        self.__is_selected = False
        self.chess_board.has_moving_piece = True
        i, j = self.__coordinates
        self.__new_coordinates = coordinates
        new_position = (coordinates[0] * ChessSettings.SQUARESIZE, coordinates[1] * ChessSettings.SQUARESIZE)
        self.__animation_variable_x.start = i * ChessSettings.SQUARESIZE
        self.__animation_variable_x.end = new_position[0]
        self.__animation_variable_y.start = j * ChessSettings.SQUARESIZE
        self.__animation_variable_y.end = new_position[1]
        self.__animation.reset(1)
        AnimationEngine.add_animation(self.__animation)
        self.__animation.play()

    def __animated_event_handler(self, sender, args):
        px, py = self.chess_board.position
        self.__position = (px + self.__animation_variable_x.value, py + self.__animation_variable_y.value)

    def __finished_event_handler(self, sender, args):
        self.coordinates = self.__new_coordinates
        self.chess_board.has_moving_piece = False
        move_layout = self.chess_board.move_layout
        move_layout.clear()

        SoundEffect.play_move_sound()
        self.move_end_event(self, None)
        if self.move_event is not None:
            self.move_event(self)

    @property
    def opacity(self):
        return self.__opacity

    @opacity.setter
    def opacity(self, value):
        self.__opacity = util.Util.clamp(value, 0, 255)
        self.__image.set_alpha(self.__opacity)

    def initialize(self, chess_board):
        self.chess_board = chess_board
        self.update_position()

    @abstractmethod
    def _name(self):
        pass

    def update_position(self):
        if self.chess_board is None:
            return
        self.__position = self.chess_board.to_screen_coordinates(self.__coordinates[0], self.__coordinates[1])

    @abstractmethod
    def can_move(self):
        pass

    def __is_valid_move(self, coords, only_capture=False, can_capture=True):
        if not Move.is_valid_coords(coords):
            return False
        piece = self.chess_board.get_piece(coords)

        # If the square at the coords is not empty
        if piece is not None:
            # and the piece at the square is opponent, and the move can be capture the piece.
            if self.is_opponent(piece) and can_capture:
                return True
            # If the piece is not opponent, then return false to indicate that the move is not valid.
            elif not self.is_opponent(piece):
                return False
        # If the square is empty.
        else:
            # and the move can be done only if a opponent piece exists, then return False, otherwise True.
            if only_capture:
                return False
            return True

    @abstractmethod
    def clone(self):
        pass
