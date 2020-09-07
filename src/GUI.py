# GUI.py
import pygame
import time
pygame.font.init()
import sys
import grid_solver
import numpy as np
import random

class Grid:
    def __init__(self, size, width, height, win):
        self.size = size
        self.board = [[size*i + j + 1 for j in range(size)] for i in range(size)]
        self.board[size-1][size-1] = 0
        self.rows = size
        self.cols = size
        self.cubes = [[Cube(self.board[i][j], size, i, j, width, height) for j in range(size)] for i in range(size)]
        self.width = width
        self.height = height
        self.selected = None
        self.win = win
        self.update_grid()

    def update_grid(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.cubes[i][j].value = self.board[i][j]

    def find_neighbour_gap(self):
        row, col = self.selected
        neighbours = [(row-1, col), (row, col-1), (row+1, col), (row, col+1)]
        for (a,b) in neighbours:
            if 0 <= a < len(self.cubes) and 0 <= b < len(self.cubes[row]):
                if self.cubes[a][b].value == 0:
                    return (a,b)
        return (-1,-1)

    def move(self):
        row, col = self.selected
        (a,b) = self.find_neighbour_gap()
        if a != -1 and b != -1:
            self.board[a][b] = self.board[row][col]
            self.board[row][col] = 0
            self.update_grid()
            return True
        return False

    def draw(self):
        # Draw grid lines
        gap = self.width / self.size
        for i in range(self.rows + 1):
            thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def shuffle(self):
        valid = False
        while not valid:
            number_list = list(range(0, self.size * self.size, 1))
            random.shuffle(number_list)
            if solvable(number_list):
                valid = True

        new_grid = np.array(number_list).reshape(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = new_grid[i][j]
        self.update_grid()

    def select(self, row, col):
        # Reset
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row,col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / self.size
            x = pos[0] // gap
            y= pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def change_state(self, new_state):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != new_state[self.size*i + j] and self.board[i][j] != 0:
                    self.select(i,j)
                    self.move()


class Cube:

    def __init__(self,  value, grid_size, row, col, width, height):
        self.grid_size = grid_size
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / self.grid_size
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), self.grid_size)

def redraw_window(win, board, time, steps = None):
    win.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    # Draw steps
    if steps:
        text = fnt.render("Steps: " + str(steps), 1, (255, 0, 0))
        win.blit(text, (20, 560))
    # Draw instructions
    fnt = pygame.font.SysFont("comicsans", 20)
    text = fnt.render("S - Shuffle" , 1, (0, 0, 0))
    win.blit(text, (540 - 320, 560-15))
    text = fnt.render("LMB - Slide", 1, (0, 0, 0))
    win.blit(text, (540 - 320, 560))
    text = fnt.render("Space - Solve", 1, (0, 0, 0))
    win.blit(text, (540 - 320, 560+15))
    # Draw grid and board
    board.draw()

def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60
    mat = " " + str(minute) + ":" + str(sec)
    return mat

def solvable(order):
    count = 0
    for i in range(len(order)):
        for j in range(i+1, len(order)):
            if order[j] and order[i] > order[j]:
                count += 1
    return count % 2 == 0

def main():
     size = int(input("Enter grid size: "))
     goal_state = [[size * i + j + 1 for j in range(size)] for i in range(size)]
     goal_state[size - 1][size - 1] = 0
     win = pygame.display.set_mode((540, 600))
     pygame.display.set_caption("Sliding Puzzle")
     board = Grid(size, 540, 540, win)
     key = None
     run = True
     steps = 0
     start = time.time()

     while run:
         play_time = round(time.time() - start)
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()

             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE:
                     solver = grid_solver.GridSolver(np.array(board.board), np.array(goal_state))
                     for node in reversed(solver.solve_grid()):
                         steps += 1
                         board.change_state(node.curr_state)
                         redraw_window(win, board, play_time, steps)
                         pygame.display.update()
                         time.sleep(0.25)
                     steps = 0
                 if event.key == pygame.K_s:
                     board.shuffle()
                 key = None

             if event.type == pygame.MOUSEBUTTONDOWN:
                 pos = pygame.mouse.get_pos()
                 clicked = board.click(pos)
                 if clicked:
                     board.select(clicked[0], clicked[1])
                     key = None
                     board.move()

         redraw_window(win, board, play_time)
         pygame.display.update()

main()
pygame.quit()