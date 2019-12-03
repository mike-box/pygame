"""贪吃蛇"""
import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque

LIGHT = (100, 100, 100)     # free 
DARK = (200, 200, 200)      # obstacle 
BLACK = (0, 0, 0)           # line
RED = (200, 30, 30)         # robot
BGCOLOR = (40, 40, 60)      # back
    
class Robot:
    def __init__(self,room,pos):
        self.w = len(room[0])
        self.h = len(room)
        self.robot = pos
        self.rooms = room
        self.direction = 'U'
        self.sz = 80
        self.speed = 1
        self.visited = set()
        self.lasttime = time.time()

        #color
        self.backGround = BGCOLOR
        self.robotColor = RED
        self.spaceColor = DARK
        self.obstacleColor = RED

        #init game
        pygame.init()
        self.screen = pygame.display.set_mode((self.w*self.sz, self.h*self.sz))
        pygame.display.set_caption('Robot')
        self.game_draw()
        self.clock = pygame.time.Clock()

    def clean_room(self):
        self.visited.add(str(0)+','+str(0))

        def dfsRobot(x,y,dir):
            d = [(-1,0),(0,-1),(1,0),(0,1)]
            self.robot_clean()

            for i in range(4):
                newDir = (dir+i)%4
                x1 = x + d[newDir][0]
                y1 = y + d[newDir][1]
                key = str(x1)+','+str(y1)

                if key not in self.visited and self.robot_move():
                    self.visited.add(key)
                    dfsRobot(x1,y1,newDir)
                    self.turn_left()
                    self.turn_left()
                    self.robot_move()
                    self.turn_left()
                    self.turn_left()
                
                self.turn_left()
        
        dfsRobot(0,0,0)
          
    def robot_move(self):
        d = {'L':(0,-1),'R':(0,1),'U':(-1,0),'D':(1,0)}
        x = self.robot[0] + d[self.direction][0]
        y = self.robot[1] + d[self.direction][1]

        if x < 0 or x >= self.h or y < 0 or y >= self.w:
            return False

        if self.rooms[x][y] == 0:
            return False
        
        self.robot = (x,y)
        self.game_draw()

        return True

    def robot_clean(self):
        self.rooms[self.robot[0]][self.robot[1]] = 1
        self.game_draw()

    def turn_left(self):
        left_change = {'L':'D','R':'U','U':'L','D':'R'}
        self.direction = left_change[self.direction]
        self.game_draw()
    
    def turn_right(self):
        right_change = {'L':'U','R':'U','U':'L','D':'R'}
        self.direction = 'R'
        self.game_draw()
    
    def room_draw(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.rooms[i][j] == 0:
                    pygame.draw.rect(self.screen,self.obstacleColor,(j*self.sz,i*self.sz,self.sz,self.sz),0)
                elif self.rooms[i][j] == 1:
                    pygame.draw.rect(self.screen,self.spaceColor,(j*self.sz,i*self.sz,self.sz,self.sz),0)
                elif self.rooms[i][j] == -1:
                    img = pygame.image.load("\\rush.bmp")
                    self.screen.blit(img,(j*self.sz,i*self.sz)) 

    def robot_delay(self):
        while True:
            for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()
            curTime = time.time()
            if curTime - self.lasttime > 0.5:
                self.lasttime = curTime
                break
            self.clock.tick(100)

    # set robot
    def robot_draw(self):
        d = {'U':0,'L':90,'D':180,'R':270}
        img = pygame.image.load("\\robot.bmp")
        img = pygame.transform.rotate(img,d[self.direction])
        pos = self.robot
        self.screen.blit(img,(pos[1]*self.sz,pos[0]*self.sz))
        #pygame.draw.rect(self.screen,self.robotColor,(pos[1]*self.sz,pos[0]*self.sz,self.sz,self.sz),0)

    def game_draw(self):
        self.robot_delay()
        self.screen_draw()
        self.room_draw()
        self.robot_draw()
        self.line_draw()
        pygame.display.update()

    def speed_up(self):
        if self.speed < 0.1:
            return
        self.speed = self.speed - 0.05

    def speed_down(self):
        self.speed = self.speed + 0.05

    # set background
    def screen_draw(self):
        self.screen.fill(self.backGround)

    # line draw
    def line_draw(self):
        for x in range(self.w):
            p1 = (x*self.sz,0)
            p2 = (x*self.sz, self.h*self.sz)
            pygame.draw.line(self.screen, BLACK,p1, p2, 1)
        for y in range(self.h):
            p1 = (0,y*self.sz)
            p2 = (self.w*self.sz, y*self.sz)
            pygame.draw.line(self.screen, BLACK, p1, p2, 1)

rooms = [[-1,1,-1,1,1,-1,1,1],[1,1,1,1,1,0,1,1],[1,0,1,1,1,-1,1,1],[0,0,0,1,0,0,0,0],[1,-1,-1,1,-1,1,-1,1]]
pos = (1,3)
rob = Robot(rooms,pos)
rob.clean_room()