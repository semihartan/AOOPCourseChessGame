from abc import ABC, abstractmethod


class KeyEventArgs:
    def __init__(self, key, char):
        self.key = key
        self.char = char


class IKeyboardInput(ABC):

    @abstractmethod
    def on_key_down(self, event_args: KeyEventArgs):
        pass

    @abstractmethod
    def on_key_up(self, event_args):
        pass


