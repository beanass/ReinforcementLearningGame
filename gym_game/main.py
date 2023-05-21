import subprocess
import pyautogui
from pynput.keyboard import Key, Controller
from GymCustomEnv import *
from GymCustomEnv import customEnv
import time

def main():
    game_cmd = ['C:\\Program Files\\LOVE\\love.exe', 'game']
    #game_socket_rcv = ['python', 'python\\socketpy.py']
    game_process = subprocess.Popen(game_cmd)
    #socket_process = subprocess.Popen(game_socket_rcv)

    keyboard = Controller()
    time.sleep(5)
    print("Press Enter please!!!")
    #pyautogui.press('enter')
    #keyboard.press(Key.enter)
    #keyboard.release(Key.enter)
    time.sleep(1)
    keyboard.press(Key.right)
    #env = customEnv()
    #del game_process
    #del socket_process

if __name__ == "__main__":
    main()