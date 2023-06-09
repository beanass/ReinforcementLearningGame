from src.states import BaseState
import pygame

class PlayerIdleState(BaseState.BaseState):
    def __init__(self, player):
        self.player = player

        # animation

    def enter(self, params):
        pass

    def exit(self):
        pass

    def render(self, surf, screen):
        pass

    def update(self, dt):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.walking = True
                if event.key == pygame.K_UP:
                    self.player.changeState('jump', {})
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.walking = False

        if self.player.walking:
            self.player.changeState('walking', {})

                # collision and dying
        for entity in self.player.level.entities:
            if entity.collides(self.player):
                self.player.dead = True
                