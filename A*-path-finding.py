import pygame
import math
from queue import PriorityQueue

#Setting up the display
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("A* Path Finding Algorithm!")

#Color attributes for path changing and selecting
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURTOUISE = (64, 224, 208)

#VISUALIZATION TOOLS:
#Spot: the little cube in the grid 
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # x and y are the coordinate of each of the spot in the 
        # grid, each spot has its own width so to get to a particlar spot on the screen, the row and column must be multiplied by its width
        self.x = row * width
        self.y = col * width 
        self.neighbors = []
        self.width = width
        self.total_row = total_rows
        self.color = WHITE

    #getting the position of the spot.
    def get_pos(self):
        return self.row, self.col

    #Checking if a spot has been looked at or not
    def is_closed(self):
        return self.color == RED 

    #Checking if a spot is open for path to go through
    def is_open(self):
        return self.color == GREEN

    #Checking if a spot is barrier
    def is_barrier(self):
        return self.color == BLACK

    #Checking if the spot is a starting position
    def is_start(self):
        return self.color == ORANGE
    
    #checking if the spot is an ending node.
    def is_end(self):
        return self.color == TURTOUISE
    
    def reset(self):
        self.color == WHITE

    #actually changning the color based on the status of the grid 
    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURTOUISE
    
    def make_path(self):
        self.color = PURPLE
    
    #Draw a queue with previous attributes of color.
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.width))
        
    
    def update_neighbor(self, grid):
        pass

    def __lt__(self, other):
        return False




#Heuristic function: This is used to predict how long it would take to go from point 1 to point 2
#This function will calculate the distance between point 1 and point 2, but we will only calculate the distance under the L path, i.e. the manhattan distance
def h(p1, p2):
    #setting coordinate for p1 and p2
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot) 
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, row, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, row, width)
    pygame.display.update()


