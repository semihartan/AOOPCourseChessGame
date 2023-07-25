import pygame

from ui.uipanel import UIPanel
from ui.uibutton import UIButton
from ui.uilabel import UILabel


from chessboard import ChessBoard
from chessclock import ChessClock
from gamecontroller import GameController
from gameengine import GameEngine
from movelayout import MoveLayout
from soundeffect import SoundEffect


class ChessGame:
    def __init__(self):
        SoundEffect.init()

        self.__players = list()

        self.__is_turn_white = True
        self.__home_page = UIPanel((0, 0), 900, 700)
        self.__home_page.background = pygame.Color("white")

        self.__project_name_label = UILabel("AOOP: Design Chess", (300, 250), 0, 0)
        self.__project_name_label.font_size = 40
        self.__project_name_label.auto_size = True
        self.__play_button = UIButton("Play", (360, 380), 160, 80)
        self.__play_button.font_size = 25
        self.__play_button.click_event += self.__play_button_click

        self.__home_page.add_child(self.__play_button)
        self.__home_page.add_child(self.__project_name_label)

        self.__message_overlay_panel = UIPanel((0, 0), 900, 700)
        self.__message_overlay_panel.background = (44, 44, 44, 160)
        self.__message_overlay_panel.is_visible = False
        self.__game_result_panel = UIPanel((250, 200), 400, 300)
        self.__game_result_label = UILabel("", (20, 20), 0, 0)
        self.__game_result_label.font_size = 22
        self.__game_result_label.auto_size = True
        self.__game_result_panel.add_child(self.__game_result_label)

        self.__message_overlay_panel.add_child(self.__game_result_panel)

        self.__chessboard = GameEngine.add_game_object(ChessBoard())
        self.__chessboard.render_priority = 0
        self.__chessboard.piece_moved_event = self.__piece_moved_event_handler
        self.__chessboard.position = (90, 120)
        self.__game_controller = GameEngine.add_game_object(GameController(self.__chessboard))
        self.__game_controller.render_priority = 1

        self.__move_layout = GameEngine.add_game_object(MoveLayout(chess_board=self.__chessboard))
        self.__move_layout.render_priority = 1
        self.__move_layout.game_controller = self.__game_controller

        self.__chessboard.move_layout = self.__move_layout

        for piece in self.__chessboard.get_chessboard_state().pieces:
            piece.game_controller = self.__game_controller

        self.__chess_clock = GameEngine.add_game_object(ChessClock(minutes=10))
        self.__chess_clock.position = [610, 280]
        self.__chess_clock.timesup_event = self.__timesup_event_handler

        self.__players = list()
        self.set_turn(False)
        self.__chess_clock.start()

    def set_turn(self, is_white):
        self.__chessboard.disable_side(is_white)

    def __piece_moved_event_handler(self, piece):
        self.__is_turn_white = not piece.is_white
        self.__chess_clock.switch()
        self.set_turn(not self.__is_turn_white)
        if self.__game_controller.do_controls():
            if self.__game_controller.check_side:
                self.__game_result_label.text = "White Won!"
            else:
                self.__game_result_label.text = "Black Won!"
            self.__chess_clock.stop()
            self.__message_overlay_panel.show()

    def __timesup_event_handler(self, is_left):
        self.__chess_clock.stop()
        state = self.__chessboard.get_chessboard_state()
        if state.get_black_count() > state.get_white_count():
            self.__game_result_label.text = "Black Won!"
        else:
            self.__game_result_label.text = "White Won!"
        self.__message_overlay_panel.show()

    def __play_button_click(self, sender, args):
        self.__home_page.hide()
