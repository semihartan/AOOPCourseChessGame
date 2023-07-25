from enum import Enum
import time
from event import Event

# Defines a time segment in the time line to animate a set of variables. It has a duration to determine
# how long it will take for the animation to complete and repeat count to provide a replay feature.
# A minus one (-1) of repeat value means that animaiton will long FOREVER.
class Animation:
    FOREVER = -1
    def __init__(self, duration, name="", repeat=1):
        self.__name = name
        self.__variables = []
        self.__duration = duration
        self.__duration_ns = duration * 1_000_000_000
        self.__time = 0.0
        self.__repeat = repeat
        self.__is_finished = False
        self.__is_playing = False
        self.finished_event = Event()
        self.animated_event = Event()

    def add_variable(self, variable):
        self.__variables.append(variable)

    def advance_time(self, delta_time):
        if not self.__is_playing:
            return
        self.__time += delta_time
        if self.__time >= self.__duration_ns:
            self.__time = 0.0

            self.__update_animation_variables(1.0)

            if self.__repeat != Animation.FOREVER:
                self.__repeat -= 1

            if self.__repeat == 0:
                self.__is_finished = True
                self.finished_event(self, None)
            else:
                self.__is_finished = False
            return
        t = self.__time / self.__duration_ns
        self.__update_animation_variables(t)

    @property
    def is_finished(self):
        return self.__is_finished

    @is_finished.setter
    def is_finished(self, value):
        self.__is_finished = value

    @property
    def is_playing(self):
        return self.__is_playing

    @is_playing.setter
    def is_playing(self, value):
        self.__is_playing = value

    def pause(self):
        self.__is_playing = False

    def play(self):
        self.__is_playing = True

    def stop(self):
        self.__is_playing = False
        self.reset(self.__repeat)

    def reset(self, repeat=None):
        if repeat is not None:
            self.set_repeat(repeat)
        self.__time = 0.0
        for variable in self.__variables:
            variable.reset();

    def set_repeat(self, repeat):
        self.__repeat = repeat
        if repeat > 0 or repeat == Animation.FOREVER:
            self.is_finished = False
        else:
            self.__is_finished = True

    def __update_animation_variables(self, t):
        for animation_variable in self.__variables:
            animation_variable.t = t
        self.animated_event(self, None)

    def __repr__(self):
        return f"Animation({self.__name}, {self.__duration})"