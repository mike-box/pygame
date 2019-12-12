import sys, time
import math, random
import cv2
import win32api
import win32gui
import win32con
from PIL import ImageGrab
import time
from config import *

def getGameWindowPosition():
    window = win32gui.FindWindow(None, WINDOW_TITLE)
    while not window:
        print('unable to find window, try in 3 secs...')
        time.sleep(3)
        window = win32gui.FindWindow(None, WINDOW_TITLE)
    win32gui.SetForegroundWindow(window)
    pos = win32gui.GetWindowRect(window)
    print("Window found at:" + str(pos))
    return pos[0], pos[1]

def getScreenImage():
    print('capturing screenshot...')
    scim = ImageGrab.grab()
    scim.save('screen.png')
    return cv2.imread("screen.png")

def getAllSquare(screen_image, game_pos):
    print('cutting pics...')
    game_x = game_pos[0] + MARGIN_LEFT
    game_y = game_pos[1] + MARGIN_HEIGHT
    all_square = []
    print("width:",len(screen_image))
    print("height:",len(screen_image[0]))

    for x in range(0, COL_NUM):
        for y in range(0, ROW_NUM):
            square = screen_image[game_y + y*SQUARE_HEIGHT:
                                  game_y + (y+1)*SQUARE_HEIGHT,
                                  game_x + x*SQUARE_WIDTH:
                                  game_x + (x+1)*SQUARE_WIDTH]
            all_square.append(square)
    return list(map(lambda square:
                    square[SUB_LT_Y:SUB_RB_Y, SUB_LT_X:SUB_RB_X], all_square))

def subImageSquare(img1,img2):
    res = 0
    for i in range(len(img1)):
        for j in range(len(img1[0])):
            res += abs(int(img1[i][j][0]) - int(img2[i][j][0])) + \
                    abs(int(img1[i][j][1]) - int(img2[i][j][1])) + \
                    abs(int(img1[i][j][2]) - int(img2[i][j][2]))
    return res

def getAllImageTypes(all_square):
    print("sorting pics...")
    empty_img = cv2.imread('empty.png')
    types = set([0])

    for square in all_square:
        types.add(subImageSquare(empty_img,square))
    return sorted(list(types))

def generateMatrix(all_square,imgTypes):
    mat = []
    empty_img = cv2.imread('empty.png')

    for square in all_square:
        diff = subImageSquare(empty_img,square)
        for i in range(len(imgTypes)):
            if diff == imgTypes[i]:
                mat.append(i) 
    return mat

def checkConnect(x,y,mat):
    width = COL_NUM
    height = ROW_NUM

    if x[0] < 0 or x[1] < 0 or x[0] >= width or x[1] >= height or\
       y[0] < 0 or y[1] < 0 or y[0] >= width or y[1] >= width:
            return False
    if x[0] != y[0] and x[1] != y[1]:
        return False

    #check row
    if x[0] == y[0]:
        for i in range(min(x[1],y[1])+1,max(x[1],y[1])):
            if mat[x[0]*height+i] > 0:
                return False
    #check colum
    if x[1] == y[1]:
        for i in range(min(x[0],y[0])+1,max(x[0],y[0])):
            if mat[i*height+x[1]] > 0:
                return False
    return True

def isCanLink(x,y,mat):
    width = COL_NUM
    height = ROW_NUM

    #check same value
    if mat[x[0]*height+x[1]] != mat[y[0]*height+y[1]]:
        return False
    #one step check
    if checkConnect(x,y,mat):
        return True
    #two step check
    if mat[x[0]*height+y[1]] == 0:
        if checkConnect(x,(x[0],y[1]),mat) and \
           checkConnect((x[0],y[1]),y,mat):
            return True
    if mat[y[0]*height+x[1]] == 0:
        if checkConnect(x,(y[0],x[1]),mat) and \
           checkConnect((y[0],x[1]),y,mat):
            return True
    
    #three step check
    for i in range(0,height):
        if mat[x[0]*height+i] == 0 and mat[y[0]*height+i] == 0:
            if checkConnect(x,(x[0],i),mat) and \
               checkConnect((y[0],i),y,mat) and \
               checkConnect((x[0],i),(y[0],i),mat):
               return True
    for i in range(0,width):
        if mat[i*height+x[1]] == 0 and mat[i*height+y[1]] == 0:
            if checkConnect(x,(i,x[1]),mat) and \
               checkConnect((i,y[1]),y,mat) and \
               checkConnect((i,x[1]),(i,y[1]),mat):
               return True

def autoMouseClick(pos,delay = 0.001):
    win32api.SetCursorPos((pos[0],pos[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos[0],pos[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1],0,0)
    time.sleep(TIME_INTERVAL())
   
def autoRemove(mat,game_pos):
    game_x = game_pos[0] + MARGIN_LEFT
    game_y = game_pos[1] + MARGIN_HEIGHT
    width = COL_NUM
    height = ROW_NUM
    remove = 0

    for i in range(width):
        for j in range(height):
            if mat[i*height+j] > 0:
                remove += 1

    while remove > 0:
        for i in range(len(mat)):
            for j in range(len(mat)):
                if i != j and mat[i] == mat[j] and mat[i] > 0:
                    px = (i//height,i%height)
                    py = (j//height,j%height)
                    if isCanLink(px,py,mat):
                        x1 = game_x + px[0]*SQUARE_WIDTH
                        y1 = game_y + px[1]*SQUARE_HEIGHT
                        x2 = game_x + py[0]*SQUARE_WIDTH
                        y2 = game_y + py[1]*SQUARE_HEIGHT
                        pos_x = (x1+CLICK_POS_X,y1+CLICK_POS_Y)
                        pos_y = (x2+CLICK_POS_X,y2+CLICK_POS_Y)
                        autoMouseClick(pos_x)
                        autoMouseClick(pos_y)
                        mat[i] = 0
                        mat[j] = 0
                        remove -= 2
                        print(px,py)
                        print("remove one pair:",pos_x,pos_y)

if __name__ == '__main__':
    game_pos = getGameWindowPosition()
    time.sleep(1)
    screen_image = getScreenImage()
    all_square_list = getAllSquare(screen_image, game_pos)
    imgTypes = getAllImageTypes(all_square_list)
    mat = generateMatrix(all_square_list,imgTypes)
    autoRemove(mat,game_pos)