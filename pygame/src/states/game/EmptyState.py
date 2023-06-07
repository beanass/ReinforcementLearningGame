from src.states import BaseState

class EmptyState(BaseState.BaseState):
    def __init__(self):
        pass

    def enter(self, params):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def render(self, surf, screen):
        pass