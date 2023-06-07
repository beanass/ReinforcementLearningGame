

class GameLevel:
    def __init__(self, entities, objects, tilemap):
        self.entities = entities
        self.objects = objects
        self.tilemap = tilemap

    def clear(self):
        for i in range(len(self.objects), 0, -1):
            del self.objects[i]

        for i in range(len(self.entities), 0, -1):
            del self.entities[i]

    def update(self, dt):
        self.tilemap.update(dt)

        for object in self.objects:
            object.update(dt)

        for entity in self.entities:
            entity.update(dt)

    def render(self, surf, screen):
        self.tilemap.render(surf, screen)

        for object in self.objects:
            object.render(surf, screen)

        for entity in self.entities:
            entity.render(surf, screen)