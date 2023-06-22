import json
import socket
import subprocess
import time
from gym import Env
from gym import spaces
import numpy as np
from pynput.keyboard import Key, Controller
from PIL import ImageGrab, Image, ImageFilter, ImageOps
import win32gui
from .pythongame import SuperBros
import pygame

class CustomEnv(Env):

    def __init__(self):
        """initialize environment"""
        super(CustomEnv, self).__init__()

        self.game = SuperBros.SuperBros()
        self.game.on_init()
        
        self.action_space = spaces.Discrete(4)

        #self.observation_space = spaces.Box(low=0, high=255, shape=(144, 256, 1), dtype=np.uint8)
        self.observation_space = spaces.Dict({
            'tiles': spaces.MultiBinary([9, 16]),
            'playerX': spaces.Box(low=np.array([0]), high=np.array([100*16]), shape=(1,), dtype=np.float32),
            'playerY': spaces.Box(low=np.array([0]), high=np.array([9*16]), shape=(1,), dtype=np.float32),
            'nextEnemyX': spaces.Box(low=np.array([-100*16]), high=np.array([100*16]), shape=(1,), dtype=np.float32),
            'nextEnemyY': spaces.Box(low=np.array([-9*16]), high=np.array([9*16]), shape=(1,), dtype=np.float32),
            'keyX': spaces.Box(low=np.array([-100*16]), high=np.array([100*16]), shape=(1,), dtype=np.float32),
            'lockX': spaces.Box(low=np.array([-100*16]), high=np.array([100*16]), shape=(1,), dtype=np.float32),
            'key': spaces.MultiBinary([1]),
            'lock': spaces.MultiBinary([1]),
            'dead': spaces.MultiBinary([1]),
            'score': spaces.Box(low=np.array([0]), high=np.array([np.inf]), shape=(1,), dtype=np.float32)
        })

        # Initialize variables for stdout and stderr
        self.keyboard = Controller()

        #self.hwnd = win32gui.FindWindow(None, r'Super 50 Bros.')
        #win32gui.SetForegroundWindow(self.hwnd)
        #self.dimensions = win32gui.GetWindowRect(self.hwnd)

    def __delete__(self):
        """initialize environment"""
        #self.game_process.kill()
        #self.socket_process.kill()

    def reset(self):
        """reset environment"""
        # Reset the environment to its initial state
        self.keyboard.release(Key.right)
        self.keyboard.release(Key.left)

        self.game.on_init()

        self.keyboard.press(Key.down)
        self.keyboard.release(Key.down)

        self.temp_score = 0
        self.temp_x = 0
        self.highest_x = 0
        self.highest_level = 0
        self.x_timer = time.time()
        self.done = False
        self.got_key = False
        self.got_lock = False

        #image = ImageGrab.grab(self.dimensions)
        #im1 = image.crop((8, 39, 1288, 759))

        #im1 = im1.resize((256, 144))
        #im1 = im1.convert('L')
        #state = np.array(im1)

        state = self._process_observation()

        return state
        #self._receive_data()
        #return self._process_observation()

    def step(self, action):
        """this function defines what to do in every step"""
        # Take a step in the environment based on the action
        # ... perform action and receive data from the socket ...
        self.walk(action)

        for event in pygame.event.get():
            self.game.on_event(event)
        self.game.on_loop()

        observation = self._process_observation()
        reward = self._calculate_reward()
        done = self.done
        info = {}  # Additional information

        return observation, reward, done, info

    def _calculate_reward(self):
        reward = 0
        if self.game.player.score > self.temp_score:
            reward += 1

        if self.game.player.x > self.temp_x and ((not self.got_key and self.game.player.x < self.game.keyX) or self.got_key) and ((not self.got_lock and self.game.player.x < self.game.lockX) or self.got_lock):
            reward += 10
        elif self.game.player.x == self.temp_x:
            reward -= 3
        elif self.game.player.x < self.temp_x:
            reward -= 5
        if not self.got_key and self.game.player.x > self.game.keyX:
            reward -= 10
        if not self.got_lock and self.game.player.x > self.game.lockX:
            reward -= 10
        if self.game.player.key and not self.got_key:
            self.got_key = True
            reward += 50
        if self.game.player.lock and not self.got_lock:
            self.got_lock = True
            reward += 50

        if self.game.player.dead:
            reward -= 50

        if time.time() - self.x_timer > 20:
            reward -= 50
            self.done = True

        if self.game.player.dead:
            self.done = True

        self.temp_score = self.game.player.score
        self.temp_x = self.game.player.x

        if self.game.player.x > self.highest_x:
            self.highest_x = self.game.player.x
            self.x_timer = time.time()

        if self.game.levelcount > self.highest_level:
            self.highest_level = self.game.levelcount
            self.highest_x = 0
            self.x_timer = time.time()

        return reward

    def _process_observation(self):
        #image = ImageGrab.grab(self.dimensions)
        #im1 = image.crop((8, 39, 1288, 759))

        #im1 = im1.resize((256, 144))
        #im1 = im1.convert('L')
        #observation = np.array(im1)

        observation = {
            'tiles': self.game.get_tile_observation(),
            'playerX': self.game.player.x,
            'playerY': self.game.player.y,
            'nextEnemyX': self.game.get_next_enemyX(),
            'nextEnemyY': self.game.get_next_enemyY(),
            'keyX': self.game.keyX - self.game.player.x,
            'lockX': self.game.lockX - self.game.player.x,
            'key': self.game.player.key,
            'lock': self.game.player.lock,
            'dead': self.game.player.dead,
            'score': self.game.player.score
        }

        print(observation['nextEnemyX'])

        return observation

    def walk(self, direction):
        # walk right
        if direction == 0:
            self.keyboard.release(Key.left)
            self.keyboard.press(Key.right)
        # walk left
        elif direction == 1:
            self.keyboard.release(Key.right)
            self.keyboard.press(Key.left)
        # jump
        elif direction == 2:
            self.keyboard.press(Key.up)
            self.keyboard.release(Key.up)
        elif direction == 3:
            self.keyboard.release(Key.right)
            self.keyboard.release(Key.left)

    def render(self):
        self.game.on_render()

    def close(self):
        # Terminate the socket process
        pygame.quit()
