import random
import pygame
import sys
import tkinter as tk
from tkinter import messagebox

global rows, width, s, snack


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.x_direction = 1
        self.y_direction = 0
        self.color = color

    def move(self, x_direction, y_direction):
        self.x_direction = x_direction
        self.y_direction = y_direction
        self.pos = (self.pos[0] + self.x_direction, self.pos[1] + self.y_direction)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.x_direction = 0
        self.y_direction = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.init()
            keys = pygame.key.get_pressed()
            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.x_direction = -1
                    self.y_direction = 0
                    self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

                elif keys[pygame.K_RIGHT]:
                    self.x_direction = 1
                    self.y_direction = 0
                    self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

                elif keys[pygame.K_UP]:
                    self.x_direction = 0
                    self.y_direction = -1
                    self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

                elif keys[pygame.K_DOWN]:
                    self.x_direction = 0
                    self.y_direction = 1
                    self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.x_direction == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.x_direction == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.y_direction == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.y_direction == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.x_direction, c.y_direction)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.x_direction = 0
        self.y_direction = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.x_direction, tail.y_direction

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].x_direction = dx
        self.body[-1].y_direction = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, grid_rows, surface):
    size_between = w // rows

    x = 0
    y = 0
    for _ in range(grid_rows):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redraw_window(surface):
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(snack_row, item):
    positions = item.body

    while True:
        x = random.randrange(snack_row)
        y = random.randrange(snack_row)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)

    # noinspection PyBroadException
    try:
        root.destroy()
    except Exception:
        pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(random_snack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(10)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = cube(random_snack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score:', len(s.body))
                message_box('You Lost!', 'Play Again!')
                s.reset((10, 10))
                break

        redraw_window(win)

    pass


main()






