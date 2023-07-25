from interpolationtype import InterpolationType
from interpolationfunction import InterpolationFunction


# An animation variable is just a simple encapsulation of the data required to animate a value.
# This data include a start value, an end value, a t value ranging from 0.0 to 1.0, and an interpolation
# type and function. The animation class sets the t value and then the users gets the interpolated
# value of the variable. Using both built-in functions and your custom functions, you can achieve a wide
# variety of animation and transition effects.
class AnimationVariable:
    def __init__(self, start=0, end=0, interpolation_type=InterpolationType.SmoothStep, func=None):
        self.__start = start
        self.__end = end
        self.__t = 0.0
        self.__interpolation_type = interpolation_type
        self.__func = func
        if self.__interpolation_type == InterpolationType.Custom:
            if func is None:
                raise ValueError(func)

        self.__value_changed_event = None

    # Returns the interpolated value.
    @property
    def value(self):
        function = self.__get_interpolation_function()
        return self.__start + (self.__end - self.__start) * function(self.__t)

    # Gets the current t value.
    @property
    def t(self):
        return self.__t

    # Sets the current t value.
    @t.setter
    def t(self, value):
        # Clamp the t value into the range [0.0-1.0]
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0
        self.__t = value
        if self.__value_changed_event is not None:
            self.__value_changed_event(self.__t)

    # Gets the start value.
    @property
    def start(self):
        return self.__start

    # Sets the start value.
    @start.setter
    def start(self, start):
        self.__start = start

    # Gets the end value.
    @property
    def end(self):
        return self.__end

    # Sets the end value.
    @end.setter
    def end(self, end):
        self.__end = end

    # Resets the animation variable. This is required when the container animation of this variable
    # is replayed.
    def reset(self):
        self.__t = 0.0

    @property
    def value_changed_event(self):
        return self.__value_changed_event

    @value_changed_event.setter
    def value_changed_event(self, value):
        self.__value_changed_event = value

    def __get_interpolation_function(self):
        if self.__interpolation_type == InterpolationType.Linear:
            return InterpolationFunction.linear
        elif self.__interpolation_type == InterpolationType.Quadratic:
            return InterpolationFunction.quadratic
        elif self.__interpolation_type == InterpolationType.Cubic:
            return InterpolationFunction.qubic
        elif self.__interpolation_type == InterpolationType.SmoothStep:
            return InterpolationFunction.smooth_step
        elif self.__interpolation_type == InterpolationType.Sin:
            return InterpolationFunction.sin
        elif self.__interpolation_type == InterpolationType.Custom:
            return self.__func
