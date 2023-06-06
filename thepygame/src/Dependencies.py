import pygame
import os

pygame.init()

print(os.getcwd())

# Get the base directory of your script
current_file_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_file_dir)
# Construct the paths to the sound files using the base directory
sounds_path = os.path.join(base_dir, "sounds")
graphics_path = os.path.join(base_dir, "graphics")
fonts_path = os.path.join(base_dir, "fonts")

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

def generateTileSets(quads, setsX, setsY, sizeX, sizeY):
    tileSets = []
    tableCounter = 0
    sheetWidth = setsX * sizeX
    sheetHeight = setsY * sizeY

    for tilesetY in range(setsY):
        for tilesetX in range(setsX):
            tileSet = pygame.Surface((sheetWidth, sheetHeight), pygame.SRCALPHA)
            tileSet.fill((0, 0, 0, 0))
            for y in range(sizeY):
                for x in range(sizeX):
                    tileSet.blit(gTextures["tiles"], (x * 16, y * 16), quads[tableCounter])
                    tableCounter += 1
            tileSets.append(tileSet)

    return tileSets

def getSurfaces(spritesheet, width, height):
    surfaces = []
    
    surfaces.append(spritesheet.subsurface(pygame.Rect(0, 0, width, height)))
    surfaces.append(spritesheet.subsurface(pygame.Rect(0, height, width, height)))
    surfaces.append(spritesheet.subsurface(pygame.Rect(0, height * 2, width, height)))

    return surfaces

gSounds = {
    "jump": pygame.mixer.Sound(os.path.join(sounds_path, "jump.wav")),
    "death": pygame.mixer.Sound(os.path.join(sounds_path, "death.wav")),
    "music": pygame.mixer.music.load(os.path.join(sounds_path, "music.wav")),
    "powerup-reveal": pygame.mixer.Sound(os.path.join(sounds_path, "powerup-reveal.wav")),
    "pickup": pygame.mixer.Sound(os.path.join(sounds_path, "pickup.wav")),
    "empty-block": pygame.mixer.Sound(os.path.join(sounds_path, "empty-block.wav")),
    "kill": pygame.mixer.Sound(os.path.join(sounds_path, "kill.wav")),
    "kill2": pygame.mixer.Sound(os.path.join(sounds_path, "kill2.wav"))
}

gTextures = {
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

gFrames = {
    "tiles": generateQuads(gTextures["tiles"], 16, 16),
    "toppers": generateQuads(gTextures["toppers"], 16, 16),
    "bushes": generateQuads(gTextures["bushes"], 16, 16),
    "jump-blocks": generateQuads(gTextures["jump-blocks"], 16, 16),
    "gems": generateQuads(gTextures["gems"], 16, 16),
    "backgrounds": getSurfaces(gTextures["backgrounds"], 256, 128),
    "green-alien": generateQuads(gTextures["green-alien"], 16, 20),
    "creatures": generateQuads(gTextures["creatures"], 16, 16),
    "keys-and-locks": generateQuads(gTextures["keys-and-locks"], 16, 16),
    "flags": generateQuads(gTextures["flags"], 16, 16)
}

gFrames["tilesets"] = generateTileSets(gFrames["tiles"], 6, 10, 5, 4)
gFrames["toppersets"] = generateTileSets(gFrames["toppers"], 6, 18, 5, 4)

gFonts = {
    "small": pygame.font.Font(os.path.join(fonts_path, "font.ttf"), 8),
    "medium": pygame.font.Font(os.path.join(fonts_path, "font.ttf"), 16),
    "large": pygame.font.Font(os.path.join(fonts_path, "font.ttf"), 32),
    "title": pygame.font.Font(os.path.join(fonts_path, "ArcadeAlternate.ttf"), 32)
}

