from src.states import BaseState
from src import constants
import pygame

class PlayerWalkingState(BaseState.BaseState):
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
        # animation

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.walking = False

        if not self.player.walking:
            self.player.changeState('idle', {})
        else:
            tileBottomLeft = self.player.map.pointToTile(self.player.x + 1, self.player.y + self.player.height)
            tileBottomRight = self.player.map.pointToTile(self.player.x + self.player.width - 1, self.player.y + self.player.height)


            self.player.y = self.player.y + 1

            collidedObjects = self.player.checkObjectCollisions()

            self.player.y = self.player.y - 1

            if len(collidedObjects) == 0 and (tileBottomLeft and tileBottomRight) and (not tileBottomLeft.collidable() and not tileBottomRight.collidable()):
                self.player.dy = 0
                self.player.changeState('falling', {})
            else:
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

        for entity in self.player.level.entities:
            if entity.collides(self.player):
                self.player.dead = True
                # sound

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.changeState('jump', {})


