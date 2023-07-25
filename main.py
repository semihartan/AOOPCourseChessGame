from gameengine import *
from chessgame import ChessGame


def main():
    GameEngine.initialize()
    game = ChessGame()
    GameEngine.start()


something = {1, 2}
print(type(something))
if __name__ == '__main__':
    main()
