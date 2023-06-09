import pygame
from pygame.locals import *
from src import constants, Dependencies, StateMachine
from src.states.game import StartState, PlayState

class SuperBros:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT

    def on_init(self):
        pygame.init()
        Dependencies.loadAssets()

        self._state_machine = StateMachine.StateMachine({
            'start': lambda: StartState.StartState(),
            'play': lambda: PlayState.PlayState()
        })
        self._state_machine.change('start', {})

        self._display_screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf = pygame.Surface((constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT))
        pygame.display.set_caption('Super 50 Bros.')
        pygame.font.init()

        self.clock = pygame.time.Clock()

        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and self._state_machine.name == 'start':
                    self._state_machine.change('play', {
                        'levelWidth': 100,
                        'score': 0
                    })

    def on_loop(self):
        self._state_machine.update(self.clock.tick(60) / 1000)
        if self._state_machine.current.player and self._state_machine.current.player.dead:
            self._state_machine.change('start', {})

    def on_render(self):
        self._state_machine.render(self._display_surf, self._display_screen)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    game = SuperBros()
    game.on_execute()