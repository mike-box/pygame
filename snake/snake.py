import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque

LIGHT = (100, 100, 100)
DARK = (200, 200, 200)      # 蛇的颜色
BLACK = (0, 0, 0)           # 网格线颜色
RED = (200, 30, 30)         # 红色，GAME OVER 的字体颜色
BGCOLOR = (40, 40, 60)      # 背景色
GAMEOVER = 0
GAMERUN = 1

class Snake:
    def __init__(self,w,h):
        self.speed = 0.1
        self.snake = [(0,0)]
        self.body = set(self.snake)
        self.head = (0,0)
        self.direction = 'R'
        self.snakeColor = DARK
        self.foodColor = RED
        self.foods = set()
        self.state = GAMERUN
        self.score = 0
        self.w = w
        self.h = h
        #initial add 10 foods
        self.add_food()

    def set_snake_color(self,rgb):
        self.color = rgb


    def set_snake_direction(self,dir):
        if (dir == 'L' and self.direction == 'R') or \
           (dir == 'R' and self.direction == 'L') or \
           (dir == 'U' and self.direction == 'D') or \
           (dir == 'D' and self.direction == 'U'):
           return False
        self.direction = dir

    def get_score(self):
        return len(self.snake) - 1

    def snake_move(self):
        d = {"L":(0,-1),"R":(0,1),"U":(-1,0),"D":(1,0)}
        x = self.head[0] + d[self.direction][0]
        y = self.head[1] + d[self.direction][1]

        if x < 0 or y < 0 or  x >= self.h or y >= self.w:
            self.state = GAMEOVER
            self.scroe = -1
            return -1

        curr = (x,y)
        self.head = (x,y)
        self.snake.append(curr)

        if len(self.foods) > 0 and curr in self.foods:
            self.foods.remove(curr)
            self.body.add(curr)
        else:
            self.body.remove(self.snake[0])
            self.snake.pop(0)
            if curr in self.body:
                self.state = GAMEOVER
                self.scroe = -1
                return -1
            else:
                self.body.add(curr)

        if len(self.foods) == 0:
            self.add_food()

        return len(self.snake)-1

    def add_food(self):
        nums = random.randint(1,10)
        for i in range(nums):
            self.foods.add(self.creat_food())

    def creat_food(self):
        food_x = random.randint(0,self.h)
        food_y = random.randint(0,self.w)
        while (food_x, food_y) in self.body or (food_x, food_y)  in self.foods:
            # 如果食物出现在蛇身上 ，则重来
            food_x = random.randint(0,self.w)
            food_y = random.randint(0,self.h)

        return (food_x,food_y)

class Game:
    def __init__(self,w,h,sz = 20):
        self.width = w
        self.high = h
        self.textHigh = 2
        self.sz = sz
        self.line = 1
        self.backGround = BGCOLOR
        self.snakeColor = DARK
        self.foodColor = RED
        self.textColor = RED
        self.state = GAMERUN
        self.score = 0
        self.speed = 1.0
        self.last_move_time = time.time()
        self.snake = Snake(w,h-self.textHigh)

        #init game
        pygame.init()
        self.screen = pygame.display.set_mode((w*sz, h*sz))
        pygame.display.set_caption('Gluttonous snake')
        self.font1 = pygame.font.SysFont('SimHei', 24)  # 得分的字体
        self.font2 = pygame.font.SysFont('arial', 72)  # GAME OVER 的字体

    def text_draw(self):
        imgText = self.font1.render(f'speed: {int(1/self.speed)}',True,pygame.Color(255, 255, 255))
        self.screen.blit(imgText,(160,10))
        imgText = self.font1.render(f'score: {self.score}',True,pygame.Color(255, 255, 255))
        self.screen.blit(imgText,(self.width*self.sz-160,10))

    def game_draw(self):
        self.screen_draw()
        self.snake_draw()
        self.food_draw()
        self.line_draw()
        self.text_draw()

    def speed_up(self):
        if self.speed < 0.1:
            return
        self.speed = self.speed - 0.05

    def speed_down(self):
        self.speed = self.speed + 0.05

    # set background
    def screen_draw(self):
        self.screen.fill(self.backGround)        

    # set snake
    def snake_draw(self):
        for x,y in self.snake.body:
            pygame.draw.rect(self.screen,self.snakeColor,(y*self.sz,(x+self.textHigh)*self.sz,self.sz,self.sz),0)

    # line draw
    def line_draw(self):
        pygame.draw.rect(self.screen,LIGHT,(0,0,self.width*self.sz,self.textHigh*self.sz),0)
        for x in range(self.width):
            p1 = (x*self.sz,self.textHigh*self.sz)
            p2 = (x*self.sz, self.high*self.sz)
            pygame.draw.line(self.screen, BLACK,p1, p2, 1)
        for y in range(self.textHigh,self.high):
            p1 = (0,y*self.sz)
            p2 = (self.width*self.sz, y*self.sz)
            pygame.draw.line(self.screen, BLACK, p1, p2, 1)

    # set food
    def food_draw(self):
        for (x,y) in self.snake.foods:
            pygame.draw.rect(self.screen,self.foodColor,(y*self.sz,(x+self.textHigh)*self.sz,self.sz,self.sz),0)

    # set screen
    def scree_update(self):
        pygame.display.update()
    
    def game_over(self):
        imgText = self.font2.render(f'game over',True,pygame.Color(200,30,30))
        self.screen.blit(imgText,(self.width/2*self.sz-100,self.high/2*self.sz))
    
    def run(self):
        while True:
            self.game_draw()
            self.scree_update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key in (K_w, K_UP):
                        self.snake.set_snake_direction('U')
                    elif event.key in (K_s, K_DOWN):
                        self.snake.set_snake_direction('D')
                    elif event.key in (K_a, K_LEFT):
                        self.snake.set_snake_direction('L')
                    elif event.key in (K_d, K_RIGHT):
                        self.snake.set_snake_direction('R')
                    elif event.key in (K_PLUS, K_EQUALS):
                        self.speed_up()
                    elif event.key in (K_MINUS,K_UNDERSCORE):
                        self.speed_down()
                
            if self.state is not GAMEOVER:
                curTime = time.time()
                if curTime - self.last_move_time > self.speed:
                    res = self.snake.snake_move()
                    if res < 0:
                        self.state = GAMEOVER
                    else:
                        self.last_move_time = curTime
                        self.score = res 

            if self.state == GAMEOVER:
                self.game_over()
                self.scree_update()

game = Game(40,30)
game.run()