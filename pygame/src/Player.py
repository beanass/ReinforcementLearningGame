from src import Entity, constants
import pygame

class Player(Entity.Entity):
    def __init__(self, x, y, width, height, texture, stateMachine, map, level):
        super().__init__(x, y, width, height, texture, stateMachine, map, level)

        self.score = 0
        self.key = 0
        self.consumingKey = False
        self.dead = False
        self.walking = False
        self.surf = None
        self.screen = None

    def update(self, dt):
        super().update(dt)

    def render(self, surf, screen):
        self.surf = surf
        self.screen = screen
        super().render(surf, screen)    

    def checkTopCollisions(self, dt):
        collide = False
        for x in range(self.x, self.x + self.width, 16):
            for y in range(0, constants.VIRTUAL_HEIGHT, 16):
                tile = self.map.pointToTile(x, y)
                if tile and tile.collidable():
                    collide = self.rect.colliderect(tile.rect)
                    if collide:
                        self.y = (tile.y + 1) * 16
                        self.dy = 0
                        break

    def checkBottomCollisions(self, dt):
        collide = False
        for x in range(self.x, self.x + self.width, 16):
            for y in range(0, constants.VIRTUAL_HEIGHT, 16):
                tile = self.map.pointToTile(x, y)
                if tile and tile.collidable():
                    collide = self.rect.colliderect(tile.rect)
                    if self.surf:
                        pygame.draw.rect(self.surf, (255, 0, 0), (x, y, 16, 16))
                    if collide:
                        self.y = (tile.y - 1) * 16 - self.height
                        self.dy = 0
                        break

    def checkLeftCollisions(self, dt):
        tileTopLeft = self.map.pointToTile(self.x - 1, self.y - 1)
        tileBottomLeft = self.map.pointToTile(self.x - 1, self.y + self.height + 1)

        if (tileTopLeft and tileBottomLeft) and (tileTopLeft.collidable() or tileBottomLeft.collidable()):
            self.x = (tileTopLeft.x - 1) * 16 + tileTopLeft.width - 1
        else:
            self.y = self.y - 1
            collidedObjects = self.checkObjectCollisions()
            self.y = self.y + 1

            if len(collidedObjects) > 0:
                self.x = self.x + constants.PLAYER_WALK_SPEED * dt

    def checkRightCollisions(self, dt):
        tileTopRight = self.map.pointToTile(self.x + self.width + 1, self.y - 1)
        tileBottomRight = self.map.pointToTile(self.x + self.width + 1, self.y + self.height + 1)

        if (tileTopRight and tileBottomRight) and (tileTopRight.collidable() or tileBottomRight.collidable()):
            self.x = (tileTopRight.x - 1) * 16 - self.width
        else:
            self.y = self.y - 1
            collidedObjects = self.checkObjectCollisions()
            self.y = self.y + 1

            if len(collidedObjects) > 0:
                self.x = self.x - constants.PLAYER_WALK_SPEED * dt

    def checkObjectCollisions(self):
        collidedObjects = []

        for object in self.level.objects:
            if object.collides(self):
                collidedObjects.append(object)
            elif object.consumable:
                if object.onConsume(self, object):
                    del(self.level.objects[self.level.objects.index(object)])

        return collidedObjects