import torch
import random
import numpy as np
from collections import deque
from snakegame import SnakeGameAI, Direction, Point

MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def _init_(self):
        self.game = SnakeGameAI()

    def get_state(self, game):
        pass

    def select_action(self, state):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
