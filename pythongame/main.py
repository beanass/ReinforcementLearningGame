import pygame
from pygame.locals import *
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

VIRTUAL_WIDTH = 256
VIRTUAL_HEIGHT = 144

PLAYER_WALK_SPEED = 60 #100
PLAYER_JUMP_VELOCITY = -225

SNAIL_MOVE_SPEED = 10

TILE_ID_EMPTY = 4
TILE_ID_GROUND = 2

GRAVITY = 8

pygame.init()

def generateSubsurfaces(spritesheet, width, height):
    sheetWidth = spritesheet.get_width() // width
    sheetHeight = spritesheet.get_height() // height

    sheetCounter = 0
    subsurfaces = []

    for y in range(sheetHeight):
        for x in range(sheetWidth):
            subsurfaces.append(spritesheet.subsurface(pygame.Rect(x * width, y * height, width, height)))
            sheetCounter += 1

    return subsurfaces

def generateTileSets(tiles, setsX, setsY, sizeX, sizeY):
    tilesets = []
    tableCounter = -1
    sheetWidth = setsX * sizeX
    sheetHeight = setsY * sizeY

    for tilesetY in range(setsY):
        for tilesetX in range(setsX):
            tilesets.append([])
            tableCounter += 1
            
            for y in range(sizeY * (tilesetY - 1) + 1, sizeY * (tilesetY - 1) + 1 + sizeY):
                for x in range(sizeX * (tilesetX - 1) + 1, sizeX * (tilesetX - 1) + 1 + sizeX):
                    tilesets[tableCounter] = tiles[sheetWidth * (y - 1) + x]

    return tilesets

