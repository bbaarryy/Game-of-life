import pygame
import random
import math
import time
import copy

from pygame.color import THECOLORS

n = 100
p = 15

WIDTH = p*n
HEIGHT = p*n
FPS = 90
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

color1 = WHITE
color2 = BLACK
# Создаем игру и окно
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)

pygame.display.set_caption("Game of life")
clock = pygame.time.Clock()

running = True
screen.fill(THECOLORS['white'])

arr = []
for x in range(n+2):
    arr.append([0])
    for y in range(n+1):
        arr[x].append(0)

preset = 1
mouse_down = 0
lastx = 1
lasty = 1

def random_choice():
    for x in range(n):
        for y in range(n):
            arr[x+1][y+1] = random.randint(0,1)

def clear():
    for x in range(n):
        for y in range(n):
            arr[x+1][y+1] = 0


while running:
    screen.fill((255,255,255))

    keys = pygame.key.get_pressed() 
    
    for event in pygame.event.get():
        ch = 0
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            print(event.dict)
            #+rus
            if event.dict['key'] == 32:
                if preset==1:
                    preset=0
                    FPS = 10
                else:
                    preset=1
                    FPS = 90
            elif event.dict['scancode'] == 6:
                clear()
            elif event.dict['scancode'] == 21:
                random_choice()

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down=0
        elif mouse_down == 1 and event.type == pygame.MOUSEMOTION:
            try:
                lastx = event.pos[0] // p + 1
                lasty = event.pos[1] // p + 1
                arr[event.pos[0] // p + 1][event.pos[1] // p + 1] = 1
            except:
                print("Куда жмешь?")

        elif event.type == pygame.MOUSEBUTTONDOWN and preset==1:
            mouse_down = 1
            if(event.pos[1] > n*p and event.pos[0] <= 4*p):
                random_choice()
            elif(event.pos[1] > n*p and event.pos[0] >= (n-3)*p):
                clear()
            elif(event.pos[1] > n*p):
                preset=0
                FPS = 10
            else:
                try:
                    lastx = event.pos[0]//p+1
                    lasty = event.pos[1]//p+1
                    arr[event.pos[0]//p+1][event.pos[1]//p+1] ^= 1
                except:
                    print("Куда жмёшь?")

        elif event.type == pygame.MOUSEBUTTONDOWN and preset==0:
            preset = 1
            FPS = 90

    if keys[pygame.K_RIGHT]:
        lastx+=0.1
        ch=1
    elif keys[pygame.K_LEFT]:
        lastx-=0.1
        ch=1
    elif keys[pygame.K_DOWN]:
        lasty+=0.1
        ch=1
    elif keys[pygame.K_UP]:
        lasty-=0.1
        ch=1
    if(ch):
        try:
            arr[int(lastx)][int(lasty)]=1
        except:
            print("error")        

    for x in range(n):
        for y in range(n):
            if(arr[x+1][y+1]):
                pygame.draw.rect(screen, color1, (x*p,y*p,p,p), 0)
            else:
                pygame.draw.rect(screen, color2, (x * p, y * p, p, p), 0)


    new_arr = [a[:] for a in arr]

    if(preset == 0):
        for x in range(1,n+1):
            for y in range(1,n+1):
                neibs = 0
                neibs = arr[x+1][y] + arr[x+1][y-1] + arr[x+1][y+1]+\
                        arr[x-1][y] + arr[x-1][y-1] + arr[x-1][y+1]+\
                        arr[x][y-1] + arr[x][y+1]

                if arr[x][y] == 1 and (neibs<2 or neibs>3):
                    new_arr[x][y] = 0
                elif arr[x][y] == 0 and neibs == 3:
                    new_arr[x][y] = 1

    arr = [a[:] for a in new_arr]

    for x in range(n+2):
        arr[0][x]=0
        arr[x][0]=0
        arr[n+1][x]=0
        arr[x][n+1]=0

    pygame.display.update()
    clock.tick(FPS)
    #screen.fill((255, 255, 255))