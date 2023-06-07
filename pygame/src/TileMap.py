
class TileMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []

    def pointToTile(self, x, y):
        if x < 0 or x > self.width * 16 or y < 0 or y > self.height * 16:
            return None

        return self.tiles[y // 16][x // 16]

    def render(self):
        pass