import subprocess
import pyautogui
from pynput.keyboard import Key, Controller
from GymCustomEnv.customEnv import CustomEnv
import time

from GymCustomEnv.deepQLearning import build_model

def main():
    env = CustomEnv()
    observation = env.reset()      
    done = False

    model = build_model(len(env.observation_space), env.action_space.n)
    #model = QNetwork(len(env.observation_space), env.action_space.n)

    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        #env.render()
    env.close()

if __name__ == "__main__":  
    main()