import pygame
from resourcemanager import ResourceManager
from animationengine import AnimationEngine
from ui.uimanager import UIManager


# A simple class to encapsulate a basic game engine. It has several important responsibilities such as
# initializing resource manager, maintaining a list of GameObject instance, updating the game, drawing
# the game objects by calling their draw methods and so forth.
class GameEngine:
    __screen_surface = None
    __gameobjects = []
    __clock = pygame.time.Clock()
    __icon = None

    @classmethod
    def initialize(cls):

        # Initialize pygame.
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()
        # Initialize the resource manager.
        ResourceManager.load("resources")

        pygame.display.set_caption("AOOP Project: Design Chess")

        cls.__icon = ResourceManager.get_resource("chess-icon")
        pygame.display.set_icon(cls.__icon)
        # Get the display surface, the changes to this surface will be reflected to the display device, in our case,
        # it is the monitor. We try to enable the vsync, but it may fail.
        cls.__screen_surface = pygame.display.set_mode((900, 700), vsync=True)

        UIManager.init(cls.__screen_surface)
    # Adds a game object to the engine.
    @classmethod
    def add_game_object(cls, game_object):
        if game_object.render_priority == -1:
            if len(cls.__gameobjects) > 0:
                game_object.render_priority = cls.__get_lowest_priority()
        cls.__gameobjects.append(game_object)
        # Sort the game object list to respect their render priorities. We use a custom sort criteria.
        cls.__gameobjects.sort(key=cls.__sort_criteria)
        return game_object

    # Removes a game object from the engine.
    @classmethod
    def remove_game_object(cls, game_object):
        cls.__gameobjects.remove(game_object)

    # Starts the engine. This involves starting a game loop that updates .
    @classmethod
    def start(cls):
        running = True
        while running:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                # process the mouse events and forward them to the enabled game objects.
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for go in cls.__gameobjects:
                        if go.is_enabled:
                            if go.on_mouse_down(mousepos[0], mousepos[1]):
                                break
                elif event.type == pygame.MOUSEMOTION:
                    for go in cls.__gameobjects:
                        if go.is_enabled:
                            go.on_mouse_move(mousepos[0], mousepos[1])
                elif event.type == pygame.MOUSEBUTTONUP:
                    for go in cls.__gameobjects:
                        if go.is_enabled:
                            go.on_mouse_up(mousepos[0], mousepos[1])
                UIManager.handle_mouse_events(event)
            # Update the Animation Engine.
            AnimationEngine.update()
            # Allow for the game objects to update themselves.
            cls.__update_game_objects()
            # Draw the game objects.
            cls.__draw_game_objects()

            UIManager.update()
            # This function swaps back and front buffers internally.
            pygame.display.flip()
            # Limit the fps. This doesn't set the fps to 60 fps exactly, but it will be close to that.
            # That is enough.
            cls.__clock.tick(60)

    # Draws the game objects by sorting them according to their render priorities.
    @classmethod
    def __draw_game_objects(cls):
        surface = cls.__screen_surface
        # Clear the surface with white.
        surface.fill((255, 255, 255))

        for game_object in cls.__gameobjects:
            # Draw if the object is visible.
            if game_object.is_visible:
                game_object.draw(surface)

    @classmethod
    def __update_game_objects(cls):
        for game_object in cls.__gameobjects:
            # Draw if the object is visible.
            game_object.update()

    @staticmethod
    def __sort_criteria(item):
        return item.render_priority

    @classmethod
    def __get_lowest_priority(cls):
        maximum = 0
        for game_object in cls.__gameobjects:
            # Draw if the object is visible.
            if game_object.render_priority > maximum:
                maximum = game_object.render_priority
        return maximum