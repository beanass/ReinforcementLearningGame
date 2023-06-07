class StateMachine:
    def __init__(self, states):
        self.empty = {
            'render': lambda: None,
            'update': lambda: None,
            'enter': lambda: None,
            'exit': lambda: None
        }
        self.states = states or {}
        self.current = self.empty
        self.name = ""

    def change(self, stateName, enterParams):
        assert self.states[stateName]
        self.current['exit']()
        self.current = self.states[stateName]()
        self.current.enter(enterParams)
        self.name = stateName

    def update(self, dt):
        self.current.update(dt)

    def render(self, surf, screen):
        self.current.render(surf, screen)