import subprocess
import pyautogui
from pynput.keyboard import Key, Controller
from GymCustomEnv.customEnv import CustomEnv
import time

def main():
    game_cmd = ['C:\\Program Files\\LOVE\\love.exe', 'game']
    game_process = subprocess.Popen(game_cmd)

    time.sleep(3)

    env = CustomEnv()
    observation = env.reset()      
    done = False
    time.sleep(3)
    print("sleep over")
    keyboard = Controller()
    keyboard.press(Key.up)
    time.sleep(0.5)
    keyboard.release(Key.up)
    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        #env.render()
    env.close()

if __name__ == "__main__":  
    main()