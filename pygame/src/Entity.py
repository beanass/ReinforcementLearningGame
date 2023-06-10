from src import Dependencies
import pygame

class Entity:
    def __init__(self, x, y, width, height, texture, stateMachine, map, level):
        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0

        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.texture = texture
        self.stateMachine = stateMachine

        self.direction = 'left'

        self.map = map

        self.level = level

    def changeState(self, state, params):
        self.stateMachine.change(state, params)
   
    def update(self, dt):
        self.stateMachine.update(dt)

    def collides(self, entity):
        return not (self.x > entity.x + entity.width or entity.x > self.x + self.width or
                self.y > entity.y + entity.height or entity.y > self.y + self.height)
    
    def render(self, surf, screen):
        surf.blit(Dependencies.gFrames[self.texture][0], (self.x + 8, self.y + 10))


        