class HitTest:

    @classmethod
    def is_point_in_rectangle(cls, point, rectangle):
        px, py = point
        x, y, w, h = rectangle
        if x <= px <= x + w and y <= py <= y + h:
            return True
        return False
