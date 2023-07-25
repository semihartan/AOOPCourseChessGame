import pygame.surface

from gameobject import GameObject


class Rectangle(GameObject):
    __rectangle_surface = None

    def __init__(self, position, color, size, opacity=255):
        super().__init__()
        self.position = position
        self.color = color
        self.size = size
        self.__opacity = opacity
        self.__surface = pygame.surface.Surface(size, flags=pygame.SRCALPHA)
        self.__surface.fill(self.color, (0, 0, self.size[0], self.size[1]))
        self.set_opacity(opacity)

    def draw(self, surface):
        surface.blit(self.__surface, (self.position[0], self.position[1], self.size[0], self.size[1]))

    def on_mouse_down(self, x, y):
        pass

    def on_mouse_move(self, x, y):
        pass

    def on_mouse_up(self, x, y):
        pass

    def update(self):
        pass

    def set_opacity(self, opacity):
        self.__opacity = opacity
        self.__surface.set_alpha(self.__opacity)

    @classmethod
    def fill(cls, surface, color, bounds):
        cls.__rectangle_surface = pygame.Surface((bounds[2], bounds[3]), flags=pygame.SRCALPHA)
        cls.__rectangle_surface.fill(color, (0, 0, bounds[2], bounds[3]))
        surface.blit(cls.__rectangle_surface, bounds)
        del cls.__rectangle_surface
