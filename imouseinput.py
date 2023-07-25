from abc import  ABC, abstractmethod


# An interface between the game engine and objects to get and process the mouse input.
class IMouseInput(ABC):

    @abstractmethod
    def on_mouse_down(self, x, y):
        pass

    @abstractmethod
    def on_mouse_move(self, x, y):
        pass

    @abstractmethod
    def on_mouse_up(self, x, y):
        pass
