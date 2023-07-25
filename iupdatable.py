from abc import ABC, abstractmethod


# Provides a functionality to update the state of an object.
class IUpdatable(ABC):
    # Update the object state. This can be anything.
    @abstractmethod
    def update(self):
        pass
