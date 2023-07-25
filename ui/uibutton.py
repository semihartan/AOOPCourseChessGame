import pygame
from enum import Flag
from ui.uielement import UIElement


class UIButton(UIElement):
    def __init__(self, text, position, width, height):
        super().__init__(position, width, height)
        self.font_size = 15
        self.text = text

    def draw(self, surface):
        UIElement.draw(self, surface)

    def on_mouse_down(self, x, y):
        UIElement.on_mouse_down(self, x, y)
        self.background = pygame.Color(104, 147, 255)
        self.invalidate()

    def on_mouse_move(self, x, y):
        UIElement.on_mouse_move(self, x, y)

    def on_mouse_up(self, x, y):
        UIElement.on_mouse_up(self, x, y)
        self.background = pygame.Color(0, 19, 70)
        self.invalidate()

    def on_mouse_enter(self):
        self.background = pygame.Color(0, 19, 255)
        self.invalidate()

    def on_mouse_leave(self):
        self.background = pygame.Color(104, 19, 255)
        self.invalidate()

