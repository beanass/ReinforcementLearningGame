WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

VIRTUAL_WIDTH = 256
VIRTUAL_HEIGHT = 144

TILE_SIZE = 16

SCREEN_TILE_WIDTH = VIRTUAL_WIDTH / TILE_SIZE
SCREEN_TILE_HEIGHT = VIRTUAL_HEIGHT / TILE_SIZE

CAMERA_SPEED = 100

BACKGROUND_SCROLL_SPEED = 10

TILE_SET_WIDTH = 5
TILE_SET_HEIGHT = 4

TILE_SETS_WIDE = 6
TILE_SETS_TALL = 10

TOPPER_SETS_WIDE = 6
TOPPER_SETS_TALL = 18

TOPPER_SETS = TOPPER_SETS_WIDE * TOPPER_SETS_TALL
TILE_SETS = TILE_SETS_WIDE * TILE_SETS_TALL

PLAYER_WALK_SPEED = 60 #100

PLAYER_JUMP_VELOCITY = -150 #-225

KEY_FOLLOW_DRAG = 20

SNAIL_MOVE_SPEED = 10

TILE_ID_EMPTY = 5
TILE_ID_GROUND = 3

COLLIDABLE_TILES = [
    TILE_ID_GROUND
]

BUSH_IDS = [
    1, 2, 5, 6, 7
]

COIN_IDS = [
    1, 2, 3
]

CRATES = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
]

GEMS = [
    1, 2, 3, 4, 5, 6, 7, 8
]

JUMP_BLOCKS = []

KEYS = [
    1, 2, 3, 4
]

LOCKS = [
    5, 6, 7, 8
]

POLES = [
    1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 15, 19, 20, 21, 22, 23, 24
]

FLAGS = [
    7, 8, 9, 16, 17, 18, 25, 26, 27, 34, 35, 36
]

for i in range(30):
    JUMP_BLOCKS.append(i)