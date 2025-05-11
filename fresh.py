import pygame
import random

from pygame.color import THECOLORS

n = 100
p = 5

WIDTH = p * n
HEIGHT = p * n
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

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Game of life")
clock = pygame.time.Clock()

arr = []
for x in range(n + 2):
    arr.append([0])
    for y in range(n + 1):
        arr[x].append(0)

drawing = 1
mouse_down = 0
lastx = 1
lasty = 1

def random_choice():
    for x in range(n):
        for y in range(n):
            arr[x + 1][y + 1] = random.randint(0, 1)


def draw_line(lx, ly, x, y):
    a = abs(x - lx)
    b = abs(y - ly)

    right = (x - lx) >= 0
    up = (y - ly) >= 0
    if up == 0:
        up = -1
    if right == 0:
        right = -1

    if (a == 0):
        for i in range(ly, y + up, up):
            arr[x][i] = 1
        return
    if (b == 0):
        for i in range(lx, x + right, right):
            arr[i][y] = 1
        return

    curry = ly
    plus = up * (b / (a + 1))

    for currx in range(lx, x + right, right):
        border = -1
        if (up == -1):
            border = max(int(curry + plus + up), y - 1)
        else:
            border = min(int(curry + plus + up), y + 1)

        for i in range(int(curry), border, up):
            arr[currx][i] = 1
        curry += plus
    arr[x][y] = 1


def clear():
    for x in range(n):
        for y in range(n):
            arr[x + 1][y + 1] = 0

running = True
while running:
    screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()
    ch = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.dict['key'] == 32:
                if drawing == 1:
                    drawing = 0
                    FPS = 10
                else:
                    drawing = 1
                    FPS = 200
            elif event.dict['scancode'] == 6:
                clear()
            elif event.dict['scancode'] == 21:
                random_choice()

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = 0
        elif mouse_down == 1 and event.type == pygame.MOUSEMOTION:

            arr[event.pos[0] // p + 1][event.pos[1] // p + 1] = 1
            lx = lastx
            ly = lasty
            x = event.pos[0] // p + 1
            y = event.pos[1] // p + 1
            draw_line(lx,ly,x,y)
            #draw_line(0, 10,10 ,0 )
            lastx = event.pos[0] // p + 1
            lasty = event.pos[1] // p + 1


        elif event.type == pygame.MOUSEBUTTONDOWN and drawing == 1:
            mouse_down = 1
            try:
                lastx = event.pos[0] // p + 1
                lasty = event.pos[1] // p + 1
                arr[event.pos[0] // p + 1][event.pos[1] // p + 1] ^= 1
            except:
                print("Куда жмёшь?")

        elif event.type == pygame.MOUSEBUTTONDOWN and drawing == 0:
            drawing = 1
            FPS = 200

    if keys[pygame.K_RIGHT]:
        lastx += 0.1
        ch = 1
    elif keys[pygame.K_LEFT]:
        lastx -= 0.1
        ch = 1
    elif keys[pygame.K_DOWN]:
        lasty += 0.1
        ch = 1
    elif keys[pygame.K_UP]:
        lasty -= 0.1
        ch = 1
    if ch:
        try:
            arr[int(lastx)][int(lasty)] = 1
        except:
            print("error")

    for x in range(n):
        for y in range(n):
            if (arr[x + 1][y + 1]):
                pygame.draw.rect(screen, color1, (x * p, y * p, p, p), 0)
            else:
                pygame.draw.rect(screen, color2, (x * p, y * p, p, p), 0)

    new_arr = [a[:] for a in arr]

    if (drawing == 0):
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                neibs = 0
                neibs = arr[x + 1][y] + arr[x + 1][y - 1] + arr[x + 1][y + 1] + \
                        arr[x - 1][y] + arr[x - 1][y - 1] + arr[x - 1][y + 1] + \
                        arr[x][y - 1] + arr[x][y + 1]

                if arr[x][y] == 1 and (neibs < 2 or neibs > 3):
                    new_arr[x][y] = 0
                elif arr[x][y] == 0 and neibs == 3:
                    new_arr[x][y] = 1

    arr = [a[:] for a in new_arr]

    for x in range(n + 2):
        arr[0][x] = 0
        arr[x][0] = 0
        arr[n + 1][x] = 0
        arr[x][n + 1] = 0

    pygame.display.update()
    clock.tick(FPS)
    # screen.fill((255, 255, 255))
