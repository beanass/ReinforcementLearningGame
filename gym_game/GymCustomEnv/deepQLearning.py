import random
import numpy as np
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from torch import nn
from torch.autograd import Variable

def build_model(input_shape, num_actions):
    model = nn.Sequential(
        nn.Linear(input_shape, 24),
        nn.ReLU(),
        nn.Linear(24, 24),
        nn.ReLU(),
        nn.Linear(24, num_actions)
    )
    return model

class DQNAgent:
    def __init__(self, state_shape, action_space):
        self.state_shape = state_shape
        self.action_space = action_space

        self.gamma = 0.9  # Discount factor
        self.epsilon = 1.0  # Exploration factor
        self.epsilon_decay = 0.99  # Decay rate for exploration factor
        self.epsilon_min = 0.01  # Minimum exploration factor
        self.memory = []  # Replay memory

        # Build the Q-network
        self.q_network = self.build_q_network()
        self.target_network = self.build_q_network()
        self.update_target_network()

        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

    def build_q_network(self):
        model = nn.Sequential(
            nn.Linear(self.state_shape, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, self.action_space)
        )
        return model

    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            action = np.random.randint(self.action_space)
        else:
            with torch.no_grad():
                q_values = self.q_network(torch.FloatTensor(state))
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
            states.append(state)
            q_values = self.q_network(torch.FloatTensor(state)).detach().numpy()
            if done:
                q_values[action] = reward
            else:
                next_q_values = self.target_network(torch.FloatTensor(next_state)).detach().numpy()
                q_values[action] = reward + self.gamma * np.max(next_q_values)
            targets.append(q_values)

        states = torch.FloatTensor(states)
        targets = torch.FloatTensor(targets)

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
