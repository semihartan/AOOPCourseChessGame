import pygame.font

from algebraicnotationruler import AlgebraicNotationRuler

from chessboardstate import ChessBoardState
from chesssettings import ChessSettings
from gameengine import GameEngine
from gameobject import *
from hittest import HitTest
from bishop import Bishop
from king import King
from knight import Knight
from pawn import Pawn
from piecetype import PieceType
from queen import Queen
from rook import Rook
from resourcemanager import *


class ChessBoard(GameObject):

    def __init__(self):
        super().__init__()
        self.__position = [0, 0]
        self.__boardImage = ResourceManager.get_resource("chessboardOptimized2")
        self.__highlighterImage = ResourceManager.get_resource("highlighter")
        self.__highlighterShadowWhiteImage = ResourceManager.get_resource("highlighterShadowWhite")
        self.__highlighterShadowBlackImage = ResourceManager.get_resource("highlighterShadowBlack")
        self.__posDifference = [0, 0]
        self.__mouse_down = False
        self.__highlightedChecker = [0, 0]
        self.__font = pygame.font.SysFont("Courier New", 14, False, False)
        # self.__checkerPatternImage = ResourceManager.get_resource("CheckerSurface")
        self.__checkerPatternImage = pygame.Surface((ChessSettings.BOARDSIZE, ChessSettings.BOARDSIZE))
        self.__render_checker_pattern()
        self.__highligthing = False
        self.__moveImage = pygame.Surface((ChessSettings.SQUARESIZE, ChessSettings.SQUARESIZE))
        self.__moveImage.fill((50, 40, 160, 0))
        self.__piece_moved_event = None
        self.position_changed_event = None

        self.__algebraic_notation_ruler = AlgebraicNotationRuler(self)
        self.__algebraic_notation_ruler.render(self.__boardImage)

        self.has_moving_piece = False
        self.move_layout = None

        self.__pieces = list()
        self.init_pieces()
        for piece in self.__pieces:
            piece.initialize(self)
            piece.render_priority = 2
            piece.move_event = self.__piece_moved_event_handler
            GameEngine.add_game_object(piece)

    def draw(self, surface):

        position = self.position
        surface.blit(self.__boardImage, (position[0] - 60, position[1] - 60, 600, 600))
        #surface.blit(self.__checkerPatternImage,
        #             (position[0], position[1], ChessSettings.BOARDSIZE, ChessSettings.BOARDSIZE))

        points = self.__get_frame_points(2)
        pygame.draw.line(surface, ChessSettings.FRAMECOLOR, points[0], points[1], 4)
        pygame.draw.line(surface, ChessSettings.FRAMECOLOR, points[1], points[2], 4)
        pygame.draw.line(surface, ChessSettings.FRAMECOLOR, points[2], points[3], 4)
        pygame.draw.line(surface, ChessSettings.FRAMECOLOR, points[3], points[0], 4)

        if self.__highligthing:
            checker_coordinates = (position[0] + self.__highlightedChecker[0] * ChessSettings.SQUARESIZE - 4,
                                   position[1] + self.__highlightedChecker[1] * ChessSettings.SQUARESIZE - 4,
                                   ChessSettings.SQUARESIZE + 8, ChessSettings.SQUARESIZE + 8)
            # r, j = self.__highlightedChecker
            # if r % 2 == j % 2:
            #    surface.blit(self.__highlighterShadowWhiteImage, checker_coordinates)
            # else:
            #    surface.blit(self.__highlighterShadowBlackImage, checker_coordinates)
            surface.blit(self.__highlighterShadowBlackImage, checker_coordinates)

    def on_mouse_down(self, x, y):
        bounds = self.__get_bounds()
        checker_board_bounds = self.__get_checker_pattern_bounds()
        if not HitTest.is_point_in_rectangle((x, y), checker_board_bounds):
            if HitTest.is_point_in_rectangle((x, y), bounds):
                self.__mouse_down = True
                self.__posDifference = [x - self.__position[0], y - self.__position[1]]

    def on_mouse_move(self, x, y):
        if self.__mouse_down:
            self.position = [x - self.__posDifference[0], y - self.__posDifference[1]]
            if self.position_changed_event is not None:
                self.position_changed_event()
            self.__update_pieces_positions()
        if self.__position[0] < x < self.__position[0] + ChessSettings.BOARDSIZE and \
                self.__position[1] < y < self.__position[1] + ChessSettings.BOARDSIZE:
            self.__highligthing = True
            self.__highlightedChecker = self.__get_checker_from_point(x, y)
        else:
            self.__highligthing = False

    def on_mouse_up(self, x, y):
        self.__mouse_down = False

    def update(self):
        pass

    def init_pieces(self):
        # Add white pieces.
        for i in range(0, 8):
            self.add_piece(Pawn(True, [i, 6]))
        self.add_piece(Rook(True, [0, 7]))
        self.add_piece(Rook(True, [7, 7]))
        self.add_piece(Knight(True, [6, 7]))
        self.add_piece(Knight(True, [1, 7]))
        self.add_piece(Bishop(True, [5, 7]))
        self.add_piece(Bishop(True, [2, 7]))
        self.add_piece(Queen(True, [3, 7]))
        self.add_piece(King(True, [4, 7]))

        for i in range(0, 8):
            self.add_piece(Pawn(False, [i, 1]))
        self.add_piece(Rook(False, [0, 0]))
        self.add_piece(Rook(False, [7, 0]))
        self.add_piece(Knight(False, [6, 0]))
        self.add_piece(Knight(False, [1, 0]))
        self.add_piece(Bishop(False, [5, 0]))
        self.add_piece(Bishop(False, [2, 0]))
        self.add_piece(Queen(False, [3, 0]))
        self.add_piece(King(False, [4, 0]))

    def add_piece(self, piece):
        piece.initialize(self)
        piece.render_priority = 2
        piece.move_event = self.__piece_moved_event_handler
        GameEngine.add_game_object(piece)
        self.__pieces.append(piece)
        return piece

    def remove_piece(self, piece):
        piece.is_enabled = False
        piece.is_visible = False
        self.__pieces.remove(piece)

    def get_chessboard_state(self):
        state = ChessBoardState()
        for piece in self.__pieces:
            if not piece.is_captured:
                state.add_piece(piece)
        return state

    @property
    def piece_moved_event(self):
        return self.__piece_moved_event

    @piece_moved_event.setter
    def piece_moved_event(self, value):
        self.__piece_moved_event = value

    def __piece_moved_event_handler(self, piece):
        if self.__piece_moved_event is not None:
            self.__piece_moved_event(piece)

    def __update_pieces_positions(self):
        for piece in self.__pieces:
            piece.update_position()

    def to_screen_coordinates(self, x, y):
        return self.__position[0] + x * ChessSettings.SQUARESIZE, self.__position[1] + y * ChessSettings.SQUARESIZE

    def disable_side(self, is_white):
        for piece in self.__pieces:
            if piece.is_captured:
                continue
            if piece.is_white == is_white:
                piece.is_enabled = False
            else:
                piece.is_enabled = True

    def enable_side(self, is_white):
        for piece in self.__pieces:
            if piece.is_white == is_white:
                piece.is_enabled = True

    def disable_except(self, _piece):
        for piece in self.__pieces:
            if piece == _piece:
                piece.is_enabled = True
            else:
                piece.is_enabled = False

    def enable_except(self, _piece):
        for piece in self.__pieces:
            if piece == _piece:
                piece.is_enabled = False
            else:
                piece.is_enabled = True

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position[0] = position[0]
        self.__position[1] = position[1]
        self.__update_pieces_positions()

    def set_position_changed_event_handler(self, position_changed_event_handler):
        self.position_changed_event = position_changed_event_handler

    def __get_bounds(self):
        return self.__position[0] - 30, self.__position[1] - 30, 540, 540

    def __get_checker_pattern_bounds(self):
        return self.__position[0], self.__position[1], ChessSettings.BOARDSIZE, ChessSettings.BOARDSIZE

    def __get_checker_from_point(self, x, y):
        x -= self.__position[0]
        y -= self.__position[1]
        x //= ChessSettings.SQUARESIZE
        y //= ChessSettings.SQUARESIZE
        return x, y

    def __get_frame_points(self, width=1):
        points = [(self.__position[0] - width, self.__position[1] - width),
                  (self.__position[0] + 8 * ChessSettings.SQUARESIZE + width, self.__position[1] - width),
                  (self.__position[0] + 8 * ChessSettings.SQUARESIZE + width, self.__position[1] + 8 * ChessSettings.SQUARESIZE + width),
                  (self.__position[0] - width, self.__position[1] + 8 * ChessSettings.SQUARESIZE + width)]
        return points

    def __render_checker_pattern(self):
        surface = self.__checkerPatternImage
        for y in range(0, 8):
            for x in range(0, 8):
                if x % 2 == y % 2:
                    color = ChessSettings.CHECKERCOLORWHITE
                else:
                    color = ChessSettings.CHECKERCOLORBLACK
                sx, sy = self.to_screen_coordinates(x, y)
                surface.fill(color, (sx, sy, ChessSettings.SQUARESIZE, ChessSettings.SQUARESIZE))

    @staticmethod
    def create_piece(piece_type, is_white, coordinates):
        if piece_type == PieceType.KING:
            return King(is_white, coordinates)

        if piece_type == PieceType.QUEEN:
            return Queen(is_white, coordinates)

        if piece_type == PieceType.KNIGHT:
            return Knight(is_white, coordinates)

        if piece_type == PieceType.ROOK:
            return Rook(is_white, coordinates)

        if piece_type == PieceType.BISHOP:
            return Bishop(is_white, coordinates)

        if piece_type == PieceType.PAWN:
            return Pawn(is_white, coordinates)
