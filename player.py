

class Player:
    def __init__(self, name, is_white):
        self.__name = name
        self.__is_white = is_white

    @property
    def name(self):
        return self.__name

    @property
    def is_white(self):
        return self.__is_white
