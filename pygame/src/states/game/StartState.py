from src import LevelMaker, constants, Dependencies
from src.states import BaseState
import random
import pygame

class StartState(BaseState.BaseState):
    def __init__(self):
        self.map = LevelMaker.LevelMaker().generate(100, 10)
        self.background = random.randint(0, 2)
        self.player = None

    def enter(self, params):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def render(self, surf, screen):
        surf.blit(Dependencies.gFrames["backgrounds"][self.background], (0, 0))
        surf.blit(Dependencies.gFrames["backgrounds"][self.background], (0, Dependencies.gFrames["backgrounds"][self.background].get_height() / 3 * 2))
        self.map.render(surf, screen)
        text_surface = Dependencies.gFonts["title"].render('Super 50 Bros.', True, (0, 0, 0))
        surf.blit(text_surface, (constants.VIRTUAL_WIDTH / 2 - text_surface.get_width() / 2, constants.VIRTUAL_HEIGHT / 2 - 40 + 1))
        text_surface = Dependencies.gFonts["title"].render('Super 50 Bros.', True, (255, 255, 255))
        surf.blit(text_surface, (constants.VIRTUAL_WIDTH / 2 - text_surface.get_width() / 2, constants.VIRTUAL_HEIGHT / 2 - 40))
        text_surface = Dependencies.gFonts["medium"].render('Press Enter', True, (255, 255, 255))
        surf.blit(text_surface, (constants.VIRTUAL_WIDTH / 2 - text_surface.get_width() / 2, constants.VIRTUAL_HEIGHT / 2 + 20))

        screen.blit(pygame.transform.scale(surf, (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)), (0, 0))

        pygame.display.update()