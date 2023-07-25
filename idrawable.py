from abc import ABC, abstractmethod
 

class IDrawable(ABC):
    @abstractmethod
    def draw(self, surface):
        pass


