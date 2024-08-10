import torch
import random
import numpy as np
from collections import deque
from snakegame import SnakeGameAI, Direction, Point
from model import Lienar_QNet, QTrainer

MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def _init_(self):
        self.rounds = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MEMORY)
        self.model = Lienar_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        point_left = Point(head.x - 10, head.y)
        point_right = Point(head.x + 10, head.y)
        point_up = Point(head.x, head.y - 10)
        point_down = Point(head.x, head.y + 10)

        direction_left = game.direction == Direction.LEFT
        direction_right = game.direction == Direction.RIGHT
        direction_up = game.direction == Direction.UP
        direction_down = game.direction == Direction.DOWN

        state = [
            (direction_right and game.is_collision(point_right)) or
            (direction_left and game.is_collision(point_left)) or
            (direction_up and game.is_collision(point_up)) or
            (direction_down and game.is_collision(point_down)),

            (direction_up and game.is_collision(point_right)) or
            (direction_down and game.is_collision(point_left)) or
            (direction_left and game.is_collision(point_up)) or
            (direction_right and game.is_collision(point_down)),

            (direction_down and game.is_collision(point_right)) or
            (direction_up and game.is_collision(point_left)) or
            (direction_right and game.is_collision(point_up)) or
            (direction_left and game.is_collision(point_down)),

            direction_left,
            direction_right,
            direction_up,
            direction_down,

            game.food.x < game.head.x,  
            game.food.x > game.head.x,  
            game.food.y < game.head.y,  
            game.food.y > game.head.y  
        ]

        return np.array(state, dtype=int)

    def store_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def experience_replay(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory

        states, actions, rewards, next_states, dones = zip(*sample)
        self.trainer.train_batch(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_batch([state], [action], [reward], [next_state], [done])

    def get_action(self, state):
        self.epsilon = 80 - self.rounds
        move = [0, 0, 0]
        if random.uniform(0, 1) < self.epsilon / 200:
            move_index = random.choice([0, 1, 2])
            move[move_index] = 1
        else:
            state_tensor = torch.tensor(state, dtype=torch.float)
            predictions = self.model(state_tensor)
            best_move = torch.argmax(predictions).items()
            move[best_move] = 1

        return move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.store_memory(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.rounds += 1
            agent.experience_replay()

            if score > record:
                record = score
                agent.model.save()
            print('Game:', agent.rounds, 'Score:', score, 'Record:', record)

if __name__ == '__main__':
    train()