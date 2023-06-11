from src import GameLevel, constants, TileMap, Tile
import random

class LevelMaker:
    def __init__(self):
        pass

    def generate(self, width, height):
        tiles = []
        entities = []
        objects = []
        keyX = random.randint(2, width//2)
        lockX = random.randint(width//2 + 2, width - 10)
        lockColor = random.randint(1, 4)

        tileID = constants.TILE_ID_GROUND

        topper = True
        tileset = random.randint(1, 20)
        topperset = random.randint(1, 20)

        for y in range(height):
            tiles.append([])

        for x in range(width):
            tileID = constants.TILE_ID_EMPTY

            for y in range(7):
                tiles[y].append(Tile.Tile(x*16, y*16, tileID, None, tileset, topperset))

            if random.randint(1, 7) == 1 and x != keyX and x != lockX:
                for y in range(7, height):
                    tiles[y].append(Tile.Tile(x*16, y*16, tileID, None, tileset, topperset))
            else:
                tileID = constants.TILE_ID_GROUND

                blockHeight = 3
                highestBlock = 6

                for y in range(7, height):
                    tiles[y].append(Tile.Tile(x*16, y*16, tileID, y == 7 and topper or None, tileset, topperset))

                if random.randint(1, 8) == 1:
                    blockHeight = 3
                    highestBlock = 6

                    tiles[5][x] = Tile.Tile(x*16, 5*16, tileID, topper, tileset, topperset)
                    tiles[6][x] = Tile.Tile(x*16, 6*16, tileID, None, tileset, topperset)
                    tiles[7][x].topper = None

                if x == keyX:
                    # insert key
                    b = 1

                if x == lockX:
                    # insert lock
                    b = 1

                if random.randint(1, 10) == 1:
                    # spawn block
                    b = 1

        map = TileMap.TileMap(width, height)
        map.tiles = tiles

        return GameLevel.GameLevel(entities, objects, map)

        def spawnFlagpole(self, width, objects, x, y):
            pass
