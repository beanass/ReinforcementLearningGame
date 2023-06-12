import json
import socket
import subprocess
import time
from gym import Env
from gym import spaces
import numpy as np
from pynput.keyboard import Key, Controller
from PIL import ImageGrab, Image, ImageFilter
import pytesseract
import win32gui
from .pythongame import SuperBros
import pygame

class CustomEnv(Env):

    def __init__(self):
        """initialize environment"""
        super(CustomEnv, self).__init__()

        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

        #game_cmd = ['C:\\Program Files\\LOVE\\love.exe', 'game']
        #self.game_process = subprocess.Popen(game_cmd)
        self.game = SuperBros.SuperBros()
        self.game.on_init()
        #time.sleep(3)
        #print("sleep over")
        keyboard = Controller()
        keyboard.press(Key.down)
        keyboard.release(Key.down)

        # actions: left,right,up
        self.action_space = spaces.Discrete(6)
        # data we get from the game
        '''self.observation_space = spaces.Dict({
            "entities": spaces.MultiDiscrete([1000] * 40),  # dx, dy, x, y
            "objects": spaces.MultiDiscrete([1000] * 70),  # x, y
            "player": spaces.MultiDiscrete([1000] * 5),  # dx, dy, score, x, y
            "tileMatrix": spaces.MultiDiscrete([2] * 200)  # 10x20 tile matrix with binary values
        })'''

        self.observation_space = spaces.Box(low=0, high=255, shape=(144, 256, 3), dtype=np.uint8)

        # socket
        #self.HOST = '127.0.0.1'
        #self.PORT = 8080
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.connect((self.HOST, self.PORT))

        # Initialize variables for stdout and stderr
        self.stdout = None
        self.stderr = None
        self.keyboard = Controller()
        #reward vars
        self.temp_score = 0
        self.temp_x = 0

        self.hwnd = win32gui.FindWindow(None, r'Super 50 Bros.')
        win32gui.SetForegroundWindow(self.hwnd)
        self.dimensions = win32gui.GetWindowRect(self.hwnd)

    def __delete__(self):
        """initialize environment"""
        #self.game_process.kill()
        #self.socket_process.kill()

    def reset(self):
        """reset environment"""
        # Reset the environment to its initial state
        self.game = SuperBros.SuperBros()
        self.game.on_init()
        self.temp_level = 0
        self.temp_score = 0
        self.temp_x = 0
        self.done = False
        return None
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

        observation, text = self._process_observation()
        reward = self._calculate_reward(text)
        if text == 'Super':
            done = True
        else:
            done = False 
        info = {}  # Additional information

        return observation, reward, done, info

    def _calculate_reward(self, text):
        reward = 0
        if self.game.player.score > self.temp_score:
            reward += 0.5
        elif self.game.player.score < self.temp_score:
            reward -= 0.5
        if self.game.player.x > self.temp_x:
            reward += 10
        elif self.game.player.x == self.temp_x:
            reward -= 0.5
        elif self.game.player.x < self.temp_x:
            reward -= 5

        if text == 'Super':
            reward -= 1000

        self.temp_score = self.game.player.score
        self.temp_x = self.game.player.x

        print(reward)

        return reward

    def _process_observation(self):
        image = ImageGrab.grab(self.dimensions)
        im1 = image.crop((8, 39, 1288, 759))

        im2 = image.crop((60, 180, 520, 340))
        im2 = im2.convert('L')
        im2 = im2.filter(ImageFilter.MedianFilter())
        im2 = im2.point(lambda x: 0 if x < 240 else 255)
        text = pytesseract.image_to_string(im2).split('\n')[0]

        im1 = im1.resize((256, 144))
        observation = np.array(im1)

        return observation, text

    def walk(self, direction):
        #const_fps = 1./30 # change movement duration here
        # walk right
        if direction == 0:
            self.keyboard.press(Key.right)
        # walk left
        elif direction == 1:
            self.keyboard.press(Key.left)
        # jump
        elif direction == 2:
            self.keyboard.press(Key.up)
            self.keyboard.release(Key.up)
        elif direction == 3:
            self.keyboard.release(Key.right)
        elif direction == 4:
            self.keyboard.release(Key.left)
        elif direction == 5:
            self.keyboard.release(Key.left)
            self.keyboard.release(Key.right)

    def render(self):
        self.game.on_render()

    def close(self):
        # Terminate the socket process
        pygame.quit()
