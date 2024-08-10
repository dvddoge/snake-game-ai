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
        self.reset()
        
    def _place_food(self):
        x = random.randint(0, (dis_width-snake_block)//snake_block)*snake_block
        y = random.randint(0, (dis_height-snake_block)//snake_block)*snake_block
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

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

    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > dis_width - snake_block or pt.x < 0 or pt.y > dis_height - snake_block or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self._move(action)
        self.snake.insert(0, self.head)
        
        reward = 0
        game_over = False
        if self._is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        self.render()
        clock.tick(snake_speed)
        
        return reward, game_over, self.score

    def render(self):
        dis.fill(white)
        for pt in self.snake:
            pygame.draw.rect(dis, blue, pygame.Rect(pt.x, pt.y, snake_block, snake_block))
            pygame.draw.rect(dis, green, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        pygame.draw.rect(dis, red, pygame.Rect(self.food.x, self.food.y, snake_block, snake_block))
        
        text = font.render("Score: " + str(self.score), True, black)
        dis.blit(text, [0, 0])
        pygame.display.flip()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(dis_width/2, dis_height/2)
        self.snake = [self.head, 
                      Point(self.head.x-snake_block, self.head.y),
                      Point(self.head.x-(2*snake_block), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0