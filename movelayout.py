import math

import gameobject
from animation import Animation
from animationengine import AnimationEngine
from animationvariable import AnimationVariable
from chesssettings import ChessSettings
from interpolationtype import InterpolationType
from move import Move
from movetype import MoveType
from piecetype import PieceType
from resourcemanager import ResourceManager
from soundeffect import SoundEffect
from ui.pieceselectdialog import PieceSelectDialog


class MoveLayout(gameobject.GameObject):
    def __init__(self, chess_board, is_virtual=False):
        super().__init__()
        self.__owner = None
        self.chess_board = chess_board
        self.chess_board_state = None
        self.__square_size = ChessSettings.SQUARESIZE
        self.__moves = list()
        self.__iterable_position = 0
        self.promotion_move = None
        self.captured_piece = None
        self.game_controller = None
        self.is_visible = not is_virtual

        if not is_virtual:
            self.__piece_select_dialog = PieceSelectDialog()
            self.__piece_select_dialog.piece_selected_event += self.__piece_selected_handler
            self.__promoted_piece_type = PieceType.UNKNOWN
            self.__move_image = ResourceManager.get_resource("MoveBackground")
            self.__move_capture_image = ResourceManager.get_resource("CaptureMoveBackground")
            self.__move_castling_image = ResourceManager.get_resource("CastlingMoveBackground")
            self.__move_promotion_image = ResourceManager.get_resource("PromotionMoveBackground")

            self.__attack_animation = Animation(3.0, name="Attack Animation", repeat=Animation.FOREVER)
            self.__attack_animation_variable = AnimationVariable(interpolation_type=InterpolationType.Custom,
                                                                 func=MoveLayout.__attack_animation_func)
            self.__attack_animation.add_variable(self.__attack_animation_variable)
            self.__attack_animation_variable.start = 0
            self.__attack_animation_variable.end = 255
            AnimationEngine.add_animation(self.__attack_animation)

            self.__capture_animation = Animation(0.4, "CaptureAnimation", 1)
            self.__capture_animation_variable = AnimationVariable(interpolation_type=InterpolationType.Linear,
                                                                  func=MoveLayout.__capture_animation_func)
            self.__capture_animation.animated_event += self.__capture_animation_animated
            self.__capture_animation.finished_event += self.__capture_animation_finished
            self.__capture_animation.add_variable(self.__capture_animation_variable)
            self.__capture_animation_variable.start = 255
            self.__capture_animation_variable.end = 100

    def add_move_by_coordinate(self, coords, only_capture=False, can_capture=True):
        if not Move.is_valid_coords(coords):
            return False
        if self.chess_board_state is None:
            piece = self.chess_board.get_chessboard_state().get_piece(coords)
        else:
            piece = self.chess_board_state.get_piece(coords)

        if piece is not None:
            if self.__owner.is_opponent(piece) and can_capture:

                self.__moves.append(Move(self, MoveType.Capture, coords))
                return True
            elif not self.__owner.is_opponent(piece):
                return True
        else:
            if not only_capture:
                self.__moves.append(Move(self, MoveType.Move, coords))
            return False

        # if not only_capture and piece is None:
        #     self.__moves.append(Move(False, coords))
        # elif can_capture and piece is not None:
        #     if self.__owner.is_opponent(piece):
        #         self.__moves.append(Move(True, coords))
        #     return True
        #  return False

    def add_moves(self, moves):
        for move in moves:
            self.__moves.append(move)

    def add_move(self, move):
        self.__moves.append(move)

    def clear(self):
        self.__moves.clear()

    def contains(self, coords):
        for move in self.__moves:
            move_coords = move.coordinates
            if move_coords[0] == coords[0] and move_coords[1] == coords[1]:
                return True
        return False

    def count(self):
        return len(self.__moves)

    def draw(self, surface):
        if len(self.__moves) == 0 or not self.is_visible:
            return
        for move in self.__moves:
            i, j = move.coordinates
            px, py = self.chess_board.to_screen_coordinates(i, j)
            bounds = [px, py, self.__square_size, self.__square_size]
            if (move.move_type & MoveType.Capture) == MoveType.Capture:
                self.__move_capture_image.set_alpha(self.__attack_animation_variable.value)
                if move.move_type & MoveType.EnPassant == MoveType.EnPassant:
                    surface.blit(self.__move_castling_image, bounds)
                    px, py = self.chess_board.to_screen_coordinates(move.en_passant_coord[0],
                                                                      move.en_passant_coord[1])
                    bounds[0] = px
                    bounds[1] = py
                surface.blit(self.__move_capture_image, bounds)
            elif move.move_type == MoveType.Move:
                surface.blit(self.__move_image, bounds)
            elif move.move_type == MoveType.Castling:
                surface.blit(self.__move_castling_image, bounds)
            elif move.move_type & MoveType.Promotion == MoveType.Promotion:
                surface.blit(self.__move_promotion_image, bounds)

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value
        if self.is_visible:
            self.__attack_animation.play()

    def on_mouse_down(self, x, y):
        if len(self.__moves) == 0 or self.chess_board.has_moving_piece:
            return
        chessboard_position = self.chess_board.position
        x -= chessboard_position[0]
        y -= chessboard_position[1]
        x //= self.__square_size
        y //= self.__square_size
        for move in self.__moves:
            move_coords = move.coordinates
            if move_coords[0] == x and move_coords[1] == y:
                self.is_visible = False
                if  move.move_type & MoveType.Capture == MoveType.Capture:
                    self.__attack_animation.stop()
                    move.execute()
                    self.__capture_animation.set_repeat(1)
                    self.__capture_animation.play()
                    AnimationEngine.add_animation(self.__capture_animation)
                elif move.move_type & MoveType.Promotion == MoveType.Promotion:
                    self.__piece_select_dialog.show()
                    self.promotion_move = move
                    move.execute()
                else:
                    move.execute()

    def on_mouse_move(self, x, y):
        pass

    def on_mouse_up(self, x, y):
        pass

    def remove(self, move):
        self.__moves.remove(move)

    def update(self):
        pass

    def __move_end_handler(self, sender, event_data):
        if self.__promoted_piece_type != PieceType.UNKNOWN:
            self.chess_board.remove_piece(self.owner)
            piece = self.chess_board.add_piece(self.chess_board.create_piece(self.__promoted_piece_type, self.owner.is_white, self.owner.coordinates))
            piece.game_controller = self.game_controller
            piece.chess_board = self.owner.chess_board
            self.__promoted_piece_type = PieceType.UNKNOWN
            sender.move_end_event -= self.__move_end_handler

    def __piece_selected_handler(self, sender, args):
        self.__promoted_piece_type = self.__piece_select_dialog.piece_type
        self.promotion_move.execute()
        self.__owner.move_end_event += self.__move_end_handler

    @staticmethod
    def __capture_animation_func(t):
        # return -4.0 * (t - 0.5) ** 2 + 1.0
        return -t + 1.0

    @staticmethod
    def __attack_animation_func(t):
        # return -4.0 * (t ** 2) + 1
        return 0.5 * math.sin(6.0 * math.pi * t + 0.5 * math.pi) + 0.5

    def __capture_animation_animated(self, sender, args):
        self.captured_piece.opacity = self.__capture_animation_variable.value

    def __capture_animation_finished(self, sender, args):
        self.captured_piece.is_captured = True
        SoundEffect.play_piece_capture_sound()

    def __getitem__(self, coords):
        for move in self.__moves:
            if move.coordinates[0] == coords[0] and move.coordinates[1] == coords[1]:
                return move
        return None

    def __iter__(self):
        return self

    def __next__(self):
        if self.__iterable_position < self.count():
            move = self.__moves[self.__iterable_position]
            self.__iterable_position += 1
            return move
        else:
            self.__iterable_position = 0
            raise StopIteration
