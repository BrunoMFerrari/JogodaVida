"""Rules
1- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2- Any live cell with two or three live neighbours lives on to the next generation.
3- Any live cell with more than three live neighbours dies, as if by overpopulation.
4- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

Buttons
a - Autoplay
c - Clear
r - Skip Round
mouseclick - paint
"""

import pygame
from pygame.locals import *

pygame.init()

#Colors
dark_blue = (45, 96, 102, 40)
darker_blue = (31, 68, 72, 28)
light_green = (0, 230, 98, 90)

#Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
GRID_SQUARES = 20 #Size of the squares in pixels
GRID_WIDTH = WINDOW_WIDTH // GRID_SQUARES #X axis of the grid
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SQUARES #Y axis of the grid
FPS = 60 #FPS of the window

#Window
pygame.display.set_caption("Conway's Game of Life") #Name of the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #Creating the window
frame = pygame.time.Clock()

#Functions
def draw_grid(positions):
    #Getting positions of the squares
    for collum, row in positions: #Checking what squares need to change color
        top_left = (collum * GRID_SQUARES, row * GRID_SQUARES) #Getting the X and Y axis in the grid
        pygame.draw.rect(window, #Drawing the light_green square when needed
                         light_green,
                         (*top_left, GRID_SQUARES, GRID_SQUARES))
    #Drawing rows
    for row in range(GRID_HEIGHT):
        pygame.draw.line(window,
                         darker_blue,
                         (0, row * GRID_SQUARES),
                         (WINDOW_WIDTH, row * GRID_SQUARES))
    #Drawing collums
    for collum in range(GRID_WIDTH):
        pygame.draw.line(window,
                         darker_blue,
                         (collum * GRID_SQUARES, 0),
                         (collum * GRID_SQUARES, WINDOW_HEIGHT))

def update_grid(positions):
    all_neighbors = set() #Gathering all neighbors of living cells into a list
    next_round_positions = set() #Putting all cells that will be present in next round in a list

    for position in positions: 
        neighbors = get_neighbors(position) #Positions of live neighbors around cell
        all_neighbors.update(neighbors) #Adding new neighbors to the all_neighbors list

        neighbors = list(filter(lambda x: x in positions, neighbors)) #Filtering list of neighbors so it wont repeat

        if len(neighbors) in [2, 3]: #Adding cells that will continue in next round to next_round_positions list
            next_round_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position) #Positions of live neighbors around cell
        neighbors = list(filter(lambda x: x in positions, neighbors)) #Filtering list of neighbors so it wont repeat

        if len(neighbors) == 3: #Adding dead cells that will live on the next round
            next_round_positions.add(position)

    return next_round_positions

def get_neighbors(position): #Checking live neighbors around cells
    x, y = position
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))

    return neighbors

positions = set() #Positions of live cells
count = 0 #Round count
update_freq = 1 #Frequency that the game update
autoplay = False 
#Window Loop
while True:
    #Creating window
    window.fill(dark_blue)
    frame.tick(FPS)

    if autoplay == True: 
        count += 0.1

    if count >= update_freq: #Update cells
        count = 0
        positions = update_grid(positions)

    #Event detection
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            collum = x // GRID_SQUARES
            row = y // GRID_SQUARES
            pos = (collum, row)

            if pos in positions:
                positions.remove(pos)
            else:
                positions.add(pos)
        if event.type == KEYDOWN:
            if event.key == K_c:
                positions = set()
                count = 0
            if event.key == K_r:
                count += 1
            if event.key == K_a:
                if autoplay == False:
                    autoplay = True
                else:
                    autoplay = False

    draw_grid(positions)

    pygame.display.update()