def generateLevel(width, height):
        tiles = []
        entities = []
        objects = []
        keyX = random.randint(2, width//2)
        lockX = random.randint(width//2 + 2, width - 10)
        lockColor = random.randint(1, 4)

        tileID = TILE_ID_GROUND

        topper = True
        tileset = random.randint(1, 20)
        topperset = random.randint(1, 20)

        for y in range(height):
            tiles.append([])

        for x in range(width):
            tileID = TILE_ID_EMPTY

            for y in range(7):
                tiles[y].append(Tile(x*16, y*16, tileID))

            if random.randint(1, 7) == 1 and x != keyX and x != lockX:
                for y in range(7, height):
                    tiles[y].append(Tile(x*16, y*16, tileID))
            else:
                tileID = TILE_ID_GROUND

                blockHeight = 3
                highestBlock = 6

                for y in range(7, height):
                    tiles[y].append(Tile(x*16, y*16, tileID, y == 7 and topper or False))

                if random.randint(1, 8) == 1:
                    blockHeight = 3
                    highestBlock = 6

                    tiles[5][x] = Tile(x*16, 5*16, tileID, topper)
                    tiles[6][x] = Tile(x*16, 6*16, tileID)
                    tiles[7][x].topper = False

                if x == keyX:
                    # insert key
                    b = 1

                if x == lockX:
                    # insert lock
                    b = 1

                if random.randint(1, 10) == 1:
                    # spawn block
                    b = 1

        return tiles, width, height

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = 16
        self.height = 20
        self.score = 0
        self.state = "falling"
        self.direction = "right"

    def update(self, dt):
        if self.state == "falling":
            self.dy += GRAVITY
            self.y += self.dy * dt
            #if self.y >= VIRTUAL_HEIGHT - 52:
                #self.y = VIRTUAL_HEIGHT - 52
                #self.state = "idle"
        if self.state == "jumping":
            self.dy += GRAVITY
            self.y += self.dy * dt
            if self.dy >= 0:
                self.state = "falling"
        self.x += self.dx * dt

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = 16
        self.height = 16
        self.direction = "left"

class Tile:
    def __init__(self, x, y, id, topper = False):
        self.x = x
        self.y = y
        self.id = id
        self.topper = topper

class SuperBros:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.state = "start"
        self.level, self.levelwidth, self.levelheight = generateLevel(100, 10)
        self.background = random.randint(0, 2)
        self.size = self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.player = Player(16, 16)

    def on_init(self):
        pygame.init()

        self.textures = {
            "tiles": pygame.image.load("pythongame/graphics/tiles.png"),
            "toppers": pygame.image.load("pythongame/graphics/tile_tops.png"),
            "bushes": pygame.image.load("pythongame/graphics/bushes_and_cacti.png"),
            "jump-blocks": pygame.image.load("pythongame/graphics/jump_blocks.png"),
            "gems": pygame.image.load("pythongame/graphics/gems.png"),
            "backgrounds": pygame.image.load("pythongame/graphics/backgrounds.png"),
            "green-alien": pygame.image.load("pythongame/graphics/green_alien.png"),
            "creatures": pygame.image.load("pythongame/graphics/creatures.png"),
            "keys-and-locks": pygame.image.load("pythongame/graphics/keys_and_locks.png"),
            "flags": pygame.image.load("pythongame/graphics/flags.png")
        }

        self.frames = {
            "tiles": generateSubsurfaces(self.textures["tiles"], 16, 16),
            "toppers": generateSubsurfaces(self.textures["toppers"], 16, 16),
            "bushes": generateSubsurfaces(self.textures["bushes"], 16, 16),
            "jump-blocks": generateSubsurfaces(self.textures["jump-blocks"], 16, 16),
            "gems": generateSubsurfaces(self.textures["gems"], 16, 16),
            "backgrounds": generateSubsurfaces(self.textures["backgrounds"], 256, 128),
            "green-alien": generateSubsurfaces(self.textures["green-alien"], 16, 20),
            "creatures": generateSubsurfaces(self.textures["creatures"], 16, 16),
            "keys-and-locks": generateSubsurfaces(self.textures["keys-and-locks"], 16, 16),
            "flags": generateSubsurfaces(self.textures["flags"], 16, 16)
        }

        self.fonts = {
            "small": pygame.font.Font("pythongame/fonts/font.ttf", 8),
            "medium": pygame.font.Font("pythongame/fonts/font.ttf", 16),
            "large": pygame.font.Font("pythongame/fonts/font.ttf", 32),
            "title": pygame.font.Font("pythongame/fonts/ArcadeAlternate.ttf", 32)
        }

        self.sounds = {
            "jump": pygame.mixer.Sound("pythongame/sounds/jump.wav"),
            "death": pygame.mixer.Sound("pythongame/sounds/death.wav"),
            "powerup-reveal": pygame.mixer.Sound("pythongame/sounds/powerup-reveal.wav"),
            "pickup": pygame.mixer.Sound("pythongame/sounds/pickup.wav"),
            "empty-block": pygame.mixer.Sound("pythongame/sounds/empty-block.wav"),
            "kill": pygame.mixer.Sound("pythongame/sounds/kill.wav"),
            "kill2": pygame.mixer.Sound("pythongame/sounds/kill2.wav")
        }

        pygame.mixer.music.load("pythongame/sounds/music.wav")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)

        self._screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._surf = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        pygame.display.set_caption('Super 50 Bros.')
        pygame.font.init()

        self.clock = pygame.time.Clock()

        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
            if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.state == "start":
                self.state = "play"
                self.level, self.levelwidth, self.levelheight = generateLevel(100, 10)
                #self.player = Player(16, 16)
            if event.key == pygame.K_UP and self.state == "play":
                self.player.dy = PLAYER_JUMP_VELOCITY
                self.player.state = "jumping"
                self.sounds["jump"].set_volume(0.25)
                self.sounds["jump"].play()
            if event.key == pygame.K_RIGHT and self.state == "play":
                self.player.direction = "right"
                self.player.dx = PLAYER_WALK_SPEED
            if event.key == pygame.K_LEFT and self.state == "play":
                self.player.direction = "left"
                self.player.dx = -PLAYER_WALK_SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and self.player.direction == "right" and self.state == "play":
                self.player.dx = 0
            if event.key == pygame.K_LEFT and self.player.direction == "left" and self.state == "play":
                self.player.dx = 0

    def on_loop(self):
        dt = self.clock.tick(60) / 1000
        if self.state == "play":
            self.player.update(dt)
            b_collision, y = self.checkBottomCollision()
            if self.player.direction == "right":
                r_collision, x = self.checkRightCollisions()
                if r_collision:
                    self.player.dx = 0
                    self.player.x = x
            if self.player.direction == "left":
                l_collision, x = self.checkLeftCollisions()
                if l_collision:
                    self.player.dx = 0
                    self.player.x = x
            if self.player.state == "falling":
                if b_collision:
                    self.player.dy = 0
                    self.player.y = y
                    if self.player.dx == 0:
                        self.player.state = "idle"
                    else:
                        self.player.state = "walking"
            else:
                if not b_collision:
                    self.player.state = "falling"

    def pointToTile(self, x, y):
        if x < 0 or x > self.levelwidth*16 or y < 0 or y > self.levelheight*16:
            return None
        
        return self.level[int(y // 16)][int(x // 16)]

    def checkBottomCollision(self):
        tileBottomLeft = self.pointToTile(self.player.x + 1, self.player.y + self.player.height + 1)
        tileBottomRight = self.pointToTile(self.player.x + self.player.width - 1, self.player.y + self.player.height + 1)

        tiles = []
        if tileBottomLeft:
            tiles.append(tileBottomLeft)
        if tileBottomRight:
            tiles.append(tileBottomRight)

        for tile in tiles:
            if tile.id == TILE_ID_GROUND:
                return True, tile.y - self.player.height

        return False, None

    def checkRightCollisions(self):
        tileTopRight = self.pointToTile(self.player.x + self.player.width + 1, self.player.y + 1)
        tileBottomRight = self.pointToTile(self.player.x + self.player.width + 1, self.player.y + self.player.height - 1)

        tiles = []
        if tileTopRight:
            tiles.append(tileTopRight)
        if tileBottomRight:
            tiles.append(tileBottomRight)

        for tile in tiles:
            if tile.id == TILE_ID_GROUND:
                return True, tile.x - self.player.width

        return False, None
    
    def checkLeftCollisions(self):
        tileTopLeft = self.pointToTile(self.player.x - 1, self.player.y + 1)
        tileBottomLeft = self.pointToTile(self.player.x - 1, self.player.y + self.player.height - 1)

        tiles = []
        if tileTopLeft:
            tiles.append(tileTopLeft)
        if tileBottomLeft:
            tiles.append(tileBottomLeft)

        for tile in tiles:
            if tile.id == TILE_ID_GROUND:
                return True, tile.x + 16

        return False, None

    def render_level(self):
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                tile = self.level[y][x]
                if tile.id != TILE_ID_EMPTY:
                    self._surf.blit(self.frames["tiles"][tile.id], (tile.x, tile.y))
                    if tile.topper:
                        self._surf.blit(self.frames["toppers"][tile.id], (tile.x, tile.y))

    def on_render(self):
        if self.state == "start":
            self._surf.blit(self.frames["backgrounds"][self.background], (0, self.frames["backgrounds"][self.background].get_height() / 3))
            self._surf.blit(self.frames["backgrounds"][self.background], (0, 0))
            
            self.render_level()

            text_surface = self.fonts["title"].render('Super 50 Bros.', True, (0, 0, 0))
            self._surf.blit(text_surface, (VIRTUAL_WIDTH / 2 - text_surface.get_width() / 2 + 1, VIRTUAL_HEIGHT / 2 - 40 + 1))
            text_surface = self.fonts["title"].render('Super 50 Bros.', True, (255, 255, 255))
            self._surf.blit(text_surface, (VIRTUAL_WIDTH / 2 - text_surface.get_width() / 2, VIRTUAL_HEIGHT / 2 - 40))
            text_surface = self.fonts["medium"].render('Press Enter', True, (0, 0, 0))
            self._surf.blit(text_surface, (VIRTUAL_WIDTH / 2 - text_surface.get_width() / 2 + 1, VIRTUAL_HEIGHT / 2 + 17))
            text_surface = self.fonts["medium"].render('Press Enter', True, (255, 255, 255))
            self._surf.blit(text_surface, (VIRTUAL_WIDTH / 2 - text_surface.get_width() / 2, VIRTUAL_HEIGHT / 2 + 16))

            self._screen.blit(pygame.transform.scale(self._surf, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

            pygame.display.update()
        if self.state == "play":
            self._surf.blit(self.frames["backgrounds"][self.background], (0, self.frames["backgrounds"][self.background].get_height() / 3))
            self._surf.blit(self.frames["backgrounds"][self.background], (0, 0))

            self.render_level()

            self._surf.blit(self.frames["green-alien"][0], (self.player.x, self.player.y))

            text_surface = self.fonts["medium"].render(str(self.player.score), True, (0, 0, 0))
            self._surf.blit(text_surface, (5, 5))
            text_surface = self.fonts["medium"].render(str(self.player.score), True, (255, 255, 255))
            self._surf.blit(text_surface, (4, 4))

            self._screen.blit(pygame.transform.scale(self._surf, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

            pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    game = SuperBros()
    game.on_execute()