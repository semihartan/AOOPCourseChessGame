import pygame

from ui.uielement import UIElement


class UIPanel(UIElement):
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
        self.background = pygame.Color(180, 180, 180)
