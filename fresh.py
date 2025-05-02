import pygame
import random
import math
import time
import copy

from pygame.color import THECOLORS

n = 160
p = 10

WIDTH = p*n
HEIGHT = p*(n+3)
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
while running:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.dict['key'] == 32:
                if preset==1:
                    preset=0
                    FPS = 10
                else:
                    preset=1
                    FPS = 90
            elif 79 <= event.dict['scancode'] <= 82:
                if event.dict['key'] == 1073741903:
                    lastx+=1
                elif event.dict['key'] == 1073741904:
                    lastx-=1
                elif event.dict['key'] == 1073741905:
                    lasty+=1
                elif event.dict['key'] == 1073741906:
                    lasty-=1
                try:
                    preset=1
                    arr[lastx][lasty] = 1
                except:
                    print("куда жмёшь?")

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down=0
        elif mouse_down == 1 and event.type == pygame.MOUSEMOTION:
            if (event.pos[1] > n * p and event.pos[0] > 3*p):
                preset = 0
                FPS = 10
            else:
                try:
                    lastx = event.pos[0] // p + 1
                    lasty = event.pos[1] // p + 1
                    arr[event.pos[0] // p + 1][event.pos[1] // p + 1] = 1
                except:
                    print("Куда жмешь?")
        elif event.type == pygame.MOUSEBUTTONDOWN and preset==1:
            mouse_down = 1
            if(event.pos[1] > n*p and event.pos[0] <= 4*p):
                for x in range(n):
                    for y in range(n):
                        arr[x+1][y+1] = random.randint(0,1)
            elif(event.pos[1] > n*p and event.pos[0] >= (n-3)*p):
                for x in range(n):
                    for y in range(n):
                        arr[x+1][y+1] = 0
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

    for x in range(n):
        for y in range(n):
            if(arr[x+1][y+1]):
                pygame.draw.rect(screen, color1, (x*p,y*p,p,p), 0)
            else:
                pygame.draw.rect(screen, color2, (x * p, y * p, p, p), 0)

    # for x in range(n):
    #     pygame.draw.line(screen,BLACK,(0,p*x),(p*n,p*x))
    # for x in range(n):
    #     pygame.draw.line(screen,BLACK,(p*x,0),(p*x,p*n))

    pygame.draw.line(screen,BLACK,(0,p*n), (p*n,p*n),3)
    pygame.draw.line(screen, BLACK, (0, p *(n+3)), (p*n,p * n+3*p),3)
    pygame.draw.line(screen, BLACK, (4*p,n*p), (4*p,(n+3)*p),3)
    pygame.draw.line(screen, BLACK, ((n-3)*p,n*p), ((n-3)*p,(n+3)*p),3)
    if(preset==1):
        pygame.draw.polygon(screen,BLACK,[(n*p//2,n*p+p*1),(n*p//2,n*p+p*2),(n*p//2+p,n*p+p*1.5)])
    else:
        pygame.draw.polygon(screen, BLACK, [(n * p // 2, n * p + p * 1), (n * p // 2, n * p + p * 2),
                                            (n * p // 2 + p, n * p + p * 2), (n * p // 2 + p, n * p + p * 1)])

    this_font = pygame.font.SysFont('impact', p+7)
    text = this_font.render("+ rand", True, (0, 0, 0))
    screen.blit(text, (p//2, p*n+p ))

    text = this_font.render("clear", True, (0, 0, 0))
    screen.blit(text, (p//2+p*(n-3), p*n+p ))

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