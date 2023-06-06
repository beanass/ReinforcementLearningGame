import pygame

def gemerateQuads(atlas, tileWidth, tileHeight):
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

gSounds = {
    "jump": pygame.mixer.Sound("sounds/jump.wav"),
    "death": pygame.mixer.Sound("sounds/death.wav"),
    "music": pygame.mixer.music.load("sounds/music.wav"),
    "powerup-reveal": pygame.mixer.Sound("sounds/powerup-reveal.wav"),
    "pickup": pygame.mixer.Sound("sounds/pickup.wav"),
    "empty-block": pygame.mixer.Sound("sounds/empty-block.wav"),
    "kill": pygame.mixer.Sound("sounds/kill.wav"),
    "kill2": pygame.mixer.Sound("sounds/kill2.wav")
}

gTextures = {
    "tiles": pygame.image.load("graphics/tiles.png"),
    "toppers": pygame.image.load("graphics/tile_tops.png"),
    "bushes": pygame.image.load("graphics/bushes_and_cacti.png"),
    "jump-blocks": pygame.image.load("graphics/jump_blocks.png"),
    "gems": pygame.image.load("graphics/gems.png"),
    "backgrounds": pygame.image.load("graphics/backgrounds.png"),
    "green-alien": pygame.image.load("graphics/green_alien.png"),
    "creatures": pygame.image.load("graphics/creatures.png"),
    "keys-and-locks": pygame.image.load("graphics/keys_and_locks.png"),
    "flags": pygame.image.load("graphics/flags.png")
}

gFrames = {
    "tiles": gemerateQuads(gTextures["tiles"], 16, 16),
    "toppers": generateQuads(gTextures["toppers"], 16, 16),
    "bushes": generateQuads(gTextures["bushes"], 16, 16),
    "jump-blocks": generateQuads(gTextures["jump-blocks"], 16, 16),
    "gems": generateQuads(gTextures["gems"], 16, 16),
    "backgrounds": generateQuads(gTextures["backgrounds"], 256, 128),
    "green-alien": generateQuads(gTextures["green-alien"], 16, 20),
    "creatures": generateQuads(gTextures["creatures"], 16, 16),
    "keys-and-locks": generateQuads(gTextures["keys-and-locks"], 16, 16),
    "flags": generateQuads(gTextures["flags"], 16, 16),
    "tilesets": generateTileSets(gFrames["tiles"], 6, 10, 5, 4),
    "toppersets": generateTileSets(gFrames["toppers"], 6, 18, 5, 4)
}

gFonts = {
    "small": pygame.font.Font("fonts/font.ttf", 8),
    "medium": pygame.font.Font("fonts/font.ttf", 16),
    "large": pygame.font.Font("fonts/font.ttf", 32),
    "title": pygame.font.Font("fonts/ArcadeAlternate.ttf", 32)
}

