"""
 Name: 连连看游戏
 Athor: mike-meng
 Email: mml1106@126.com
 Description: 连连看
"""

import sys, time
import math, random
import pygame
from pygame.locals import *

LIGHT = (255, 255, 255)     # free 
DARK = (200, 200, 200)      # obstacle 
BLACK = (0, 0, 0)           # line
RED = (200, 30, 30)         # robot
BGCOLOR = (40, 40, 60)      # back

class Grid:
    def __init__(self,width = 40,height = 40,max_key = 9):
        self.width = width
        self.height = height
        self.grid = [[0 for i in range(width)] for j in range(height)]
        self.max_key = max_key
        self.init_grid()
    
    def init_grid(self):
        for i in range(1,self.height-1):
            for j in range(1,self.width-1):
                self.grid[i][j] = random.randint(1,self.max_key)
    
    def set_grid(self,pos,keys):
        self.grid[pos[0]][pos[1]] = keys
    
    def get_grid(self,pos):
        return self.grid[pos[0]][pos[1]]
    
    def all_grid(self):
        return self.grid
    
    def check_connect(self,x,y):
        if x[0] < 0 or x[1] < 0 or x[0] >= self.height or x[1] >= self.width or\
           y[0] < 0 or y[1] < 0 or y[0] >= self.height or y[1] >= self.width:
            return False
        
        if x[0] != y[0] and x[1] != y[1]:
            return False

        #check row
        if x[0] == y[0]:
            for i in range(min(x[1],y[1])+1,max(x[1],y[1])):
                if self.grid[x[0]][i] > 0:
                    return False
        #check colum
        if x[1] == y[1]:
            for i in range(min(x[0],y[0])+1,max(x[0],y[0])):
                if self.grid[i][x[1]] > 0:
                    return False

        return True
    
    def mini_connect(self,x,y):
        res = []
        if self.grid[x[0]][x[1]] != self.grid[y[0]][y[1]]:
            return res

        #one step check
        if self.check_connect(x,y):
            res.append((x,y))
            return res

        #two step check
        if self.check_connect(x,(x[0],y[1])) and self.check_connect((x[0],y[1]),y):
            if self.grid[x[0]][y[1]] == 0:
                res.append((x,(x[0],y[1])))
                res.append(((x[0],y[1]),y))
                return  res
        if self.check_connect(x,(y[0],x[1])) and self.check_connect((y[0],x[1]),y):
            if self.grid[y[0]][x[1]] == 0:
                res.append((x,(y[0],x[1])))
                res.append(((y[0],x[1]),y))
                return  res

        #three step check
        for i in range(min(x[1],y[1])+1,max(x[1],y[1])):
            if self.check_connect(x,(x[0],i)) and self.grid[x[0]][i] == 0:
                if self.check_connect((x[0],i),(y[0],i)) and \
                   self.check_connect((y[0],i),y):
                    if self.grid[x[0]][i] == 0 and self.grid[y[0]][i] == 0:
                        res.append((x,(x[0],i)))
                        res.append(((x[0],i),(y[0],i)))
                        res.append(((y[0],i),y))
                        return res
        for i in range(min(x[0],y[0])+1,max(x[0],y[0])):
            if self.check_connect(x,(i,x[1])):
                print(i,x[1])
                if self.check_connect((i,x[1]),(i,y[1])) and \
                   self.check_connect((i,y[1]),y):
                    if self.grid[i][x[1]] == 0 and self.grid[i][y[1]] == 0:
                        res.append((x,(i,x[1])));
                        res.append(((i,x[1]),(i,y[1])));
                        res.append(((i,y[1]),y))
                        return res
        
        #check row
        for i in range(0,self.width):
            if self.check_connect(x,(x[0],i)):
                if self.check_connect((x[0],i),(y[0],i)) and \
                   self.check_connect((y[0],i),y):
                    if self.grid[x[0]][i] == 0 and self.grid[y[0]][i] == 0:
                        res.append((x,(x[0],i)))
                        res.append(((x[0],i),(y[0],i)))
                        res.append(((y[0],i),y))
                        return res
        #check colum
        for i in range(0,self.height):
            if self.check_connect(x,(i,x[1])):
                if self.check_connect((i,x[1]),(i,y[1])) and \
                   self.check_connect((i,y[1]),y):
                    if self.grid[i][x[1]] == 0 and self.grid[i][y[1]] == 0:
                        res.append((x,(i,x[1])));
                        res.append(((i,x[1]),(i,y[1])));
                        res.append(((i,y[1]),y))
                        return res
        
        return res

