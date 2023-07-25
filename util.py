

class Util:
    @classmethod
    def convert_coordinates_to_position(cls, x, y):
        return

    @staticmethod
    def clamp(value, minimum, maximum):
        if value < minimum:
            return minimum
        elif value > maximum:
            return maximum
        else:
            return value
