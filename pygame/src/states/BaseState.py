from abc import ABC, abstractmethod

class BaseState(ABC):
    @abstractmethod
    def enter(self, params):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self, surf, screen):
        pass