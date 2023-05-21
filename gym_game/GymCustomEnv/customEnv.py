import subprocess
from gym import Env
from gym import spaces
import numpy as np

class CustomEnv(Env):

    def __init__(self, data_dict):
        """initialize environment"""
        # actions: left,right,up
        self.action_space = spaces.Discrete(3)
        # data we get from the game
        self.observation_space = {}
        #self.game_cmd = ['C:\\Program Files\\LOVE\\love.exe', '..\\game']
        #self.game_socket_rcv = ['python', '..\\python\\socketpy.py']
        #self.game_process = subprocess.Popen(self.game_cmd)
        #self.socket_process = subprocess.Popen(self.game_socket_rcv)
        #self.observation_space = {}

    def __delete__(self):
        """initialize environment"""
        self.game_process.kill()
        self.socket_process.kill()

    def reset(self):
        """reset environment"""
        observation = 0 # still have to be define
        return observation

    def step(self, action):
        """this function defines what to do in every step"""
        self.Cu
        observation = 0
        reward = 0
        done = 0
        info = 0
        return observation, reward, done, info

    #def render(self, mode='human'): 
        """reset environment"""
