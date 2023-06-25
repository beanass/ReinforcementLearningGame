import pygame
from pygame.locals import *
import random
from math import floor
import os

current_file_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_file_dir)

sounds_path = os.path.join(base_dir, "pythongame", "sounds")
graphics_path = os.path.join(base_dir, "pythongame", "graphics")
fonts_path = os.path.join(base_dir, "pythongame", "fonts")

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

VIRTUAL_WIDTH = 256
VIRTUAL_HEIGHT = 144

PLAYER_WALK_SPEED = 80
PLAYER_JUMP_VELOCITY = -275

SNAIL_MOVE_SPEED = 10

TILE_ID_EMPTY = 4
TILE_ID_GROUND = 2

GRAVITY = 12

KEYS = [
    0, 1, 2, 3
]

LOCKS = [
    4, 5, 6, 7
]

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
        lockColor = random.randint(0, 3)

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

                blockHeight = 4
                highestBlock = 7

                for y in range(7, height):
                    tiles[y].append(Tile(x*16, y*16, tileID, y == 7 and topper or False))

                if random.randint(1, 8) == 1:
                    blockHeight = 2
                    highestBlock = 5

                    if random.randint(1, 8) == 1:
                        id = random.randint(0, 4)
                        if id > 1:
                            id += 2
                        objects.append(Gameobject(x*16, 4*16, id, "bushes"))

                    tiles[5][x] = Tile(x*16, 5*16, tileID, topper)
                    tiles[6][x] = Tile(x*16, 6*16, tileID)
                    tiles[7][x].topper = False

                elif random.randint(1, 8) == 1:
                    id = random.randint(0, 4)
                    if id > 1:
                        id += 2
                    objects.append(Gameobject(x*16, 6*16, id, "bushes"))

                if x == keyX:
                    objects.append(Gameobject(x*16, (highestBlock-1)*16, KEYS[lockColor], "keys-and-locks", True))

                if x == lockX:
                    objects.append(Gameobject(x*16, (highestBlock-1)*16, LOCKS[lockColor], "keys-and-locks"))

                if random.randint(1, 12) == 1:
                    gemspawn = random.randint(0, 3)
                    objects.append(Gameobject(x*16, blockHeight*16, random.randint(0, 29), "jump-blocks", gem = True if gemspawn == 0 else False))

                if random.randint(1, 20) == 1 and x > 10:
                    entities.append(Entity(x*16, (highestBlock-1)*16, None))

        return tiles, objects, entities, width, height, lockColor, keyX*16, lockX*16

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = 16
        self.height = 20
        self.score = 0
        self.state = "idle"
        self.direction = "right"
        self.key = False
        self.lock = False
        self.dead = False

    def update(self, dt):
        if self.state == "falling":
            self.dy += GRAVITY
            self.y += self.dy * dt
        if self.state == "jumping":
            self.dy += GRAVITY
            self.y += self.dy * dt
            if self.dy >= 0:
                self.state = "falling"
        self.x += self.dx * dt

class Entity:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = 16
        self.height = 16
        self.direction = "left"
        self.state = "idle"
        self.player = player

    def update(self, dt):
        if abs(self.player.x - self.x) <= 5*16:
            self.state = "chasing"
        if self.state == "chasing":
            if self.player.x > self.x:
                self.direction = "right"
                self.dx = SNAIL_MOVE_SPEED
            else:
                self.direction = "left"
                self.dx = -SNAIL_MOVE_SPEED
        if self.state == "idle":
            self.dx = 0
        self.x += self.dx * dt

class Tile:
    def __init__(self, x, y, id, topper = False):
        self.x = x
        self.y = y
        self.id = id
        self.topper = topper

class Gameobject:
    def __init__(self, x, y, id, texture, key = False, gem = False):
        self.x = x
        self.y = y
        self.id = id
        self.texture = texture
        self.key = key
        self.hit = False
        self.collided = False
        self.gem = gem

