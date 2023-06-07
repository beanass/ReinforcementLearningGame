import pygame
import os

def generateQuads(atlas, tileWidth, tileHeight):
    sheetWidth = atlas.get_width() // tileWidth
    sheetHeight = atlas.get_height() // tileHeight

    sheetCounter = 0
    quads = []

    for y in range(sheetHeight):
        for x in range(sheetWidth):
            quads.append(pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            sheetCounter += 1

    return quads

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

def getTileset(spritesheet):
    for y in range(4):
        for x in range(5):
            continue
    pass

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

def getBackgroundSurfaces(spritesheet, width, height):
    surfaces = []
    
    surfaces.append(spritesheet.subsurface(pygame.Rect(0, 0, width, height)))
    surfaces.append(spritesheet.subsurface(pygame.Rect(0, height, width, height)))
    surfaces.append(spritesheet.subsurface(pygame.Rect(0, height * 2, width, height)))

    return surfaces

gSounds = {}
gTextures = {}
gFrames = {}
gFonts = {}

def loadAssets():
    global gSounds
    global gTextures
    global gFrames
    global gFonts

    gSounds = {
        "jump": pygame.mixer.Sound("pygame/sounds/jump.wav"),
        "death": pygame.mixer.Sound("pygame/sounds/death.wav"),
        "music": pygame.mixer.music.load("pygame/sounds/music.wav"),
        "powerup-reveal": pygame.mixer.Sound("pygame/sounds/powerup-reveal.wav"),
        "pickup": pygame.mixer.Sound("pygame/sounds/pickup.wav"),
        "empty-block": pygame.mixer.Sound("pygame/sounds/empty-block.wav"),
        "kill": pygame.mixer.Sound("pygame/sounds/kill.wav"),
        "kill2": pygame.mixer.Sound("pygame/sounds/kill2.wav")
    }

    gTextures = {
        "tiles": pygame.image.load("pygame/graphics/tiles.png"),
        "toppers": pygame.image.load("pygame/graphics/tile_tops.png"),
        "bushes": pygame.image.load("pygame/graphics/bushes_and_cacti.png"),
        "jump-blocks": pygame.image.load("pygame/graphics/jump_blocks.png"),
        "gems": pygame.image.load("pygame/graphics/gems.png"),
        "backgrounds": pygame.image.load("pygame/graphics/backgrounds.png"),
        "green-alien": pygame.image.load("pygame/graphics/green_alien.png"),
        "creatures": pygame.image.load("pygame/graphics/creatures.png"),
        "keys-and-locks": pygame.image.load("pygame/graphics/keys_and_locks.png"),
        "flags": pygame.image.load("pygame/graphics/flags.png")
    }

    gFrames = {
        "tiles": generateSubsurfaces(gTextures["tiles"], 16, 16),
        "toppers": generateSubsurfaces(gTextures["toppers"], 16, 16),
        #"bushes": generateQuads(gTextures["bushes"], 16, 16),
        #"jump-blocks": generateQuads(gTextures["jump-blocks"], 16, 16),
        "gems": generateSubsurfaces(gTextures["gems"], 16, 16),
        "backgrounds": generateSubsurfaces(gTextures["backgrounds"], 256, 128),
        "green-alien": generateSubsurfaces(gTextures["green-alien"], 16, 20),
        "creatures": generateSubsurfaces(gTextures["creatures"], 16, 16),
        "keys-and-locks": generateSubsurfaces(gTextures["keys-and-locks"], 16, 16),
        "flags": generateSubsurfaces(gTextures["flags"], 16, 16)
    }

    gFrames["tilesets"] = generateTileSets(gFrames["tiles"], 6, 10, 5, 4)
    gFrames["toppersets"] = generateTileSets(gFrames["toppers"], 6, 18, 5, 4)

    gFonts = {
        "small": pygame.font.Font("pygame/fonts/font.ttf", 8),
        "medium": pygame.font.Font("pygame/fonts/font.ttf", 16),
        "large": pygame.font.Font("pygame/fonts/font.ttf", 32),
        "title": pygame.font.Font("pygame/fonts/ArcadeAlternate.ttf", 32)
    }

