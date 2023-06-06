import pygame
from pygame.locals import *
from src import constants, Dependencies

class SuperBros:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT

    def on_init(self):
        pygame.init()
        self._display_screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf = pygame.Surface((constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT))
        pygame.display.set_caption('Super 50 Bros.')
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.blit(Dependencies.gFrames["backgrounds"][0], (0, 0))
        self._display_screen.blit(pygame.transform.scale(self._display_surf, self.size), (0, 0))
        
        pygame.display.update()
        pass

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