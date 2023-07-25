import math


# Defines a set of built-in interpolation functions to animate animation variables.
class InterpolationFunction:
    @staticmethod
    def linear(t):
        return t

    @staticmethod
    def quadratic(t):
        return t ** 2

    @staticmethod
    def qubic(t):
        return t ** 3

    @staticmethod
    def sin(t):
        return math.sin(t * math.pi)

    @staticmethod
    def smooth_step(t):
        if t < 0.0:
            t = 0.0
        elif t > 1.0:
            t = 1.0
        else:
            t = t * t * (3 - 2 * t)
        return t
