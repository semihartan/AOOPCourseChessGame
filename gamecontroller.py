import math

from animation import Animation
from animationengine import AnimationEngine
from animationvariable import AnimationVariable
from chesssettings import ChessSettings
from gameobject import GameObject
from gamestatus import GameStatus
from controlresult import ControlResult
from interpolationtype import InterpolationType
from movelayout import MoveLayout
from movetype import MoveType
from rectangle import Rectangle
from resourcemanager import ResourceManager
from soundeffect import SoundEffect


class GameController(GameObject):
    def __init__(self, chessboard):
        super().__init__()
        self.__chessboard = chessboard
        self.game_status = GameStatus.Active
        self.control_status = ControlResult.UNKNOWN
        self.check_side = None
        self.__check_background_image = ResourceManager.get_resource("CheckBackground")
        self.__check_background_animation_image = ResourceManager.get_resource("CheckBackgroundAnimationClouds")
        self.is_check = False
        self.__check_coordinates = None

        self.__check_animation = Animation(30, name="Check Animation", repeat=Animation.FOREVER)
        self.__check_animation_variable = AnimationVariable(interpolation_type=InterpolationType.Custom,
                                                            func=GameController.__check_animation_func)
        self.__check_animation.add_variable(self.__check_animation_variable)
        self.__check_animation_variable.start = 0
        self.__check_animation_variable.end = 255
        AnimationEngine.add_animation(self.__check_animation)

    def draw(self, surface):
        if self.control_status != ControlResult.UNKNOWN:
            position = self.__chessboard.to_screen_coordinates(self.__check_coordinates[0],
                                                               self.__check_coordinates[1])
            size = ChessSettings.SQUARESIZE
            # Rectangle.fill(surface, (255, 166, 43, self.__check_animation_variable.value), (position[0], position[1], size, size))
            # self.__check_background_image.set_alpha(self.__check_animation_variable.value)
            #surface.blit(self.__check_background_image, (position[0], position[1], size, size))
            Rectangle.fill(surface, (26, 0, 0, 255), (position[0], position[1], size, size))
            source_x = 540 * (self.__check_animation_variable.value / 255)
            surface.blit(self.__check_background_animation_image, (position[0], position[1], size, size)
                        , (source_x, 0, 60, 60))

    def on_mouse_down(self, x, y):
        pass

    def on_mouse_move(self, x, y):
        pass

    def on_mouse_up(self, x, y):
        pass

    def update(self):
        pass

    def do_controls(self):
        self.control_status = ControlResult.UNKNOWN
        if self.test_check_mate(self.__chessboard.get_chessboard_state().clone(), True):
            return True
        elif self.test_check_mate(self.__chessboard.get_chessboard_state().clone(), False):
            return True

        if self.control_status == ControlResult.CHECK:
            SoundEffect.play_check_sound()
            self.__check_animation.play()
        else:
            self.__check_animation.pause()

    def test_check_mate(self, chessboard_state, for_white):
        king_checked = self.test_check(chessboard_state, for_white)
        if king_checked is not None:
            self.__check_coordinates = king_checked.coordinates
            move_layout = MoveLayout(self.__chessboard, is_virtual=True)
            if for_white:
                pieces = chessboard_state.get_white_pieces()
            else:
                pieces = chessboard_state.get_black_pieces()
            for piece in pieces:
                clone_state = chessboard_state.clone()
                move_layout.owner = piece
                move_layout.chess_board_state = clone_state
                piece.build_moves(move_layout)
                for move in move_layout:
                    moved_clone_state = clone_state.clone()
                    clone_piece = moved_clone_state.get_piece(piece.coordinates)
                    if move.move_type & MoveType.Capture == MoveType.Capture:
                        captured_piece = moved_clone_state.get_piece(move.coordinates)
                        captured_piece.is_captured = True
                    clone_piece.coordinates = move.coordinates

                    if self.test_check(moved_clone_state, clone_piece.is_white) is None:
                        self.control_status = ControlResult.CHECK
                        return False
                move_layout.clear()
            self.control_status = ControlResult.CHECKMATE
            self.check_side = king_checked.is_white
            SoundEffect.play_checkmate_sound()
            return True

    def test_check(self, chessboard_state, for_white):
        chessboard = self.__chessboard
        state = chessboard_state
        move_layout = MoveLayout(chessboard, is_virtual=True)

        if for_white:
            king = state.get_white_king()
            opponent_pieces = state.get_black_pieces()
        else:
            king = state.get_black_king()
            opponent_pieces = state.get_white_pieces()

        for piece in opponent_pieces:
            move_layout.owner = piece
            move_layout.chess_board_state = chessboard_state
            piece.build_moves(move_layout)
            if move_layout.contains(king.coordinates):
                return king
            move_layout.clear()

        return None

    @staticmethod
    def __check_animation_func(t):
        # return -4.0 * (t ** 2) + 1
        # return 0.5 * math.sin(6.0 * math.pi * t + 0.5 * math.pi) + 0.5
        #return t
        return 0.5 * math.sin(2 * math.pi * t - 0.5 * math.pi) + 0.5