from src.states import BaseState
from src import constants
import pygame

class PlayerFallingState(BaseState.BaseState):
    def __init__(self, player, gravity):
        self.player = player
        self.gravity = gravity

        # animation

    def enter(self, params):
        pass

    def exit(self):
        pass

    def render(self, surf, screen):
        pass

    def update(self, dt):
        # animation
        self.player.dy = self.player.dy + self.gravity
        self.player.y = self.player.y + self.player.dy * dt

        tileBottomLeft = self.player.map.pointToTile(self.player.x + 1, self.player.y + self.player.height)
        tileBottomRight = self.player.map.pointToTile(self.player.x + self.player.width - 1, self.player.y + self.player.height)

        if (tileBottomLeft and tileBottomRight) and (tileBottomLeft.collidable() or tileBottomRight.collidable()):
            self.player.dy = 0

            stateChanged = False
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.changeState('walking', {})
                        stateChanged = True

            if not stateChanged:
                self.player.changeState('idle', {})

        elif self.player.y > constants.VIRTUAL_HEIGHT:
            self.player.dead = True
            # sound

        else:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.direction = 'left'
                        self.player.x = self.player.x - constants.PLAYER_WALK_SPEED * dt
                        self.player.checkLeftCollisions(dt)
                    elif event.key == pygame.K_RIGHT:
                        self.player.direction = 'right'
                        self.player.x = self.player.x + constants.PLAYER_WALK_SPEED * dt
                        self.player.checkRightCollisions(dt)

        for object in self.player.level.objects:
            if object.collides(self.player):
                if object.solid:
                    self.player.dy = 0
                    selft.player.y = object.y - self.player.height

                    stateChanged = False
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                self.player.changeState('walking', {})
                                stateChanged = True
                    
                    if not stateChanged:
                        self.player.changeState('idle', {})
                elif object.consumable:
                    if object.onConsume(self.player, object):
                        del(self.player.level.objects[self.player.level.objects.index(object)])

        for entity in self.player.level.entities:
            if entity.collides(self.player):
                # sounds
                self.player.score = self.player.score + 100
                del(self.player.level.entities[self.player.level.entities.index(entity)])