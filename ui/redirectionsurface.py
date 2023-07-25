

class RedirectionSurface:
    def __init__(self, element_id, internal_surface):
        self.__element_id = element_id
        self.__internal_surface = internal_surface
        self.__size = internal_surface.get_size()
        self.__needs_redraw = True

    @property
    def internal_surface(self):
        return self.__internal_surface

    @internal_surface.setter
    def internal_surface(self, value):
        self.__internal_surface = value

    @property
    def needs_redraw(self):
        return self.__needs_redraw

    @needs_redraw.setter
    def needs_redraw(self, value):
        self.__needs_redraw = value

    @property
    def element_id(self):
        return self.__element_id

    @element_id.setter
    def element_id(self, value):
        self.__element_id = value

    @property
    def size(self):
        return self.__size