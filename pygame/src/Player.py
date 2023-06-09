from src import Entity, constants

class Player(Entity.Entity):
    def __init__(self, x, y, width, height, texture, stateMachine, map, level):
        super().__init__(x, y, width, height, texture, stateMachine, map, level)

        self.score = 0
        self.key = 0
        self.consumingKey = False
        self.dead = False
        self.walking = False

    def update(self, dt):
        print(self.stateMachine.name)
        super().update(dt)

    def render(self, surf, screen):
        super().render(surf, screen)

    def checkLeftCollisions(self, dt):
        tileTopLeft = self.map.pointToTile(self.x + 1, self.y + 1)
        tileBottomLeft = self.map.pointToTile(self.x + 1, self.y + self.height - 1)

        if (tileTopLeft and tileBottomLeft) and (tileTopLeft.collidable() or tileBottomLeft.collidable()):
            self.x = (tileTopLeft.x - 1) * 16 + tileTopLeft.width - 1
        else:
            self.y = self.y - 1
            collidedObjects = self.checkObjectCollisions()
            self.y = self.y + 1

            if len(collidedObjects) > 0:
                self.x = self.x + constants.PLAYER_WALK_SPEED * dt

    def checkRightCollisions(self, dt):
        tileTopRight = self.map.pointToTile(self.x + self.width - 1, self.y + 1)
        tileBottomRight = self.map.pointToTile(self.x + self.width - 1, self.y + self.height - 1)

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