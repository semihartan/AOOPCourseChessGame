import random
from resourcemanager import ResourceManager


class SoundEffect:
    __move_piece_sounds = list()

    @classmethod
    def init(cls):
        for i in range(0, 6):
            cls.__move_piece_sounds.append(ResourceManager.get_resource("MOVEPIECE" + str(i + 1)))

    @classmethod
    def play_move_sound(cls):
        cls.__move_piece_sounds[random.randint(0, 5)].play()

    @classmethod
    def play_check_sound(cls):
        ResourceManager.get_resource("CHECK").play()

    @classmethod
    def play_checkmate_sound(cls):
        ResourceManager.get_resource("CHECKMATEWIN").play()

    @classmethod
    def play_piece_capture_sound(cls):
        ResourceManager.get_resource("CHESS_PIECETAKEN").play()