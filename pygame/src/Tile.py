from src import constants, Dependencies
import pygame

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

    def collidable(self):
        if self.id == 2:
                return True

        return False

    def render(self, surf, screen):
        if self.id == 4:
            return

        surf.blit(Dependencies.gFrames['tiles'][self.id], ((self.x - 1) * 16, (self.y - 1) * 16))

        if self.topper:
            surf.blit(Dependencies.gFrames['toppers'][self.id], ((self.x - 1) * 16, (self.y - 1) * 16))