import subprocess
import pyautogui
from pynput.keyboard import Key, Controller
from GymCustomEnv.customEnv import CustomEnv
import keyboard
import time

from GymCustomEnv.deepQLearning import DQNAgent

def main():
    env = CustomEnv()
    space_shape = env.observation_space.shape

    agent = DQNAgent (space_shape[0]*space_shape[1]*space_shape[2], env.action_space.n)
    agent.load_model('model.pth')

    state = env.reset()      
    done = False

    finish = False
    
    batch_size = 4

    while True:
        while not done:
            if keyboard.is_pressed('q'):
                finish = True
                break

            action = agent.choose_action(state)
            with open('actions.txt', 'a') as f:
                f.write(str(action) + '\n')
            observation, reward, done, info = env.step(action)
            agent.remember(state, action, reward, observation, done)
            state = observation

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

            env.render()

        if finish:
            break

        state = env.reset()
        done = False

    agent.update_target_network()

    agent.save_model('model.pth')
    env.close()

if __name__ == "__main__":  
    main()