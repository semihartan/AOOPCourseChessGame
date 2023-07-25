import pygame


class TextRenderer:
    __font = None

    def __init__(self, font_name, font_size, bold=False, italic=False):
        self.__font = pygame.font.SysFont(font_name, font_size, bold, italic)
        self.__bounds = [0, 0, 0, 0]
        self.__rendered_texts = list()
        self.__rendered_surface = None

    def add_text(self, position, color, text):
        surface = self.__font.render(text, True, color)
        size = surface.get_width(), surface.get_height()
        self.__bounds = TextRenderer.__rectangle_union(self.__bounds, (position[0], position[1], size[0], size[1]))
        self.__rendered_texts.append((surface, position, size))
        return size

    def change_font(self, font_name, font_size, bold=False, italic=False):
        self.__font = pygame.font.SysFont(font_name, font_size, bold, italic)
        self.clear()

    def clear(self):
        self.__bounds = [0, 0, 0, 0]
        self.__rendered_texts.clear()

    def get_surface(self):
        if self.__bounds[0] < 0:
            self.__bounds[0] -= self.__bounds[0]
            self.__bounds[2] += -self.__bounds[0]
        if self.__bounds[1] < 0:
            self.__bounds[1] -= self.__bounds[1]
            self.__bounds[3] += -self.__bounds[1]
        surface = self.__rendered_surface = pygame.Surface((self.__bounds[2], self.__bounds[3]), flags=pygame.SRCALPHA)
        for rendered_text in self.__rendered_texts:
            pos = rendered_text[1]
            size = rendered_text[2]
            surface.blit(rendered_text[0], (pos[0], pos[1], size[0], size[1]))
        return self.__rendered_surface

    @classmethod
    def draw(cls, surface, color, position, text, font_name, size, bold=False, italic=False, background=None):
        cls.__font = pygame.font.SysFont(font_name, size, bold, italic)

        font_surface = cls.__font.render(text, True, color)

        surface.blit(font_surface, (position[0], position[1], font_surface.get_width(), font_surface.get_height()))

    @staticmethod
    def __rectangle_union(rect1, rect2):
        min_x = min(rect1[0], rect2[0])
        min_y = min(rect1[1], rect2[1])
        max_x = max(rect1[0] + rect1[2], rect2[0] + rect2[2])
        max_y = max(rect1[1] + rect1[3], rect2[1] + rect2[3])
        return [min_x, min_y, max_x - min_x, max_y - min_y]