
# Provides a simple event feature similar to in C#.
class Event:
    def __init__(self):
        self.__subscribers = list()

    def __add__(self, handler):
        self.__subscribers.append(handler)
        return self

    def __sub__(self, handler):
        self.__subscribers.remove(handler)
        return self

    def __call__(self, *args, **kwargs):
        for handler in self.__subscribers:
            handler(args[0], args[1])
