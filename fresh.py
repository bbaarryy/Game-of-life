import pygame
import random
import math
import time
import copy

from pygame.color import THECOLORS

n = 30
p = 15

WIDTH = p*n
HEIGHT = p*(n+3)
FPS = 20
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Создаем игру и окно
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

running = True
screen.fill(THECOLORS['white'])

arr = []
for x in range(n+2):
    arr.append([0])
    for y in range(n+1):
        arr[x].append(random.randint(0,1))

preset = 1
mouse_down = 0
while running:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down=0
        elif mouse_down == 1 and event.type == pygame.MOUSEMOTION:
            if (event.pos[1] > n * p):
                preset = 0
                FPS = 10
                # print("Go!")
            else:
                # print(event.pos)
                try:
                    arr[event.pos[0] // p + 1][event.pos[1] // p + 1] = 1
                except:
                    print("Куда жмешь?")
        elif event.type == pygame.MOUSEBUTTONDOWN and preset==1:
            mouse_down = 1
            if(event.pos[1] > n*p):
                preset=0
                FPS = 10
                #print("Go!")
            else:
                #print(event.pos)
                try:
                    arr[event.pos[0]//p+1][event.pos[1]//p+1] ^= 1
                except:
                    print("Куда жмёшь?")
        elif event.type == pygame.MOUSEBUTTONDOWN and preset==0:
            preset = 1
            FPS = 30

    for x in range(n):
        for y in range(n):
            if(arr[x+1][y+1]):
                pygame.draw.rect(screen, BLACK, (x*p,y*p,p,p), 0)
            else:
                pygame.draw.rect(screen, (255,174,201), (x * p, y * p, p, p), 0)

    for x in range(n):
        pygame.draw.line(screen,BLACK,(0,p*x),(p*n,p*x))
    for x in range(n):
        pygame.draw.line(screen,BLACK,(p*x,0),(p*x,p*n))

    pygame.draw.line(screen,BLACK,(0,p*n), (p*n,p*n),3)
    pygame.draw.line(screen, BLACK, (0, p *(n+3)), (p*n,p * n+3*p),3)
    if(preset==1):
        pygame.draw.polygon(screen,BLACK,[(n*p//2,n*p+p*1),(n*p//2,n*p+p*2),(n*p//2+p,n*p+p*1.5)])
    else:
        pygame.draw.polygon(screen, BLACK, [(n * p // 2, n * p + p * 1), (n * p // 2, n * p + p * 2),
                                            (n * p // 2 + p, n * p + p * 2), (n * p // 2 + p, n * p + p * 1)])

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

    pygame.display.update()
    clock.tick(FPS)
    #screen.fill((255, 255, 255))

