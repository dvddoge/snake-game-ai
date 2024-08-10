import torch
import random
import numpy as np
from collections import deque
from snakegame import SnakeGameAI, Direction, Point

MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