class SuperBros:
    def __init__(self):
        self._running = True

    def on_init(self):
        pygame.init()

        self.state = "start"
        self.levelcount = 0
        self.level, self.objects, self.entities, self.levelwidth, self.levelheight, self.lockColor, self.keyX, self.lockX = generateLevel(100, 10)
        self.background = random.randint(0, 2)
        self.size = self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.player = Player(16, 16)
        self.camX = 0
        self.backgroundX = 0

        self.textures = {
            "tiles": pygame.image.load(os.path.join(graphics_path, "tiles.png")),
            "toppers": pygame.image.load(os.path.join(graphics_path, "tile_tops.png")),
            "bushes": pygame.image.load(os.path.join(graphics_path, "bushes_and_cacti.png")),
            "jump-blocks": pygame.image.load(os.path.join(graphics_path, "jump_blocks.png")),
            "gems": pygame.image.load(os.path.join(graphics_path, "gems.png")),
            "backgrounds": pygame.image.load(os.path.join(graphics_path, "backgrounds.png")),
            "green-alien": pygame.image.load(os.path.join(graphics_path, "green_alien.png")),
            "creatures": pygame.image.load(os.path.join(graphics_path, "creatures.png")),
            "keys-and-locks": pygame.image.load(os.path.join(graphics_path, "keys_and_locks.png")),
            "flags": pygame.image.load(os.path.join(graphics_path, "flags.png"))
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
            "small": pygame.font.Font(os.path.join(fonts_path, "font.ttf"), 8),
            "medium": pygame.font.Font(os.path.join(fonts_path, "font.ttf"), 16),
            "large": pygame.font.Font(os.path.join(fonts_path, "font.ttf"), 32),
            "title": pygame.font.Font(os.path.join(fonts_path, "ArcadeAlternate.ttf"), 32)
        }

        self.sounds = {
            "jump": pygame.mixer.Sound(os.path.join(sounds_path, "jump.wav")),
            "death": pygame.mixer.Sound(os.path.join(sounds_path, "death.wav")),
            "powerup-reveal": pygame.mixer.Sound(os.path.join(sounds_path, "powerup-reveal.wav")),
            "pickup": pygame.mixer.Sound(os.path.join(sounds_path, "pickup.wav")),
            "empty-block": pygame.mixer.Sound(os.path.join(sounds_path, "empty-block.wav")),
            "kill": pygame.mixer.Sound(os.path.join(sounds_path, "kill.wav")),
            "kill2": pygame.mixer.Sound(os.path.join(sounds_path, "kill2.wav"))
        }

        #pygame.mixer.music.load(os.path.join(sounds_path, "music.wav"))
        #pygame.mixer.music.set_volume(0.05)
        #pygame.mixer.music.play(-1)

        self._screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._surf = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        pygame.display.set_caption('Super 50 Bros.')
        pygame.font.init()

        self.clock = pygame.time.Clock()

        self._running = True

    def get_tile_observation(self):
        tile_observation = []
        for y in range(0, 9):
            for x in range(int(self.player.x // 16), int(self.player.x // 16) + 16):
                if x >= 0 and x < self.levelwidth:
                    obs = 1 if self.level[y][x].id == TILE_ID_GROUND else 0
                else:
                    obs = 1
                tile_observation.append(obs)

        for object in self.objects:
            if object.texture == "jump-blocks":
                if object.x // 16 >= self.player.x // 16 and object.x // 16 < self.player.x // 16 + 16:
                    #index = (object.y // 16 - 1)*16 + (object.x // 16 - 1)
                    index = (object.y // 16)*16 + (object.x // 16 - int(self.player.x // 16))
                    tile_observation[index] = 1

        return tile_observation

    def get_next_enemyX(self):
        x = 100000
        e_x = 0
        for entity in self.entities:
            if abs(entity.x - self.player.x) < x:
                x = abs(entity.x - self.player.x)
                e_x = entity.x - self.player.x
        return e_x
                
    def get_next_enemyY(self):
        x = 100000
        y = 0
        for entity in self.entities:
            if abs(entity.x - self.player.x) < x:
                x = abs(entity.x - self.player.x)
                y = entity.y - self.player.y
        return y

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
            if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_DOWN) and self.state == "start":
                self.state = "play"
                self.levelcount += 1
                self.level, self.objects, self.entities, self.levelwidth, self.levelheight, self.lockColor, self.keyX, self.lockX = generateLevel(100, 10)
                self.spawnPlayer()
            if event.key == pygame.K_UP and self.state == "play" and self.player.state != "jumping" and self.player.state != "falling":
                self.player.dy = PLAYER_JUMP_VELOCITY
                self.player.state = "jumping"
                #self.sounds["jump"].set_volume(0.25)
                #self.sounds["jump"].play()
            '''if event.key == pygame.K_RIGHT and self.state == "play":
                self.player.direction = "right"
                self.player.dx = PLAYER_WALK_SPEED
            if event.key == pygame.K_LEFT and self.state == "play":
                self.player.direction = "left"
                self.player.dx = -PLAYER_WALK_SPEED'''
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and self.player.direction == "right" and self.state == "play":
                self.player.dx = 0
            if event.key == pygame.K_LEFT and self.player.direction == "left" and self.state == "play":
                self.player.dx = 0

    def on_loop(self):
        dt = self.clock.tick(60) / 1000
        if self.state == "play":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.player.direction = "right"
                self.player.dx = PLAYER_WALK_SPEED
            if keys[pygame.K_LEFT]:
                self.player.direction = "left"
                self.player.dx = -PLAYER_WALK_SPEED


            self.player.update(dt)

            for entity in self.entities:
                if entity.player == None:
                    entity.player = self.player
                entity.update(dt)

            self.camX = max(0, min(16 * self.levelwidth - VIRTUAL_WIDTH, self.player.x - (VIRTUAL_WIDTH / 2 - 8)))
            self.backgroundX = (self.camX / 3) % 256

            if self.player.y > VIRTUAL_HEIGHT:
                #self.sounds["death"].set_volume(0.25)
                #self.sounds["death"].play()
                self.state = "start"
                self.background = random.randint(0, 2)
                self.levelcount = 0
                self.level, self.objects, self.entities, self.levelwidth, self.levelheight, self.lockColor, self.keyX, self.lockX = generateLevel(100, 10)
                self.player = Player(16, 16)
                self.player.dead = True
                return

            self.checkObjectCollision()
            self.checkEntityCollision(dt)

            t_collision, y = self.checkTopCollision()
            if self.player.state == "jumping":
                if t_collision:
                    self.player.dy = 0
                    self.player.y = y
                    self.player.state = "falling"
                    return

            b_collision, y = self.checkBottomCollision()
            if self.player.direction == "right":
                r_collision, x = self.checkRightCollisions()
                if r_collision:
                    self.player.dx = 0
                    self.player.x = x - 0.5
            if self.player.direction == "left":
                l_collision, x = self.checkLeftCollisions()
                if l_collision:
                    self.player.dx = 0
                    self.player.x = x + 0.5
            if self.player.state == "falling":
                if b_collision:
                    for object in self.objects:
                        object.collided = False
                    self.player.dy = 0
                    self.player.y = y
                    if self.player.dx == 0:
                        self.player.state = "idle"
                    else:
                        self.player.state = "walking"
            elif not self.player.state == "jumping":
                if not b_collision:
                    self.player.state = "falling"

    def spawnPlayer(self):
        x = y = 0
        for i in range(0, self.levelwidth):
            for j in range(0, self.levelheight):
                if self.level[j][i].id == TILE_ID_GROUND:
                    x = i * 16
                    y = j * 16 - 20
                    break
            if x != 0 and y != 0:
                break

        self.player = Player(x, y)

    def spawnFlagpole(self):
        poleColor = random.randint(0, 5)
        x = y = 0
        for i in range(self.levelwidth-1, 1, -1):
            for j in range(0, self.levelheight):
                if self.level[j][i-1].id == TILE_ID_GROUND:
                    x = (i-1) * 16
                    y = (j-1) * 16
                    break
            if x != 0 and y != 0:
                break

        poleBottom = Gameobject(x, y, poleColor+18, "flags")
        self.objects.append(poleBottom)
        poleHeight = random.randint(1, 3)+1
        for i in range(1, poleHeight):
            pole = Gameobject(x, y - i*16, poleColor+9, "flags")
            self.objects.append(pole)

        poleTop = Gameobject(x, y - poleHeight*16, poleColor, "flags")
        self.objects.append(poleTop)

        flagCount = random.randint(2, 3)
        for i in range(flagCount):
            flagColor = (random.randint(0, 3))*9+6
            flag = Gameobject(x + 8, y - (poleHeight+i-2)*16, flagColor, "flags")
            self.objects.append(flag)     

    def pointToTile(self, x, y):
        if x < 0 or x > self.levelwidth*16 or y < 0 or y > self.levelheight*16:
            return None
        
        return self.level[int(y // 16)][int(x // 16)]

    def checkEntityCollision(self, dt):
        for entity in self.entities:
            if entity.direction == "right":
                tileRight = self.pointToTile(entity.x + entity.width, entity.y)
                tileBottomRight = self.pointToTile(entity.x + entity.width, entity.y + entity.height)

                if (tileRight and tileBottomRight) and (tileRight.id == TILE_ID_GROUND or tileBottomRight.id == TILE_ID_EMPTY):
                    entity.x -= SNAIL_MOVE_SPEED * dt
                    entity.direction = "left"
            elif entity.direction == "left":
                tileLeft = self.pointToTile(entity.x, entity.y)
                tileBottomLeft = self.pointToTile(entity.x, entity.y + entity.height)

                if (tileLeft and tileBottomLeft) and (tileLeft.id == TILE_ID_GROUND or tileBottomLeft.id == TILE_ID_EMPTY):
                    entity.x += SNAIL_MOVE_SPEED * dt
                    entity.direction = "right"

            e_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
            p_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            if p_rect.colliderect(e_rect):
                if self.player.state == "falling" and self.player.y + self.player.height - 2 <= entity.y + 5:
                    #self.sounds["kill"].set_volume(0.25)
                    #self.sounds["kill"].play()
                    #self.sounds["kill2"].set_volume(0.25)
                    #self.sounds["kill2"].play()
                    self.entities.remove(entity)
                    self.player.score += 100
                else:
                    #self.sounds["death"].set_volume(0.25)
                    #self.sounds["death"].play()
                    self.state = "start"
                    self.background = random.randint(0, 2)
                    self.levelcount = 0
                    self.level, self.objects, self.entities, self.levelwidth, self.levelheight, self.lockColor, self.keyX, self.lockX = generateLevel(100, 10)
                    self.spawnPlayer()
                    self.player.dead = True
                    return

    def checkObjectCollision(self):
        p_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for object in self.objects:
            o_rect = pygame.Rect(object.x, object.y, 16, 8)
            if object.texture == "keys-and-locks":
                if p_rect.colliderect(o_rect):
                    if object.key == True:
                        #self.sounds["pickup"].set_volume(0.25)
                        #self.sounds["pickup"].play()
                        self.objects.remove(object)
                        self.player.key = True
                        self.keyX = 0
                    else:
                        if self.player.key == True:
                            #self.sounds["pickup"].set_volume(0.25)
                            #self.sounds["pickup"].play()
                            self.objects.remove(object)
                            #self.player.key = False
                            self.player.lock = True
                            self.lockX = 0
                            self.spawnFlagpole()
            elif object.texture == "flags":
                if p_rect.colliderect(o_rect):
                    self.background = random.randint(0, 2)
                    self.levelcount += 1
                    self.level, self.objects, self.entities, self.levelwidth, self.levelheight, self.lockColor, self.keyX, self.lockX = generateLevel(100, 10)
                    score = self.player.score
                    self.spawnPlayer()
                    self.player.score = score
                    self.camX = 0
            elif object.texture == "gems":
                if p_rect.colliderect(o_rect):
                    #self.sounds["pickup"].set_volume(0.25)
                    #self.sounds["pickup"].play()
                    self.objects.remove(object)
                    self.player.score += 100

    def checkTopCollision(self):
        if self.player.y <= -10:
            return True, -10

        for object in self.objects:
            if object.texture == "jump-blocks":
                if self.player.x + self.player.width > object.x + 1 and self.player.x < object.x + 15:
                    if self.player.y - 1 <= object.y + 16 and self.player.y - 1 >= object.y + 11:
                        if not object.collided:
                            object.collided = True
                            #self.sounds["empty-block"].set_volume(0.25)
                            #self.sounds["empty-block"].play()
                            if not object.hit:
                                object.hit = True
                                if object.gem:
                                    #self.sounds["powerup-reveal"].set_volume(0.25)
                                    #self.sounds["powerup-reveal"].play()
                                    self.objects.append(Gameobject(object.x, object.y - 16 + 2, random.randint(0, 7), "gems"))
                                
                        return True, object.y + 16

        return False, None

    def checkBottomCollision(self):
        tileBottomLeft = self.pointToTile(self.player.x + 2, self.player.y + self.player.height + 2)
        tileBottomRight = self.pointToTile(self.player.x + self.player.width - 2, self.player.y + self.player.height + 2)

        tiles = []
        if tileBottomLeft:
            tiles.append(tileBottomLeft)
        if tileBottomRight:
            tiles.append(tileBottomRight)

        for tile in tiles:
            if tile.id == TILE_ID_GROUND:
                return True, tile.y - self.player.height

        for object in self.objects:
            if object.texture == "jump-blocks":
                if self.player.x + self.player.width > object.x + 1 and self.player.x < object.x + 15:
                    if self.player.y + self.player.height >= object.y and self.player.y + self.player.height <= object.y + 5:
                        return True, object.y - self.player.height

        return False, None

    def checkRightCollisions(self):
        tileTopRight = self.pointToTile(self.player.x + self.player.width + 2, self.player.y + 2)
        tileBottomRight = self.pointToTile(self.player.x + self.player.width + 2, self.player.y + self.player.height - 4)

        tiles = []
        if tileTopRight:
            tiles.append(tileTopRight)
        if tileBottomRight:
            tiles.append(tileBottomRight)

        for object in self.objects:
            if object.texture == "jump-blocks":
                if self.player.x + self.player.width + 2 >= object.x and self.player.x + self.player.width + 2 <= object.x + 5:
                    if self.player.y + self.player.height - 3 > object.y and self.player.y + 3 < object.y + 8:
                        return True, object.x - self.player.width

        if len(tiles) == 0:
            return True, self.levelwidth * 16 - self.player.width

        for tile in tiles:
            if tile.id == TILE_ID_GROUND:
                return True, tile.x - self.player.width

        return False, None
    
    def checkLeftCollisions(self):
        tileTopLeft = self.pointToTile(self.player.x - 2, self.player.y + 2)
        tileBottomLeft = self.pointToTile(self.player.x - 2, self.player.y + self.player.height - 4)

        tiles = []
        if tileTopLeft:
            tiles.append(tileTopLeft)
        if tileBottomLeft:
            tiles.append(tileBottomLeft)

        for object in self.objects:
            if object.texture == "jump-blocks":
                if self.player.x - 2 <= object.x + 16 and self.player.x - 2 >= object.x + 11:
                    if self.player.y + self.player.height - 3 > object.y and self.player.y + 3 < object.y + 8:
                        return True, object.x + 16

        if len(tiles) == 0:
            return True, 0

        for tile in tiles:
            if tile.id == TILE_ID_GROUND:
                return True, tile.x + 16

        return False, None

    def render_level(self):
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                tile = self.level[y][x]
                if tile.id != TILE_ID_EMPTY:
                    self._surf.blit(self.frames["tiles"][tile.id], (tile.x - self.camX, tile.y))
                    if tile.topper:
                        self._surf.blit(self.frames["toppers"][tile.id], (tile.x - self.camX, tile.y))

        for object in self.objects:
            self._surf.blit(self.frames[object.texture][object.id], (object.x - self.camX, object.y))

        for entity in self.entities:
            if entity.direction == "right":
                self._surf.blit(pygame.transform.flip(self.frames["creatures"][49], True, False), (entity.x - self.camX, entity.y))
            else:
                self._surf.blit(self.frames["creatures"][49], (entity.x - self.camX, entity.y))

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
            self._surf.blit(self.frames["backgrounds"][self.background], (-self.backgroundX, self.frames["backgrounds"][self.background].get_height() / 3))
            self._surf.blit(self.frames["backgrounds"][self.background], (-self.backgroundX, 0))

            self._surf.blit(self.frames["backgrounds"][self.background], (-self.backgroundX + 256, self.frames["backgrounds"][self.background].get_height() / 3))
            self._surf.blit(self.frames["backgrounds"][self.background], (-self.backgroundX + 256, 0))

            self.render_level()

            self._surf.blit(self.frames["green-alien"][0], (self.player.x - self.camX, self.player.y))

            text_surface = self.fonts["medium"].render(str(self.player.score), True, (0, 0, 0))
            self._surf.blit(text_surface, (5, 5))
            text_surface = self.fonts["medium"].render(str(self.player.score), True, (255, 255, 255))
            self._surf.blit(text_surface, (4, 4))

            if self.player.key:
                key_surface = self.frames["keys-and-locks"][KEYS[self.lockColor]]
                key_surface = pygame.transform.scale(key_surface, (8, 8))
                self._surf.blit(key_surface, (VIRTUAL_WIDTH - 16, 5))
            if self.player.lock:
                lock_surface = self.frames["keys-and-locks"][LOCKS[self.lockColor]]
                lock_surface = pygame.transform.scale(lock_surface, (8, 8))
                self._surf.blit(lock_surface, (VIRTUAL_WIDTH - 16, 5))

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