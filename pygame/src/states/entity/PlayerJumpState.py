from src.states import BaseState
from src import constants
import pygame

class PlayerJumpState(BaseState.BaseState):
    def __init__(self, player, gravity):
        self.player = player
        self.gravity = gravity

        # animation

    def enter(self, params):
        # sound
        self.player.dy = constants.PLAYER_JUMP_VELOCITY

    def exit(self):
        pass

    def render(self, surf, screen):
        pass

    def update(self, dt):
        # animation
        self.player.dy = self.player.dy + self.gravity
        self.player.y = self.player.y + self.player.dy * dt

        if self.player.dy >= 0:
            self.player.changeState('falling', {})

        #self.player.y = self.player.y + self.player.dy * dt

        tileLeft = self.player.map.pointToTile(self.player.x + 2, self.player.y)
        tileRight = self.player.map.pointToTile(self.player.x + self.player.width - 2, self.player.y)

        if (tileLeft and tileRight) and (tileLeft.collidable() or tileRight.collidable()):
            self.player.dy = 0
            self.player.changeState('falling', {})

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
                    object.onCollide(object)

                    self.player.y = object.y - object.height
                    self.player.dy = 0
                    self.player.changeState('falling', {})
                elif object.consumable:
                    if object.onConsume(self.player, object):
                        del(self.player.level.objects[self.player.level.objects.index(object)])

        for entity in self.player.level.entities:
            if entity.collides(self.player):
                self.player.dead = True
                # sound