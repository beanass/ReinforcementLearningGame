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
        '''{"entities":[
            {"currentAnimation":
             {"currentFrame":2,"frames":[49,50],"interval":0.5,"timer":0.4955933},
             "direction":"right","dx":0,"dy":0,"height":16,"texture":"creatures","width":16,"x":865.660705,"y":82},
             {"currentAnimation":{"currentFrame":1,"frames":[51],"interval":1,"timer":0},
              "direction":"right","dx":0,"dy":0,"height":16,"texture":"creatures","width":16,"x":1097.888309,"y":50},
              {"currentAnimation":{"currentFrame":2,"frames":[49,50],"interval":0.5,"timer":0.4955933},
               "direction":"left","dx":0,"dy":0,"height":16,"texture":"creatures","width":16,"x":1246.251543,"y":82}],
               
               "objects":[{"collidable":false,"frame":13,"height":16,"texture":"bushes","width":16,"x":96,"y":80},
                          {"collidable":true,"consumable":true,"frame":1,"height":16,"key":true,"solid":false,"texture":"keys-and-locks","width":16,"x":336,"y":80},
                          {"collidable":false,"frame":16,"height":16,"texture":"bushes","width":16,"x":352,"y":80},
                          {"collidable":true,"frame":22,"height":16,"hit":false,"solid":true,"texture":"jump-blocks","width":16,"x":432,"y":48},
                          {"collidable":true,"frame":9,"height":16,"hit":false,"solid":true,"texture":"jump-blocks","width":16,"x":448,"y":48},
                          {"collidable":true,"frame":19,"height":16,"hit":false,"solid":true,"texture":"jump-blocks","width":16,"x":512,"y":16},
                          {"collidable":false,"frame":5,"height":16,"texture":"bushes","width":16,"x":624,"y":80},
                          {"collidable":true,"frame":11,"height":16,"hit":false,"solid":true,"texture":"jump-blocks","width":16,"x":880,"y":48},
                          {"collidable":false,"frame":21,"height":16,"texture":"bushes","width":16,"x":944,"y":80},
                          {"collidable":false,"frame":23,"height":16,"texture":"bushes","width":16,"x":992,"y":80},
                          {"collidable":true,"frame":12,"height":16,"hit":false,"solid":true,"texture":"jump-blocks","width":16,"x":1072,"y":48},
                          {"collidable":true,"frame":12,"height":16,"hit":false,"solid":true,"texture":"jump-blocks","width":16,"x":1088,"y":16},
                          {"collidable":true,"consumable":true,"frame":5,"height":16,"key":false,"solid":false,"texture":"keys-and-locks","width":16,"x":1280,"y":80},
                          {"collidable":false,"frame":21,"height":16,"texture":"bushes","width":16,"x":1392,"y":80},
                          {"collidable":true,"frame":26,"height":16,"hit":false,"solid":true,"texture":"jump-blocks","width":16,"x":1440,"y":48},
                          {"collidable":true,"frame":19,"height":16,"hit":false,"solid":true,"texture":"jump-blocks","width":16,"x":1504,"y":48},
                          {"collidable":false,"frame":20,"height":16,"texture":"bushes","width":16,"x":1584,"y":80}],
                          
                "player":{"consumingKey":false,"currentAnimation":
                          {"currentFrame":1,"frames":[3],"interval":1,"timer":0},
                          "direction":"right","dx":0,"dy":-60,"height":20,"key":0,"score":100,"texture":"green-alien","width":16,"x":1.8670499999999,"y":14.2447888},
                          "tileMatrix":[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        [0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                                        [0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],16]}'''
        # JSON to observation!!
        return 0

    def render(self):
        pass

    def close(self):
        # Terminate the socket process
        self.socket.close()
