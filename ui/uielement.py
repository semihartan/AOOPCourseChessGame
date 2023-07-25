from enum import Flag

import pygame

from event import Event
from gameobject import GameObject
from hittest import HitTest
from ikeyboardinput import IKeyboardInput, KeyEventArgs
from textrenderer import TextRenderer
from ui.uimanager import UIManager


class UIElement(GameObject, IKeyboardInput):
    element_id = 0

    def __init__(self, position, width, height):
        super().__init__()
        self.__position = [position[0], position[1]]
        self.__width = width
        self.__height = height
        self.__relative_bounds = [self.__position[0], self.__position[1], self.__width, self.__height]
        self.__global_bounds = [self.__position[0], self.__position[1], self.__width, self.__height]
        self.__cached_size = [self.__width, self.__height]
        self.__background = pygame.Color(90, 90, 90)
        self.__foreground = pygame.Color(190, 190,190)
        self.__border_color = pygame.Color(255, 255, 255)
        self.__border_width = 0
        self.__border_radius = -1

        self.__padding = [2, 2, 2, 2]
        self.__image = None
        self.__image_alignment = ImageAlignment.LEFT
        self.__text = ""
        self.__name = ""
        self.__font_size = 18
        self.__font_name = "Sagoe UI"
        self.__font = pygame.font.SysFont(self.__font_name, self.__font_size)
        self.__text_renderer = TextRenderer(self.__font_name, self.__font_size)
        self.__has_font_changed = True
        self._cached_rendered_text = None
        self.__child_elements = list()
        self.__parent = None
        self.__auto_size = False
        self.__text_align = TextAlignment.CENTER
        self.click_event = Event()

        UIElement.element_id += 1
        self.element_id = UIElement.element_id
        self.__name = f"UIElement{self.element_id}"
        UIManager.register_ui_element(self)

    @property
    def auto_size(self):
        return self.__auto_size

    @auto_size.setter
    def auto_size(self, value):
        self.__auto_size = value
        if self.__auto_size:
            self.__cached_size = [self.__width, self.__height]
            self.size = self.__calculate_size()
        else:
            self.size = self.__cached_size

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, value):
        self.__background = value

    @property
    def border_color(self):
        return self.__background

    @border_color.setter
    def border_color(self, value):
        self.__border_color = value

    @property
    def border_width(self):
        return self.__border_width

    @border_width.setter
    def border_width(self, value):
        self.__border_width = max(value, 0)

    @property
    def border_radius(self):
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value):
        self.__border_radius = max(value, 0)

    @property
    def global_bounds(self):
        return self.__global_bounds

    @global_bounds.setter
    def global_bounds(self, value):
        self.__position[0] = value[0]
        self.__position[1] = value[1]
        self.width = value[2]
        self.height = value[3]

    @property
    def child_elements(self):
        return self.__child_elements

    @property
    def font_size(self):
        return self.__font_size

    @font_size.setter
    def font_size(self, value: float):
        self.__font_size = value
        self.__has_font_changed = True
        self.__render_text()
        self.invalidate()

    @property
    def font_name(self):
        return self.__font_name

    @font_name.setter
    def font_name(self, value: str):
        self.__font_name = value
        self.__has_font_changed = True
        self.__render_text()
        self.invalidate()

    @property
    def font(self):
        return self.__font

    @property
    def foreground(self):
        return self.__foreground

    @foreground.setter
    def foreground(self, value):
        self.__foreground = value
        self.__has_font_changed = True
        self.invalidate()

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value
        self.invalidate()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def opacity(self):
        return UIManager.get_element_opacity(self.element_id)

    @opacity.setter
    def opacity(self, value):
        if value < 0 or (value - 0) < 0.001:
            value = 0
            self.is_visible = False
        else:
            self.is_visible = True
        UIManager.set_element_opacity(self.element_id, value)

    @property
    def padding(self):
        return self.__padding

    @padding.setter
    def padding(self, value):
        self.__padding = value

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        if value is None:
            return
        self.__parent = value
        self.__calculate_bounds()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position[0] = value[0]
        self.__position[1] = value[1]
        self.__relative_bounds[0] = value[0]
        self.__relative_bounds[1] = value[1]
        self.__calculate_bounds()

    @property
    def relative_bounds(self):
        return self.__relative_bounds

    @relative_bounds.setter
    def relative_bounds(self, value):
        self.__position[0] = value[0]
        self.__position[1] = value[1]
        self.width = value[2]
        self.height = value[3]
        self.__calculate_bounds()

    @property
    def size(self):
        return self.__width, self.__height

    @size.setter
    def size(self, value):
        self.__width = value[0]
        self.__height = value[1]
        self.__calculate_bounds()
        UIManager.set_element_size(self.element_id, self.size)

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        if value == self.__width:
            return
        self.__width = value
        self.__calculate_bounds()
        UIManager.set_element_size(self.element_id, (self.__width, self.__height))

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if value == self.__height:
            return
        self.__height = value
        self.__calculate_bounds()
        UIManager.set_element_size(self.element_id, (self.__width, self.__height))

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value
        self.__has_font_changed = True
        self.__render_text()
        self.invalidate()

    def draw(self, surface):
        rect = (0, 0, self.__width, self.__height)
        surface.fill(self.__background, rect)
        if self.__border_width > 0:
            pygame.draw.rect(surface, self.__border_color, rect, self.__border_width, self.__border_radius,
                             self.__border_radius,
                             self.__border_radius,
                             self.__border_radius)

        if self._cached_rendered_text is not None:
            surface.blit(self._cached_rendered_text,
                         self.__get_text_layout(self.__text_align, self._cached_rendered_text.get_size()))
        if self.image is not None:
            surface.blit(self.image,
                         self.__get_text_layout(self.__image_alignment, self.image.get_size()))

    def on_mouse_down(self, x, y):
        pass

    def on_mouse_move(self, x, y):
        pass

    def on_mouse_up(self, x, y):
        self.click_event(self, None)

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self):
        pass

    def update(self):
        pass

    def on_key_down(self, event_args: KeyEventArgs):
        pass

    def on_key_up(self, event_args):
        pass

    def add_child(self, ui_element):
        ui_element.parent = self
        self.__child_elements.append(ui_element)

    def invalidate(self):
        UIManager.invalidate_element(self)

    def has_font_changed(self):
        return self.__has_font_changed

    def hide(self):
        self.is_visible = False

    def show(self):
        self.is_visible = True

    def __calculate_size(self):
        size = [self.__padding[0] + self.__padding[2], self.__padding[1] + self.__padding[3]]
        if self.__image is not None:
            size[0] += self.__image.get_width()
            size[1] += self.__image.get_height()
        else:
            if len(self.text) > 0 and self._cached_rendered_text is not None:
                size[0] += self._cached_rendered_text.get_width()
                size[1] += self._cached_rendered_text.get_height()

        return size

    def __calculate_bounds(self):
        offset = [0, 0]
        if self.parent is not None:
            offset[0] = self.parent.position[0]
            offset[1] = self.parent.position[1]
        self.__global_bounds[0] = self.__position[0] + offset[0]
        self.__global_bounds[1] = self.__position[1] + offset[1]
        self.__relative_bounds[0] = self.__position[0]
        self.__relative_bounds[1] = self.__position[1]
        self.__global_bounds[2] = self.__relative_bounds[2] = self.__width
        self.__global_bounds[3] = self.__relative_bounds[3] = self.__height

    def __get_text_layout(self, text_alignment, size):
        rect = [0, 0, size[0], size[1]]
        if text_alignment == TextAlignment.CENTER:
            rect[0] = self.width // 2 - size[0] // 2
            rect[1] = self.height // 2 - size[1] // 2
        elif text_alignment == TextAlignment.LEFT:
            rect[1] = self.height // 2 - size[1] // 2
        elif text_alignment == TextAlignment.TOP:
            rect[0] = self.width // 2 - size[0] // 2
        elif text_alignment == TextAlignment.RIGHT:
            rect[0] = self.width - size[0]
            rect[1] = self.height // 2 - size[1] // 2
        elif text_alignment == TextAlignment.BOTTOM:
            rect[0] = self.width // 2 - size[0] // 2
            rect[1] = self.height - size[1]
        return rect

    def __render_text(self):
        if self.__has_font_changed:
            self.__font = pygame.font.SysFont(self.__font_name, self.__font_size)
            self.__text_renderer.change_font(self.__font_name, self.__font_size)
            y = 0
            for line in self.text.splitlines():
                y += self.__text_renderer.add_text((0, y), self.foreground, line)[1]

            self._cached_rendered_text = self.__text_renderer.get_surface()
            if self.auto_size:
                self.__calculate_size()
            self.__has_font_changed = False


class TextAlignment(Flag):
    LEFT, TOP, RIGHT, BOTTOM, CENTER = range(0, 5)


class ImageAlignment(Flag):
    LEFT, TOP, RIGHT, BOTTOM, CENTER = range(0, 5)

