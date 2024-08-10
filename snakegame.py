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

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop(frame_iteration):
    game_over = False
    frame_iteration += 1

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0       
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        text = font.render("Score ", True, white)
        dis.blit(text, [dis_width / 2, dis_height / 2])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        reward = 0
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            frame_iteration = 0
            game_over = True
            
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head or frame_iteration > 100 * len(snake_list):
                frame_iteration = 0
                reward = -10
                game_over = True

        our_snake(snake_block, snake_list)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            reward = 10
            length_of_snake += 1

        clock.tick(snake_speed)

gameLoop(frame_iteration)
