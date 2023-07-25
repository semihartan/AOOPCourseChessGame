from enum import Enum

class InterpolationType(Enum):
    Linear = 0
    Quadratic = 1
    Cubic = 2
    SmoothStep = 3
    Sin = 4
    Custom = 5