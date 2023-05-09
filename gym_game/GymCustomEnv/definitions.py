import numpy as np
from enum import IntEnum, Enum


class Actions(IntEnum):
    NOOP = 0  # standing
    UP = 1  
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_RIGHT = 5
    UP_LEFT = 6
    DOWN_RIGHT = 7
    DOWN_LEFT = 8

