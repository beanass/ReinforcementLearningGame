
class TileMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []

    def pointToTile(self, x, y):
        if x < 0 or x > self.width * 16 or y < 0 or y > self.height * 16:
            return None

        return self.tiles[int(y // 16)][int(x // 16)]

    def update(self, dt):
        pass

    def render(self, surf, screen):
        for row in self.tiles:
            for tile in row:
                tile.render(surf, screen)