import subprocess
import pyautogui
from pynput.keyboard import Key, Controller
from GymCustomEnv.customEnv import CustomEnv
from gym import spaces
import keyboard
import time
import numpy as np

from GymCustomEnv.deepQLearning import DQNAgent

def get_input_shape(observation_space):
    input_shape = 0
    for space in observation_space.values():
        if isinstance(space, spaces.Dict):
            for sub_space in space.spaces.values():
                if isinstance(sub_space, spaces.Box):
                    input_shape += np.prod(sub_space.shape)
                elif isinstance(sub_space, spaces.MultiBinary):
                    input_shape += np.product(sub_space.shape)
        elif isinstance(space, spaces.Box):
            input_shape += np.prod(space.shape)
        elif isinstance(space, spaces.MultiBinary):
            input_shape += np.product(space.shape)

    return input_shape

def main():
    train = True

    env = CustomEnv()
    #space_shape = env.observation_space.shape

    input_shape = get_input_shape(env.observation_space)

    agent = DQNAgent (input_shape, env.action_space.n, train)
    agent.load_model('model.pth')

    state = env.reset()
    done = False

    finish = False
    
    batch_size = 10

    while True:
        while not done:
            if keyboard.is_pressed('q'):
                finish = True
                break

            action = agent.choose_action(state)

            observation, reward, done, info = env.step(action)

            if train:
                with open('actions.txt', 'a') as f:
                    f.write(str(action) + '\n')
                agent.remember(state, action, reward, observation, done)

                if len(agent.memory) > batch_size:
                    agent.replay(batch_size)

            state = observation

            env.render()

        if finish:
            break

        agent.update_target_network()

        state = env.reset()
        done = False

    if train:
        agent.update_target_network()
        agent.save_model('model.pth')
        
    env.close()

if __name__ == "__main__":  
    main()