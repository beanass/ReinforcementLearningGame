import random
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

class QNetwork(nn.Module):
    def __init__(self, input_shape, num_actions):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_shape, 24)
        self.fc2 = nn.Linear(24, 24)
        self.fc3 = nn.Linear(24, num_actions)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        q_values = self.fc3(x)
        return q_values