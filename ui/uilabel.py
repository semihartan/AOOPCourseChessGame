from ui.uielement import UIElement


class UILabel(UIElement):
    def __init__(self, text, position, width, height):
        super().__init__(position, width, height)
        self.background = (0, 0, 0, 0)
        self.foreground = (24, 24, 24)
        self.text = text
