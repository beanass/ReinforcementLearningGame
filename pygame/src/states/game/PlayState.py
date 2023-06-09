from src.states import BaseState
from src.states.entity import PlayerIdleState, PlayerWalkingState, PlayerJumpState, PlayerFallingState
from src import LevelMaker, Player, StateMachine, Dependencies, constants
import random
import pygame

class PlayState(BaseState.BaseState):
    def __init__(self):
        self.camX = 0
        self.camY = 0
        self.background = 0
        self.level = None
        self.player = None
        self.tileMap = None
        self.gravityOn = True
        self.gravityAmount = 6

    def enter(self, params):
        self.background = random.randint(0, 2)
        if params['levelWidth']:
            self.level = LevelMaker.LevelMaker().generate(params['levelWidth'], 10)
        else:
            self.level = LevelMaker.LevelMaker().generate(100, 10)

        self.tileMap = self.level.tilemap

        playerStateMachine = StateMachine.StateMachine({
            'idle': lambda: PlayerIdleState.PlayerIdleState(self.player),
            'walking': lambda: PlayerWalkingState.PlayerWalkingState(self.player),
            'jump': lambda: PlayerJumpState.PlayerJumpState(self.player, self.gravityAmount),
            'falling': lambda: PlayerFallingState.PlayerFallingState(self.player, self.gravityAmount)
        })

        self.player = Player.Player(0, 0, 16, 20, 'green-alien', playerStateMachine, self.tileMap, self.level)

        if params['score']:
            self.player.score = params['score']

        self.spawnEnemies()

        self.player.changeState('falling', {})

    def exit(self):
        pass

    def update(self, dt):
        self.level.clear()

        self.player.update(dt)
        self.level.update(dt)
        self.updateCamera()

        if self.player.x <= 0:
            self.player.x = 0
        elif self.player.x >= self.tileMap.width * 16 - self.player.width:
            self.player.x = self.tileMap.width * 16 - self.player.width

    def render(self, surf, screen):
        surf.blit(Dependencies.gFrames["backgrounds"][self.background], (0, 0))
        surf.blit(Dependencies.gFrames["backgrounds"][self.background], (0, Dependencies.gFrames["backgrounds"][self.background].get_height() / 3 * 2))

        self.level.render(surf, screen)
        self.player.render(surf, screen)
        
        screen.blit(pygame.transform.scale(surf, (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)), (0, 0))

        pygame.display.update()

    def updateCamera(self):
        self.camX = max(0, min(16 * self.tileMap.width - constants.VIRTUAL_WIDTH, self.player.x - (constants.VIRTUAL_WIDTH / 2 - 8)))
        self.backgroundX = (self.camX / 3) % 256

    def spawnEnemies(self):
        pass