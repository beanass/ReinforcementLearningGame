from src import constants

class Tile:
    def __init__(self, x, y, id, topper, tileset, topperset):
        self.x = x
        self.y = y

        self.width = 16
        self.height = 16

        self.id = id
        self.tileset = tileset
        self.topper = topper
        self.topperset = topperset

    def collidable(self, target):
        for v in constants.COLLIDABLE_TILES.items():
            if self.id == v:
                return True

        return False

    def render(self):
        pass