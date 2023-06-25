import random
import numpy as np
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from torch import nn
from torch.autograd import Variable

class DQNAgent:
    def __init__(self, state_shape, action_space, train = True):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(self.device)

        self.state_shape = state_shape
        self.action_space = action_space

        self.gamma = 0.6  # Discount factor
        if train:
            self.epsilon = 1.0  # Exploration factor
        else:
            self.epsilon = 0.01
        self.epsilon_decay = 0.99  # Decay rate for exploration factor
        self.epsilon_min = 0.01  # Minimum exploration factor
        self.memory = []  # Replay memory

        # Build the Q-network
        self.q_network = self.build_q_network()
        self.q_network.train()
        self.target_network = self.build_q_network()
        self.update_target_network()

        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

    def build_q_network(self):
        model = nn.Sequential(
            nn.Linear(self.state_shape, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, self.action_space)
        )
        model.to(self.device)
        return model

    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

    def get_tensor_from_state(self, state):
        input_tensors = []

        for key, value in state.items():
            if key == 'tiles':
                np_value = np.array(value)
                tensor_value = torch.tensor(np_value, dtype=torch.float32)
            elif key == 'score' or key == 'lock' or key == 'key' or key == 'dead':
                tensor_value = torch.tensor(value, dtype=torch.float32).view(-1)
            elif key == 'playerX':
                tensor_value = torch.tensor((value - (100*8)) / (100*16), dtype=torch.float32).view(-1)
            elif key == 'playerY':
                tensor_value = torch.tensor((value - (9*8)) / (9*16), dtype=torch.float32).view(-1)
            elif key == 'nextEnemyX' or key == 'keyX' or key == 'lockX':
                tensor_value = torch.tensor(value / (200*16), dtype=torch.float32).view(-1)
            elif key == 'nextEnemyY':
                tensor_value = torch.tensor(value / (18*16), dtype=torch.float32).view(-1)

            input_tensors.append(tensor_value)

        input_tensor = torch.cat(input_tensors, dim=0)
        return input_tensor.to(self.device)

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            action = np.random.randint(self.action_space)
        else:
            with torch.no_grad():
                #state = state.flatten()
                #state_tensor = torch.FloatTensor(state).to(self.device)
                state_tensor = self.get_tensor_from_state(state)
                q_values = self.q_network(state_tensor)
                with open('q_values.txt', 'a') as f:
                    f.write(str(q_values.cpu().numpy()) + '\n')
                action = torch.argmax(q_values).item()
        return action

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        batch = np.random.choice(len(self.memory), batch_size, replace=False)
        states, targets = [], []
        for idx in batch:
            state, action, reward, next_state, done = self.memory[idx]
            if state is None or next_state is None:
                continue
            #state = state.flatten()
            #states.append(state)

            #state_tensor = torch.FloatTensor(state).to(self.device)
            state_tensor = self.get_tensor_from_state(state)
            states.append(state_tensor.cpu().numpy())
            q_values = self.q_network(state_tensor).detach().cpu().numpy()
            if done:
                q_values[action] = reward
            else:
                #next_state = next_state.flatten()
                #next_state_tensor = torch.FloatTensor(next_state).to(self.device)
                next_state_tensor = self.get_tensor_from_state(next_state)
                next_q_values = self.target_network(next_state_tensor).detach().cpu().numpy()
                q_values[action] = reward + self.gamma * np.max(next_q_values)
            targets.append(q_values)

        states = np.array(states)
        states = torch.FloatTensor(states).to(self.device)
        targets = np.array(targets)
        targets = torch.FloatTensor(targets).to(self.device)

        self.optimizer.zero_grad()
        outputs = self.q_network(states)
        loss = self.loss_fn(outputs, targets)
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, filepath):
        torch.save(self.q_network.state_dict(), filepath)

    def load_model(self, filepath):
        self.q_network.load_state_dict(torch.load(filepath))
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.epsilon = 0.01

