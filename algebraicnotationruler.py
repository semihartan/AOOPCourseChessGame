from chesssettings import ChessSettings
from gameobject import GameObject
from textrenderer import TextRenderer


class AlgebraicNotationRuler(GameObject):

    def __init__(self, chessboard):
        super().__init__()
        self.__chessboard = chessboard
        x, y = chessboard.position
        self.__position = (x - 10, y - 10)
        renderer = TextRenderer("Courier New", 14, True)
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        digits = ["1", "2", "3", "4", "5", "6", "7", "8"]
        for r in range(0, 8):
            x, y = r * ChessSettings.SQUARESIZE + 10, 5
            renderer.add_text((x, y), (185, 198, 198), letters[r])
        self.__horizontal_ruler = renderer.get_surface()
        renderer.clear()
        for r in range(0, 8):
            x, y = 5, r * ChessSettings.SQUARESIZE + 10
            renderer.add_text((x, y), (185, 198, 198), digits[7 - r])
        self.__vertical_ruler = renderer.get_surface()

        chessboard.set_position_changed_event_handler(self.__update_position_handler())

    def draw(self, surface):
        px, py = self.__chessboard.position
        surface.blit(self.__horizontal_ruler, (px, py - 25, self.__horizontal_ruler.get_width(), self.__horizontal_ruler.get_height()))
        surface.blit(self.__vertical_ruler, (px - 20, py, self.__vertical_ruler.get_width(), self.__vertical_ruler.get_height()))

    def render(self, surface):
        surface.blit(self.__horizontal_ruler,
                     (54, 32, self.__horizontal_ruler.get_width(), self.__horizontal_ruler.get_height()))
        surface.blit(self.__vertical_ruler,
                     (38, 50, self.__vertical_ruler.get_width(), self.__vertical_ruler.get_height()))

    def on_mouse_down(self, x, y):
        pass

    def on_mouse_move(self, x, y):
        pass

    def on_mouse_up(self, x, y):
        pass

    def update(self):
        pass

    def __update_position_handler(self):
        x, y = self.__chessboard.position
        self.__position = (x - 10, y - 10)