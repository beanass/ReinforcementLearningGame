import gym
from gym import spaces
import numpy as np


class CustomEnv(gym.Env):

    def __init__(self, data_dict):


        self.observation_space = {}
        self.action_space = spaces.Discrete(9)

        self.data_dict = data_dict

    def reset(self):
        observation = 0 # still have to be define 
        return observation

    def step(self, action):
        observation = 0
        reward = 0
        done = 0
        info = 0
        return observation, reward, done, info

    #def render(self, mode='human'): 
