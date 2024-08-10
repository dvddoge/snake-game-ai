import pygame
from enum import Enum
import random
from collections import namedtuple
import numpy as np

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Jogo da Cobrinha')

font = pygame.font.SysFont("Arial", 24)

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

frame_iteration = 0

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

class SnakeGameAI:
    def __init__(self):
        self.direction = Direction.RIGHT
        self.head = Point(dis_width / 2, dis_height / 2)
        self.snake = [self.head]
        self.length_of_snake = 1
        self.food = None
        self.score = 0
        self._place_food()
        
    def _place_food(self):
        self.food = Point(
            round(random.randrange(0, dis_width - snake_block) / 10) * 10,
            round(random.randrange(0, dis_height - snake_block) / 10) * 10
        )

    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += snake_block
        elif self.direction == Direction.LEFT:
            x -= snake_block
        elif self.direction == Direction.DOWN:
            y += snake_block
        elif self.direction == Direction.UP:
            y -= snake_block

        self.head = Point(x, y)
        return self.head

    def _is_collision(self, point=None):
        if self.head.x >= dis_width or self.head.x < 0 or self.head.y >= dis_height or self.head.y < 0:
            return True
        elif self.head in self.snake[1:]:
            return True
        else:
            return False

    def play_step(self, action):
        self._move(action)
        self.snake.append(self.head)
        if len(self.snake) > self.length_of_snake:
            del self.snake[0]

        if self._is_collision():
            return -10, True, self.score
        
        reward = 0
        if(self.head) == self.food:
            self.length_of_snake += 1
            self.score += 1
            reward = 10
            self._place_food()

        return reward, False, self.score
    
    def render(self):
        dis.fill(white)
        for point in self.snake:
            pygame.draw.rect(dis, black, [point.x, point.y, snake_block, snake_block])
        pygame.draw.rect(dis, green, [self.food.x, self.food.y, snake_block, snake_block])
        text = font.render("Score: " + str(self.score), True, red)
        dis.blit(text, [0, 0])
        pygame.display.flip()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(dis_width / 2, dis_height / 2)
        self.snake = [self.head]
        self.length_of_snake = 1
        self.food = None
        self.score = 0
        self._place_food()
