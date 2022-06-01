import pygame
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import  database


class Cube(object):
    rows = 20
    width = 500

    def __init__(self, start, dirnx = 1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))
        if eyes:
            center = distance // 2
            radius = 3
            circle_middle1 = (i * distance+center - radius, j * distance + 8)
            circle_middle2 = (i * distance + distance - radius * 2, j * distance + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle1, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class Snake(object):
    # list of positions
    snake_body = []
    # dictionary of turns
    turns = {}

    def __init__(self, color, pos, surface):
        self.color = color
        self.head = Cube(pos)
        self.snake_body.append(self.head)
        self.dir_x = 0
        self.dir_y = 1
        self.surface = surface

    def move(self, running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dir_x = -1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_RIGHT]:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_UP]:
                    self.dir_x = 0
                    self.dir_y = -1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_DOWN]:
                    self.dir_x = 0
                    self.dir_y = 1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
        for i, c in enumerate(self.snake_body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.snake_body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c. rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.snake_body = []
        self.snake_body.append(self.head)
        self.turns = {}
        self.dir_x = 0
        self.dir_y = 1

    def add_cube(self):
        tail = self.snake_body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.snake_body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.snake_body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.snake_body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.snake_body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.snake_body[-1].dirnx = dx
        self.snake_body[-1].dirny = dy

    def draw(self):
        for i, c in enumerate(self.snake_body):
            if i == 0:
                c.draw(self.surface, True)
            else:
                c.draw(self.surface)


def draw_greed(screen, width, rows):
    size_between = width // rows
    x = 0
    y = 0
    for row in range(rows):
        x += size_between
        y += size_between
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(screen, (255, 255, 255), (0, y), (width, y))


def random_snack(rows, snake):
    positions = snake.snake_body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    snake_pos = (x, y)
    return snake_pos


def redraw_window(screen, width, rows, snake, snack):
    screen.fill((175, 238, 238))
    snake.draw()
    snack.draw(screen)
    draw_greed(screen, width, rows)
    pygame.display.update()


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def username_box():
    parent = tk.Tk()
    parent.overrideredirect(1)  # Avoid it appearing and then disappearing quickly
    parent.withdraw()  # Hide the window as we do not want to see this one
    string_value = simpledialog.askstring("user", "Enter username")
    return string_value


def main():
    width = 500
    rows = 20
    highest_score = 0
    # initializing pygame
    pygame.init()
    # creating the screen
    screen = pygame.display.set_mode((width, width))

    # title an icon
    pygame.display.set_caption("Snake")
    icon = pygame.image.load('snake.png')
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    snake = Snake((255, 0, 0), (10, 10), screen)
    snack = Cube(random_snack(rows, snake), color=(0, 255, 0))
    username = username_box()
    print(username)
    running = True
    while running:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move(running)
        if snake.snake_body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(random_snack(rows, snake), color=(0, 255, 0))

        for x in range(len(snake.snake_body)):
            if snake.snake_body[x].pos in list(map(lambda z: z.pos, snake.snake_body[x + 1:])):
                print('Score: ', len(snake.snake_body))
                database.add_user(username, len(snake.snake_body))
                message_box('You Lost!', 'Play again...')
                snake.reset((10, 10))
                break

        redraw_window(screen, width, rows, snake, snack)


main()
