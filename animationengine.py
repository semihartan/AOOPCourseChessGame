import time


# One core components of the game. It executes all the animations. This consist of calculation of
# the timing and updating the list of animations. This class was meant to be a static class like
# game engine class.
class AnimationEngine:
    __animations = list()
    __current_time: int = 0
    __last_time: int = 0

    @classmethod
    def init(cls):
        # Initialize the timing variables.
        cls.__current_time = 0
        cls.__last_time = 0

    # Adds an animation to the engine and returns the animation.
    @classmethod
    def add_animation(cls, animation):
        # Don't add the animation if the animation already exists.
        if cls.__animations.count(animation) > 0:
            return
        cls.__animations.append(animation)
        return animation

    @classmethod
    def update(cls):
        if len(cls.__animations) == 0:
            return
        # Get the current performance counter tick count in nanoseconds.
        cls.__current_time = time.perf_counter_ns()
        # If we are in the start of the first update, don't calculate the delta because the __last_time is zero.
        if cls.__last_time != 0:
            # Calculate the delta.
            delta_time = (cls.__current_time - cls.__last_time)
            # This variable may be removed in the future.
            animations = list()

            # Traverse the list and advance the time of the animations.
            for animation in cls.__animations:
                animation.advance_time(delta_time)
            # Traverse the animations again and add the finished animations to a new list.
            for animation in cls.__animations:
                if animation.is_finished:
                    continue
                animations.append(animation)
            # Delete the previous list and assign the new one to __animations.
            del cls.__animations
            cls.__animations = animations
        # Cache the last time before exiting the update loop.
        cls.__last_time = cls.__current_time
