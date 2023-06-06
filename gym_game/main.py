import subprocess
import pyautogui
from pynput.keyboard import Key, Controller
from GymCustomEnv.customEnv import CustomEnv
import time

from GymCustomEnv.deepQLearning import build_model, DQNAgent

def main():
    env = CustomEnv()
    state = env.reset()      
    done = False

    space_shape = env.observation_space.shape

    model = build_model(space_shape[0]*space_shape[1]*space_shape[2], env.action_space.n)
    agent = DQNAgent (space_shape[0]*space_shape[1]*space_shape[2], env.action_space.n)
    #agent.load_model('model.pth')
    
    batch_size = 4

    while not done:
        # action = env.action_space.sample()
        action = agent.choose_action(state)
        observation, reward, done, info = env.step(action)
        agent.remember(state, action, reward, observation, done)
        state = observation

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
    agent.update_target_network()
        #env.render()
    agent.save_model('model.pth')
    env.close()

if __name__ == "__main__":  
    main()