class Game:
    def __init__(self,width = 30,height = 30):
        self.width = width
        self.height = height
        self.element_num = 9
        self.grid = Grid(width,height,self.element_num)
        self.grid_size = 80
        self.score = 0
        self.element = []
        self.selected = (0,0)
        self.isSelect = False
        self.autoDetect = False

        #init game
        pygame.init()
        pygame.mixer.init()
        self.load_source()
        self.screen = pygame.display.set_mode((self.width*self.grid_size, self.height*self.grid_size))
        pygame.display.set_caption('linkmatching')
        self.clock = pygame.time.Clock()
        self.game_draw()

    def load_source(self):
        for i in range(1,self.element_num+1):
            image_file = "D:\\106\\element"+str(i)+".JPG"
            image = pygame.image.load(image_file)
            image = pygame.transform.scale(image,(self.grid_size,self.grid_size))
            self.element.append(image)

        return True

    def game_draw(self):
        self.screen_draw()
        self.picture_draw()
        self.border_draw()
        pygame.display.update()

    def screen_draw(self):
        self.screen.fill(LIGHT)
        return 0
    
    def picture_draw(self):
        arrays = self.grid.all_grid()
        for i in range(self.height):
            for j in range(self.width):
                if arrays[i][j] > 0:
                    self.screen.blit(self.element[arrays[i][j]-1],(j*self.grid_size,i*self.grid_size))

    def border_draw(self):
        for i in range(self.height):
            p1 = (self.grid_size,i*self.grid_size)
            p2 = ((self.width-1)*self.grid_size,i*self.grid_size)
            self.line_draw(p1,p2,LIGHT)
        for i in range(self.width):
            p1 = (i*self.grid_size,self.grid_size)
            p2 = (i*self.grid_size,(self.height-1)*self.grid_size)
            self.line_draw(p1,p2,LIGHT)

        # we will set the selected grid
        if self.isSelect:
            x = self.selected[0]
            y = self.selected[1]
            p1 = (x*self.grid_size,y*self.grid_size)
            p2 = ((x+1)*self.grid_size,y*self.grid_size)
            p3 = (x*self.grid_size,(y+1)*self.grid_size)
            p4 = ((x+1)*self.grid_size,(y+1)*self.grid_size)
            self.line_draw(p1,p2,RED)
            self.line_draw(p1,p3,RED)
            self.line_draw(p2,p4,RED)
            self.line_draw(p3,p4,RED)

    def line_draw(self,p1,p2,color):
        pygame.draw.line(self.screen,color,p1,p2,3)
    
    def connect_draw(self,path):
        for p in path:
            p1 = (p[0][1]*self.grid_size + self.grid_size//2,\
                    p[0][0]*self.grid_size + self.grid_size//2)
            p2 = (p[1][1]*self.grid_size + self.grid_size//2,\
                    p[1][0]*self.grid_size + self.grid_size//2)
            self.line_draw(p1,p2,RED)
        pygame.display.update()
        time.sleep(1)

    def check_valid(self,x):
        if x[0] <= 0 or x[0] >= self.height-1  or \
           x[1] <= 0 or x[1] >= self.width-1:
           return False
        
        return True

    def check_over(self):
        return self.score == (self.width-1)*(self.height-1)

    def music_play(self):
        pygame.mixer.music.load("D:\\106\\connect.mp3")
        pygame.mixer.music.play()

    def auto_detect(self):
        for i in range(0,(self.height-1)*(self.width-1)):
            for j in range(0,(self.height-1)*(self.width-1)):
                if i != j:
                    p1 = ((i//(self.width-1))+1,(i%(self.width-1))+1)
                    p2 = ((j//(self.width-1))+1,(j%(self.width-1))+1)
                    if self.grid.get_grid(p1) == self.grid.get_grid(p2) and self.grid.get_grid(p1) > 0:
                        pa = self.grid.mini_connect(p1,p2)
                        if len(pa) > 0:
                            self.connect_draw(pa)
                            self.music_play()
                            self.grid.set_grid(p1,0)
                            self.grid.set_grid(p2,0)
                            self.score += 2
                            return 0

    def run(self):
        while True:
            for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key in (K_w, K_UP):
                            self.autoDetect = True
                        if event.key in (K_s, K_DOWN):
                            self.autoDetect = False
                    elif event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        x = pos[1]//self.grid_size
                        y = pos[0]//self.grid_size

                        if not self.check_valid((x,y)) or self.grid.get_grid((x,y)) == 0:
                            self.isSelect = False
                            self.selected = (0,0)
                            continue

                        if (y,x) == self.selected:
                            continue

                        if self.isSelect:
                            pa = self.grid.mini_connect((x,y),(self.selected[1],self.selected[0]))
                            if len(pa) > 0:
                                self.connect_draw(pa)
                                self.music_play()
                                self.grid.set_grid((x,y),0)
                                self.grid.set_grid((self.selected[1],self.selected[0]),0)
                                self.isSelect = False
                                self.score += 2
                            else:
                                self.selected = (y,x)
                        else:
                            if self.grid.get_grid((x,y)) > 0:
                                self.selected = (y,x)
                                self.isSelect = True

            self.game_draw()
            time.sleep(0.04)
            if self.autoDetect:
                self.auto_detect()

game = Game(15,8)
game.run()