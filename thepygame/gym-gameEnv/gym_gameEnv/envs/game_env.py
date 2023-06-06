import gym
import pygame
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

#from flappyGame import FlappyBirdGame  # Import your Flappy Bird game class


class GameEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, game_env):
        pass

    def step(self, action):
        pass

    def reset(self):
        # Reset the game
        pass

    def render(self):
        # Render the game (if needed)
        pass

    def close(self):
        pass
