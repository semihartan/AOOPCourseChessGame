import pygame
import os
from pathlib import *


# Provide a mechanism to load the resources automatically from the specified path, by using only resource
# names to access them.
class ResourceManager:
    __resources = dict()
    __resource_Directory = ""

    # Gets the root resource directory and build a full path from it using the executable path of the current script.
    @classmethod
    def load(cls, root_resource_dir):
        cls.__resource_Directory = WindowsPath(__file__).parent.joinpath(root_resource_dir)
        cls.__load_images()
        cls.__load_sounds()

    # Loads the images from the subdirectory 'image'.
    @classmethod
    def __load_images(cls):
        images_directory = Path(cls.__resource_Directory).joinpath("images")
        image_files = os.listdir(images_directory)
        for image_file in image_files:
            path = images_directory.joinpath(image_file)
            # Add the image to the dict as key-value pair using its file name without extension
            # as key and the surface as value.
            cls.__resources[path.stem] = pygame.image.load(str(path))

    @classmethod
    def __load_sounds(cls):
        sounds_directory = Path(cls.__resource_Directory).joinpath("sounds")
        sounds_files = os.listdir(sounds_directory)
        for sound_file in sounds_files:
            path = sounds_directory.joinpath(sound_file)
            # Add the sound file to the dict as key-value pair using its file name without extension
            # as key and the surface as value.
            cls.__resources[path.stem] = pygame.mixer.Sound(str(path))

    # Retrieves the specified resource, if possible, cloning it.
    @classmethod
    def get_resource(cls, name):
        resource = cls.__resources[name]
        if isinstance(resource, pygame.surface.Surface):
            return resource.copy()
        return resource

