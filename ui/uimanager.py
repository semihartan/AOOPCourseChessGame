import pygame

from hittest import HitTest
from ui.redirectionsurface import RedirectionSurface


class UIManager:
    __ui_elements = list()
    __redirection_surfaces = list()
    __display_surface = None
    __composition_surface = None
    __mouse_enter_leave_tracking_flags = list()

    @classmethod
    def init(cls, display_surface):
        cls.__display_surface = display_surface
        cls.__composition_surface = pygame.Surface((cls.__display_surface.get_width(),
                                                    cls.__display_surface.get_height()),
                                                   flags=pygame.SRCALPHA)
        cls.__composition_surface.fill((0, 0, 0, 0), cls.__composition_surface.get_rect())

    @classmethod
    def register_ui_element(cls, ui_element):
        internal_surface = pygame.Surface((ui_element.width, ui_element.height), flags=pygame.SRCALPHA)
        cls.__redirection_surfaces.append(RedirectionSurface(ui_element.element_id, internal_surface))
        cls.__ui_elements.append(ui_element)
        cls.__mouse_enter_leave_tracking_flags.append([ui_element.element_id, False])

    @classmethod
    def handle_mouse_events(cls, event):
        for ui_element in cls.__ui_elements:
            mousepos = pygame.mouse.get_pos()
            if ui_element.parent is not None:
                if not ui_element.parent.is_visible or not ui_element.parent.is_enabled:
                    return
            if not ui_element.is_visible or not ui_element.is_enabled:
                return

            mouse_offset_position = mousepos[0] - ui_element.position[0], mousepos[1] - ui_element.position[1]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HitTest.is_point_in_rectangle(mousepos, ui_element.global_bounds):
                    ui_element.on_mouse_down(mouse_offset_position[0], mouse_offset_position[1])
            elif event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
                if HitTest.is_point_in_rectangle(mousepos, ui_element.global_bounds):
                    ui_element.on_mouse_move(mouse_offset_position[0], mouse_offset_position[1])
                    for flag in cls.__mouse_enter_leave_tracking_flags:
                        if flag[0] == ui_element.element_id:
                            if not flag[1]:
                                flag[1] = True
                                ui_element.on_mouse_enter()
                else:
                    for flag in cls.__mouse_enter_leave_tracking_flags:
                        if flag[0] == ui_element.element_id:
                            if flag[1]:
                                flag[1] = False
                                ui_element.on_mouse_leave()
            elif event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
                if HitTest.is_point_in_rectangle(mousepos, ui_element.global_bounds):
                    ui_element.on_mouse_up(mouse_offset_position[0], mouse_offset_position[1])

    @classmethod
    def update(cls):
        cls.__composition_surface.fill((0, 0, 0, 0), cls.__composition_surface.get_rect())
        for redirection_surface in cls.__redirection_surfaces:
            if redirection_surface.needs_redraw:
                ui_element = cls.get_element_from_id(redirection_surface.element_id)
                if not ui_element.is_visible:
                    continue
                ui_element.draw(redirection_surface.internal_surface)
                if len(ui_element.child_elements) > 0:
                    parent_redirection_surface = cls.get_redirection_surface(ui_element.element_id)
                    for child in ui_element.child_elements:
                        child_redirection_surface = cls.get_redirection_surface(child.element_id)
                        parent_redirection_surface.internal_surface.blit(child_redirection_surface.internal_surface,
                                                                         child.relative_bounds)
                if ui_element.parent is None:
                    cls.__composition_surface.blit(redirection_surface.internal_surface, ui_element.relative_bounds)

        cls.__display_surface.blit(cls.__composition_surface, cls.__composition_surface.get_rect())

    @classmethod
    def invalidate_element(cls, ui_element):
        for redirection_surface in cls.__redirection_surfaces:
            if redirection_surface.element_id == ui_element.element_id:
                redirection_surface.needs_redraw = True
                break

    @classmethod
    def get_element_from_id(cls, id):
        for ui_element in cls.__ui_elements:
            if ui_element.element_id == id:
                return ui_element

    @classmethod
    def set_element_size(cls, element_id, size):
        redirection_surface = cls.get_redirection_surface(element_id)
        if redirection_surface.size[0] != size[0] or redirection_surface.size[1] != size[1]:
            redirection_surface.internal_surface = pygame.Surface(size, flags=pygame.SRCALPHA)

    @classmethod
    def get_element_opacity(cls, element_id):
        redirection_surface = cls.get_redirection_surface(element_id)
        return redirection_surface.internal_surface.get_alpha()

    @classmethod
    def set_element_opacity(cls, element_id, opacity):
        redirection_surface = cls.get_redirection_surface(element_id)
        redirection_surface.internal_surface.set_alpha(opacity)

    @classmethod
    def get_redirection_surface(cls, element_id):
        for redirection_surface in cls.__redirection_surfaces:
            if redirection_surface.element_id == element_id:
                return redirection_surface