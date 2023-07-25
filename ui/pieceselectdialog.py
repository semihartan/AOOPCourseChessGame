import pygame

from event import Event
from interpolationtype import InterpolationType
from piecetype import PieceType
from resourcemanager import ResourceManager
from ui.uibutton import UIButton
from ui.uilabel import UILabel
from ui.uipanel import UIPanel
from ui.uielement import UIElement
from animation import Animation
from animationvariable import AnimationVariable
from animationengine import AnimationEngine


class PieceSelectDialog(UIElement):
    def __init__(self):
        super().__init__((0, 0), 900, 700)
        #self.position = (250, 0)
        #self.size = (400, 700)
        self.background = (44, 44, 44, 160)
        self.is_visible = False

        self.__panel = UIPanel((250, 0), 400, 700)
        self.__panel.background = (255, 255, 255)

        self.__label_title = UILabel("Pawn Promotion", (30, 50), 100, 60)
        self.__label_title.auto_size = True

        self.__label_description = UILabel("You can promote your pawn! "
                                           "Which piece do you want to \npromote your pawn to?", (30, 230), 100, 60)
        self.__label_description.font_size = 16
        self.__label_description.auto_size = True

        self.__panel.add_child(self.__label_title)
        self.__panel.add_child(self.__label_description)

        self.__quenn_button = UIButton("", (20, 286), 120, 24)
        self.__quenn_button.border_width = 1
        self.__quenn_button.border_color = pygame.Color("black")
        self.__quenn_button.image = ResourceManager.get_resource("WhiteQueen")
        self.__quenn_button.auto_size = True
        self.__quenn_button.name = "queenButton"
        self.__quenn_button.click_event += self.__button_click_handler

        self.__rook_button = UIButton("", (110, 286), 120, 24)
        self.__rook_button.name = "rookButton"
        self.__rook_button.border_width = 1
        self.__rook_button.border_color = pygame.Color("black")
        self.__rook_button.image = ResourceManager.get_resource("WhiteRook")
        self.__rook_button.auto_size = True
        self.__rook_button.click_event += self.__button_click_handler

        self.__bishop_button = UIButton("", (200, 286), 120, 24)
        self.__bishop_button.name = "bishopButton"
        self.__bishop_button.border_width = 1
        self.__bishop_button.border_color = pygame.Color("black")
        self.__bishop_button.image = ResourceManager.get_resource("WhiteBishop")
        self.__bishop_button.auto_size = True
        self.__bishop_button.click_event += self.__button_click_handler

        self.__knight_button = UIButton("", (290, 286), 120, 24)
        self.__knight_button.name = "knightButton"
        self.__knight_button.border_width = 1
        self.__knight_button.border_color = pygame.Color("black")
        self.__knight_button.image = ResourceManager.get_resource("WhiteKnight")
        self.__knight_button.auto_size = True
        self.__knight_button.click_event += self.__button_click_handler

        self.__panel.add_child(self.__quenn_button)
        self.__panel.add_child(self.__rook_button)
        self.__panel.add_child(self.__bishop_button)
        self.__panel.add_child(self.__knight_button)
        self.add_child(self.__panel)
        self.piece_selected_event = Event()
        self.piece_type = PieceType.UNKNOWN

        self.__fade_effect_animation = Animation(0.6, "FadeInOutAnimation", 1)
        self.__fade_effect_animation_var = AnimationVariable(0.0, 1.0, interpolation_type=InterpolationType.Quadratic)
        self.__fade_effect_animation.add_variable(self.__fade_effect_animation_var)
        self.__fade_effect_animation.animated_event += self.__fade_effect_animated
        AnimationEngine.add_animation(self.__fade_effect_animation)

    def show(self):
        UIElement.show(self)
        self.__fade_effect_animation.reset(1)
        self.__fade_effect_animation.play()

    def __button_click_handler(self, sender, args):
        if sender.name == "queenButton":
            self.piece_type = PieceType.QUEEN
        elif sender.name == "rookButton":
            self.piece_type = PieceType.ROOK
        elif sender.name == "bishopButton":
            self.piece_type = PieceType.BISHOP
        elif sender.name == "knightButton":
            self.piece_type = PieceType.KNIGHT
        self.is_visible = False
        self.piece_selected_event(self, None)

    def __fade_effect_animated(self, sender, args):
        self.__panel.opacity = self.__fade_effect_animation_var.value * 255
        self.__panel.position[1] = -60 + self.__fade_effect_animation_var.value * 60
