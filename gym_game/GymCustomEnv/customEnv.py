import json
import socket
import subprocess
import time
from gym import Env
from gym import spaces
import numpy as np
from pynput.keyboard import Key, Controller

class CustomEnv(Env):

    def __init__(self):
        """initialize environment"""
        super(CustomEnv, self).__init__()
        # actions: left,right,up
        self.action_space = spaces.Discrete(3)
        # data we get from the game
        self.observation_space = spaces.Discrete(10)        
        #self.game_cmd = ['C:\\Program Files\\LOVE\\love.exe', '..\\game']
        #self.game_process = subprocess.Popen(self.game_cmd)#

        #self.game_socket_rcv = ['python', 'python\\socketpy.py']
        #self.socket_process = subprocess.Popen(self.game_socket_rcv)
        self.HOST = '127.0.0.1'
        self.PORT = 8080
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.filename = 'game_state.json'
        # Initialize variables for stdout and stderr
        self.stdout = None
        self.stderr = None
        self.keyboard = Controller()

    def __delete__(self):
        """initialize environment"""
        self.game_process.kill()
        self.socket_process.kill()

    def reset(self):
        """reset environment"""
        # Reset the environment to its initial state
        #with open(self.filename, 'w', encoding='utf-8') as f:
        #    f.write('')
        self.done = False
        return 0
        #self._receive_data()
        #return self._process_observation()

    def step(self, action):
        """this function defines what to do in every step"""
        # Take a step in the environment based on the action
        # ... perform action and receive data from the socket ...
        if action == 0:
            self.keyboard.press(Key.right)
            time.sleep(1./60)
            self.keyboard.release(Key.right)
        elif action == 1:
            self.keyboard.press(Key.left)
            time.sleep(1./60)
            self.keyboard.release(Key.left)
        elif action == 2:
            self.keyboard.press(Key.up)
            time.sleep(1./60)
            self.keyboard.release(Key.up)
        data = self._receive_data()
        print(data)
        observation = self._process_observation()
        reward = 0  # Replace with your reward logic
        done = False  # Replace with your termination condition
        info = {}  # Additional information

        return observation, reward, done, info

    def _receive_data(self):
        # Receive data from the socket and store it in a JSON file
        while True:
            try:
                data = self.socket.recv(8192)
                return data
            except Exception as err:
                print(err)

    def _process_observation(self):
        # TODO: Process the current observation from the socket output
        '''{
            "entities":[{"dx":0,"dy":0,"x":224,"y":82},{"dx":0,"dy":0,"x":656,"y":82},{"dx":0,"dy":0,"x":736,"y":82},{"dx":0,"dy":0,"x":864,"y":82}],
            "objects":[{"texture":"jump-blocks","x":112,"y":48},{"texture":"keys-and-locks","x":368,"y":80},{"texture":"jump-blocks","x":1040,"y":48},
                        {"texture":"jump-blocks","x":1168,"y":48},{"texture":"keys-and-locks","x":1264,"y":80},{"texture":"jump-blocks","x":1456,"y":48},
                        {"texture":"jump-blocks","x":1568,"y":48}],
            "player":{"dx":0,"dy":0,"score":0,"x":0,"y":76},
            "tileMatrix":[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
                          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
                          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],16]}'''
        # JSON to observation!!
        return 0

    def render(self):
        pass

    def close(self):
        # Terminate the socket process
        self.socket.close()
