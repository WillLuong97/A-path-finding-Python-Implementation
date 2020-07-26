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
        self.color = WHITE

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
        
    #check all neighbors of the current spot, add them into the array if they are not barrier and vice versa
    def update_neighbor(self, grid):
        self.neighbors = []
        #Checking if the neighbor is a barrier or not and if it a valid spot for the current spot to go through.
        if self.row < self.total_row - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_row - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])



    def __lt__(self, other):
        return False

    #Function to make the starting point 
    def make_start(self):
        self.color = ORANGE



#Heuristic function: This is used to predict how long it would take to go from point 1 to point 2
#This function will calculate the distance between point 1 and point 2, but we will only calculate the distance under the L path, i.e. the manhattan distance
def h(p1, p2):
    #setting coordinate for p1 and p2
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#Draw the shortest path to get from the starting node to the ending node
def reconstruct_path(came_from, current, draw):
    #draw all the current node in the
    while current in came_from:
        current = came_from[current]
        current.make_path() #as the algorithm go through each node of the optimal path, makte it Purple
        draw()

#Function to code out the Path finding algorithm: 
def algorithm(draw, grid, start, end):
    count = 0 
    #PriorityQueue() is a more sufficient queue structure to extract the smallest element in a queue
    open_set = PriorityQueue()
    #First step: Adding the starting node (f score) into the queue
    open_set.put((0, count, start))
    #what node did the current node came from: 
    came_from = {}
    #G_score of the current node
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0 
    #f_score of the current node
    f_score = {spot: float("inf") for row in grid for spot in row}
    #We need to know how far it is to from the starting node to the ending node in this graph
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #At the begining of each iteration, pop out the node with the smallest fscore
        current = open_set.get()[2]
        open_set_hash.remove(current)
        #if the node we just popped out is the end node, we have found the path:
        if current == end: 
            return True
            #display the path
            reconstruct_path(came_from, end, draw)
            end.make_end()
        
        for neighbor in current.neighbors:
            temp_g_score  = g_score[current] + 1
            #if a better way to reach the node is found
            if temp_g_score < g_score[neighbor]:
                #update the current path with this new path
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                #Add that new path into the open_set
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        #if the current we just looked at is not the starting point, then that spot will be turned into red and closed off
        if current != start:
            current.make_closed()
    #The algorithmm is finished but there are no path
    return False



#Create a two day array to store the spot
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot) 
    return grid

#Draw the created grid out on the display
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

#Function to take a mouse click and translate that into a row and column on the grid that represent the cube that was just cicked on
def get_click_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 50 
    grid = make_grid(ROWS, width)

    start = None
    end = None
    #variable to check if the algorithm has run or not
    run = True
    started = False
    #setting up for the event after the algorithm has run
    #main loop for the algorighm to run on
    while run:
        draw(win, grid, ROWS, width)
        #loop through each event happens in the game and see what they are
        # i.e. a mouseclick or mousehover, etc.   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if pygame.mouse.get_pressed()[0]:   #LEFT MOUSE CLICK
                pos = pygame.mouse.get_pos()     #extracting the mouse click position on the screen
                row, col = get_click_pos(pos, ROWS, width)      #the row and col position of the mouse clicked cube
                spot = grid[row][col]       #draw that spot
                #if have not picked a start position yet, so the first start position would be the first clicked
                if not start and spot != end:   #setting the start point and not allowing both start and end point to be on the same path
                    start = spot
                    start.make_start()
                #same concept for the ending point
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                #any spot that is clicked on by the mouse and is not either the starting or ending point would be a barrier
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  #RIGHT MOUSE CLICK
                pos = pygame.mouse.get_pos()     #extracting the mouse click position on the screen
                row, col = get_click_pos(pos, ROWS, width)      #the row and col position of the mouse clicked cube
                spot = grid[row][col]       #draw that spot
                spot.reset()
                if spot == start: 
                    start = end

                elif spot == end:
                    start = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    #run the algorithm: 
                    for row in grid:
                        for spot in row:
                            spot.update_neighbor(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    # clear the entire screen
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    #exit the pygame window
    pygame.quit()

main(WIN, WIDTH)