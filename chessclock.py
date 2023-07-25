import time
import datetime

from resourcemanager import ResourceManager
from textrenderer import TextRenderer
from gameobject import GameObject


class ChessClock(GameObject):

    def __init__(self, minutes=10, seconds=0):
        super(ChessClock, self).__init__()
        self.__left_start_time = None
        self.__right_start_time = None
        self.__left_current_time = None
        self.__right_current_time = None
        self.position = [600, 350]
        self.__clock_image = ResourceManager.get_resource("clock")
        self.__clock_switch_left_image = ResourceManager.get_resource("ClockSwitchLeft")
        self.__clock_switch_right_image = ResourceManager.get_resource("ClockSwitchRight")
        self.__is_running = False
        self.__is_left = False
        self.__has_left_started = False
        self.__has_right_started = False
        self.__total_time = datetime.timedelta(seconds=minutes*60 + seconds)
        self.__left_clock_string = self.__right_clock_string = self.__get_clock_string(self.__total_time)
        self.__diff = None
        self.__text_renderer = TextRenderer("Sagoe UI", 21, bold=True)
        self.__timesup_event = None

    def draw(self, surface):
        if self.__is_running:
            if self.__is_left:
                self.__left_current_time = datetime.datetime.now()
                self.__diff = self.__left_current_time - self.__left_start_time
                if self.__diff.total_seconds() >= self.__total_time.total_seconds():
                    self.__right_clock_string = "00:00"
                    if self.__timesup_event is not None:
                        self.__timesup_event(self.__is_left)
                    self.stop()
                else:
                    delta = (self.__total_time - self.__diff)
                    self.__left_clock_string = self.__get_clock_string(delta)
            else:
                self.__right_current_time = datetime.datetime.now()
                self.__diff = self.__right_current_time - self.__right_start_time
                if self.__diff.total_seconds() >= self.__total_time.total_seconds():
                    self.__right_clock_string = "00:00"
                    if self.__timesup_event is not None:
                        self.__timesup_event(self.__is_left)
                        self.stop()
                else:
                    delta = (self.__total_time - self.__diff)
                    self.__right_clock_string = self.__get_clock_string(delta)

        px, py = self.position
        sx, sy = self.__clock_switch_left_image.get_width(), self.__clock_switch_left_image.get_height()
        if self.__is_left:
            surface.blit(self.__clock_switch_left_image, (px + 12, py - 18, sx, sy))
        else:
            sx, sy = self.__clock_switch_right_image.get_width(), self.__clock_switch_right_image.get_height()
            surface.blit(self.__clock_switch_right_image, (px + 12, py - 18, sx, sy))
        sx, sy = self.__clock_image.get_width(), self.__clock_image.get_height()
        surface.blit(self.__clock_image, (px - 10, py - 8, sx, sy))
        TextRenderer.draw(surface, (36, 36, 36), (px + 25, py + 26), self.__left_clock_string, "Quartz MS", 34)
        TextRenderer.draw(surface, (36, 36, 36), (px + 94 + 68, py + 26), self.__right_clock_string, "Quartz MS", 34)

    def on_mouse_down(self, x, y):
        pass

    def on_mouse_move(self, x, y):
        pass

    def on_mouse_up(self, x, y):
        pass

    def update(self):
        pass

    @property
    def timesup_event(self):
        return self.__timesup_event

    @timesup_event.setter
    def timesup_event(self, value):
        self.__timesup_event = value

    def reset(self):
        self.__is_running = False
        self.__is_left = False
        self.__left_clock_string = self.__right_clock_string = "10:00"
        self.__has_left_started = self.__has_right_started = False
        self.__right_start_time = self.__left_start_time = 0

    def restart(self):
        self.reset()
        self.start()

    def start(self):
        self.__is_running = True
        if self.__is_left:
            if not self.__has_left_started:
                self.__left_start_time = datetime.datetime.now()
                self.__has_left_started = True
        else:
            if not self.__has_right_started:
                self.__right_start_time = datetime.datetime.now()
                self.__has_right_started = True


    def stop(self):
        self.__is_running = False

    def switch(self):
        self.__is_left = not self.__is_left
        if self.__is_left:
            if not self.__has_left_started:
                self.__left_start_time = datetime.datetime.now()
                self.__has_left_started = True
        else:
            if not self.__has_right_started:
                self.__right_start_time = datetime.datetime.now()
                self.__has_right_started = True

    def __get_clock_string(self, delta):
        minutes, seconds = divmod(int(delta.total_seconds()), 60)
        return f"{minutes:02}:{seconds:02}"
