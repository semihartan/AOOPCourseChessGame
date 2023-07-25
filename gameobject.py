from imouseinput import *
from idrawable import *
from  iupdatable import IUpdatable


# Every object in the game should implement this base class. Every game object has a visibility, a render priority and
# a flag to specify whether it can get mouse input or not. Derived classes must override its member methods.
class GameObject(IDrawable, IMouseInput, IUpdatable):

    def __init__(self, render_priority=-1):
        self.is_visible = True
        # The flag that tells the game engine whether the object should take the mouse input or not.
        self.is_enabled = True
        # Render Priority will determine the z order of the drawn objects. 0 means that the object will
        # be drawn as first and the ascending values will be placed on each others.
        # Default value is 0. Derived classes can override this value according to their needs.
        self.render_priority = render_priority

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def on_mouse_down(self, x, y):
        pass

    @abstractmethod
    def on_mouse_move(self, x, y):
        pass

    @abstractmethod
    def on_mouse_up(self, x, y):
        pass

    @abstractmethod
    def update(self):
        pass
