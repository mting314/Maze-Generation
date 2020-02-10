from tkinter import *
from random import seed
from random import randint
import random
import time
import cv2
import math
import numpy as np


seed()
CELL_SIZE = 70

GRID_WIDTH = 10
GRID_HEIGHT = 10
height = int(GRID_HEIGHT*CELL_SIZE)
width = int(GRID_WIDTH*CELL_SIZE)
LINE_THICKNESS = 6

DIRECTIONS = [(-1,0), (1,0), (0,-1), (0,1)]



class Wall:
    def __init__(self, first_cell, second_cell):
        self.first_cell = first_cell
        self.second_cell = second_cell
        
        #weight of each edge, i.e. how likely this wall is to be selected from the list of active walls
        self.weight = 1 #math.sqrt(first_cell[0]**2+first_cell[1]**2)*first_cell[1]**20 + math.sqrt(first_cell[0]**2+first_cell[1]**2)*first_cell[0]**20 + math.sqrt(first_cell[0]**2+first_cell[1]**2)*second_cell[1]**20 + math.sqrt(first_cell[0]**2+first_cell[1]**2)*second_cell[0]**20
        
        #orientation is 1 for horizontal, 0 for vertical wall
        self.orientation = abs(first_cell[0] - second_cell[0])
    
    #unused function but I kept it in because you never know, but just prints all info about a wall
    def print_wall(self):
        print("My first cell is", self.first_cell)
        print("My second cell is", self.second_cell)
        if self.orientation == 0:
            print("I am a vertical wall")
        else:
            print("I am a horizontal wall")
    
    #drawn a wall object. takes passage as an argument, and draws it in blue/background color if passage to make it look like there's no wall
    def drawWall(self, canvas, color, passage):
        if passage == 1:
            #determine if horizontal or vertical
            if self.orientation == 1:
                #canvas.create_rectangle(self.second_cell[0]*CELL_SIZE-LINE_THICKNESS/2, self.second_cell[1]*CELL_SIZE+LINE_THICKNESS/2+1,self.second_cell[0]*CELL_SIZE+LINE_THICKNESS/2,  (self.second_cell[1]+1)*CELL_SIZE-LINE_THICKNESS/2-1, fill = color, outline = color)
                canvas.create_rectangle(self.second_cell[1]*CELL_SIZE+LINE_THICKNESS/2+1,self.second_cell[0]*CELL_SIZE-LINE_THICKNESS/2 , (self.second_cell[1]+1)*CELL_SIZE-LINE_THICKNESS/2-1 ,self.second_cell[0]*CELL_SIZE+LINE_THICKNESS/2 , fill = color, outline = color)
            else: #it's horizontal
                #canvas.create_rectangle(self.first_cell[0]*CELL_SIZE+LINE_THICKNESS/2+1, self.second_cell[1]*CELL_SIZE-LINE_THICKNESS/2, (self.first_cell[0]+1)*CELL_SIZE-LINE_THICKNESS/2-1, self.second_cell[1]*CELL_SIZE+LINE_THICKNESS/2, fill = color, outline = color)
                canvas.create_rectangle( self.second_cell[1]*CELL_SIZE-LINE_THICKNESS/2,self.first_cell[0]*CELL_SIZE+LINE_THICKNESS/2+1, self.second_cell[1]*CELL_SIZE+LINE_THICKNESS/2,(self.first_cell[0]+1)*CELL_SIZE-LINE_THICKNESS/2-1 , fill = color, outline = color)
        else:
            if self.orientation == 1:
                canvas.create_rectangle(self.second_cell[1]*CELL_SIZE-LINE_THICKNESS/2+1, self.second_cell[0]*CELL_SIZE-LINE_THICKNESS/2, (self.second_cell[1]+1)*CELL_SIZE+LINE_THICKNESS/2,  self.second_cell[0]*CELL_SIZE+LINE_THICKNESS/2, fill = color, outline = color)
            else: #it's horizontal
                canvas.create_rectangle(self.second_cell[1]*CELL_SIZE-LINE_THICKNESS/2+1, self.first_cell[0]*CELL_SIZE-LINE_THICKNESS/2, self.second_cell[1]*CELL_SIZE+LINE_THICKNESS/2+1, (self.first_cell[0]+1)*CELL_SIZE+LINE_THICKNESS/2, fill = color, outline=color)
    #override equality operator
    def __eq__(self, other):
        if isinstance(i, Wall) and other != None:
            return (self.orientation == other.orientation and self.first_cell[0] == other.first_cell[0] and self.first_cell[1] == other.first_cell[1] and self.second_cell[1] == other.second_cell[1] and self.second_cell[0] == other.second_cell[0])

#makes the actual writable image using cv2 and np by imitating what TK does, just called at the end to generate final image
def printPicture(walls):

    
    image = np.zeros((height,width,3), np.uint8) #start with blank image
    image[:,:] = (255,255,255) #color blank image white
    
    #horizontal lines
    for i in range(GRID_HEIGHT):
        cv2.line(image,(0,i*CELL_SIZE), (width, i*CELL_SIZE), color = (0,0,0), thickness = LINE_THICKNESS)
    
    #vertical liens
    for i in range(GRID_WIDTH):
        cv2.line(image,(i*CELL_SIZE,0),(i*CELL_SIZE,height),color = (0,0,0), thickness = LINE_THICKNESS)
    
    #draw all passages  in white to blend in with background
    for i in walls:
        if i.orientation == 1:
            #topleft = (int(i.second_cell[0]*CELL_SIZE-LINE_THICKNESS//2), int(i.second_cell[1]*CELL_SIZE+LINE_THICKNESS//2+1))
            topleft = (int(i.second_cell[1]*CELL_SIZE+LINE_THICKNESS//2+1),int(i.second_cell[0]*CELL_SIZE-LINE_THICKNESS//2))
            #bottomright = (int(i.second_cell[0]*CELL_SIZE+LINE_THICKNESS//2), int((i.second_cell[1]+1)*CELL_SIZE-LINE_THICKNESS//2-1))
            bottomright = (int((i.second_cell[1]+1)*CELL_SIZE-LINE_THICKNESS//2-1),int(i.second_cell[0]*CELL_SIZE+LINE_THICKNESS//2))
        else:
            #topleft = (int(i.first_cell[0]*CELL_SIZE+LINE_THICKNESS//2+1), int(i.second_cell[1]*CELL_SIZE-LINE_THICKNESS//2))
            topleft = (int(i.second_cell[1]*CELL_SIZE-LINE_THICKNESS//2),int(i.first_cell[0]*CELL_SIZE+LINE_THICKNESS//2+1))
            #bottomright =(int((i.first_cell[0]+1)*CELL_SIZE-LINE_THICKNESS//2-1), int(i.second_cell[1]*CELL_SIZE+LINE_THICKNESS//2))
            bottomright =( int(i.second_cell[1]*CELL_SIZE+LINE_THICKNESS//2),int((i.first_cell[0]+1)*CELL_SIZE-LINE_THICKNESS//2-1))
        cv2.rectangle(image,topleft,bottomright, color = (255,255,255), thickness = -1)
    
    #maze bounds around the whole maze
    cv2.rectangle(image, (0, 0), (width, height), color = (0,0,0),thickness = LINE_THICKNESS)
    return image

class Cell:
    #main purpose of even having a cell object is to easily generate the walls around a certain cell position just by initializing the cell object at that position
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.Walls = []
        #up
        if (ypos-1) >= 0:
            self.Walls.append(Wall((xpos, ypos-1), (xpos, ypos)))
        #down
        if (ypos+1) <= (GRID_HEIGHT-1):
            self.Walls.append(Wall((xpos, ypos), (xpos, ypos+1)))
        #left
        if (xpos-1) >= 0:
            self.Walls.append(Wall((xpos-1, ypos), (xpos, ypos)))
        #right
        if (xpos+1) <= (GRID_WIDTH-1):
            self.Walls.append(Wall((xpos, ypos), (xpos+1, ypos)))

        
    def printCell(self):
        print("This is the cell", (self.xpos, self.ypos))

def drawMaze(canvas, active_walls, passage_walls, cells, wait = 0, active_wall = None):
    for i in range(GRID_HEIGHT):
        canvas.create_rectangle(0,i*CELL_SIZE, GRID_WIDTH*CELL_SIZE, i*CELL_SIZE, fill = "black", width = LINE_THICKNESS)
        
    for i in range(GRID_WIDTH):
        canvas.create_rectangle(i*CELL_SIZE,0, i*CELL_SIZE,  GRID_HEIGHT*CELL_SIZE, fill = "black",  width = LINE_THICKNESS)

        
    for i in cells:
        #canvas.create_rectangle((i[0])*CELL_SIZE+LINE_THICKNESS/2, (i[1])*CELL_SIZE+LINE_THICKNESS/2,((i[0])+1)*CELL_SIZE-LINE_THICKNESS/2, ((i[1])+1)*CELL_SIZE-LINE_THICKNESS/2, fill = "blue")
        canvas.create_rectangle( (i[1])*CELL_SIZE+LINE_THICKNESS/2,(i[0])*CELL_SIZE+LINE_THICKNESS/2, ((i[1])+1)*CELL_SIZE-LINE_THICKNESS/2,((i[0])+1)*CELL_SIZE-LINE_THICKNESS/2, fill = "blue")
            
    for i in passage_walls:
        i.drawWall(canvas, 'blue', 1)
        
    for i in active_walls:
        i.drawWall(canvas,'red',0)
        
    if active_wall != None:
        active_wall.drawWall(canvas, 'magenta', 0)

    for i in cells:
        #canvas.create_rectangle((i[0])*CELL_SIZE+LINE_THICKNESS/2, (i[1])*CELL_SIZE+LINE_THICKNESS/2,((i[0])+1)*CELL_SIZE-LINE_THICKNESS/2, ((i[1])+1)*CELL_SIZE-LINE_THICKNESS/2, fill = "blue")
        canvas.create_rectangle( (i[1])*CELL_SIZE+LINE_THICKNESS/2,(i[0])*CELL_SIZE+LINE_THICKNESS/2, ((i[1])+1)*CELL_SIZE-LINE_THICKNESS/2,((i[0])+1)*CELL_SIZE-LINE_THICKNESS/2, fill = "blue")
            
    for i in passage_walls:
        i.drawWall(canvas, 'blue', 1)
        
    time.sleep(wait)
    tk.update()
    canvas.delete("all")

def draw_maze_solving(canvas, maze, path, visited_positions, wait = 0):
    canvas.create_rectangle(0,0, height, width, fill = "blue")
    
    for i in range(GRID_HEIGHT):
        canvas.create_rectangle(0,i*CELL_SIZE, GRID_WIDTH*CELL_SIZE, i*CELL_SIZE, fill = "black", width = LINE_THICKNESS)
        
    for i in range(GRID_WIDTH):
        canvas.create_rectangle(i*CELL_SIZE,0, i*CELL_SIZE,  GRID_HEIGHT*CELL_SIZE, fill = "black",  width = LINE_THICKNESS)
        
    for i in passage_walls:
        i.drawWall(canvas, 'blue', 1)
        
    for i in visited_positions:
        #canvas.create_rectangle((i[0])*CELL_SIZE+LINE_THICKNESS/2, (i[1])*CELL_SIZE+LINE_THICKNESS/2,((i[0])+1)*CELL_SIZE-LINE_THICKNESS/2, ((i[1])+1)*CELL_SIZE-LINE_THICKNESS/2, fill = "blue")
        canvas.create_rectangle( (i[1])*CELL_SIZE+LINE_THICKNESS/2 + CELL_SIZE/4,(i[0])*CELL_SIZE+LINE_THICKNESS/2+ CELL_SIZE/4, ((i[1])+1)*CELL_SIZE-LINE_THICKNESS/2 -CELL_SIZE/4,((i[0])+1)*CELL_SIZE-LINE_THICKNESS/2-CELL_SIZE/4, fill = "yellow")
    
    for i in path:
        canvas.create_rectangle( (i[1])*CELL_SIZE+LINE_THICKNESS/2 + CELL_SIZE/4,(i[0])*CELL_SIZE+LINE_THICKNESS/2 + CELL_SIZE/4, ((i[1])+1)*CELL_SIZE-LINE_THICKNESS/2 - CELL_SIZE/4,((i[0])+1)*CELL_SIZE-LINE_THICKNESS/2 - CELL_SIZE/4, fill = "green")

        
    tk.update()
    time.sleep(wait)
    canvas.delete("all")

out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (width,height))

#for count in range(1):
tk = Tk()
canvas = Canvas(tk, width=GRID_WIDTH*CELL_SIZE, height = GRID_HEIGHT*CELL_SIZE)
tk.title(str(count+1))
canvas.pack()
#reset  arrays to be empty

#red walls that are still going to be observed
active_walls = []
#walls that have been broken down to create a passage
passage_walls = []
#cells that have been visited so far
maze_cells = []

#start in the top left corner
first_cell = (0,0)
#turn it into a Cell object to get its walls
first_Cell = Cell(0,0)
maze_cells.append(first_cell)
#start with the walls of the first cell
for i in first_Cell.Walls:
    active_walls.append(i)

	#measure total weight, pick an active wall based on weight
while len(active_walls) > 0:
    total_weight = 0
    for w in active_walls:
        total_weight += w.weight
    active_wall = active_walls[randint(0,len(active_walls)-1)]
    
    #randomly pick wall from list of active walls, with probability based on weights
    n = random.random()*total_weight
    lower_weight = 0
    upper_weight = 0
    for i in range(len(active_walls)):
        upper_weight = lower_weight+active_walls[i].weight
        if n >= lower_weight and n <= upper_weight:
            target = i
            break
        lower_weight = upper_weight
    active_wall = active_walls[target]
    
    #
    if active_wall.first_cell not in maze_cells:
        maze_cells.append(active_wall.first_cell)
        added_cell = Cell(active_wall.first_cell[0], active_wall.first_cell[1])
        for i in added_cell.Walls:
            #careful not to re-add the cell we're going to remove!
            active_walls.append(i)
        passage_walls.append(active_wall)

        
    elif active_wall.second_cell not in maze_cells:
        maze_cells.append(active_wall.second_cell)
        added_cell = Cell(active_wall.second_cell[0], active_wall.second_cell[1])
        for i in added_cell.Walls:
            active_walls.append(i)
        passage_walls.append(active_wall)

    active_walls.remove(active_wall)
    
    #remove potential remaining duplicates
    for i in active_walls:
        if active_wall == i:
            active_walls.remove(i)
    drawMaze(canvas,active_walls, passage_walls, maze_cells, wait = 0, active_wall = active_wall)
drawMaze(canvas,active_walls, passage_walls, maze_cells, wait = 0)
output = printPicture(passage_walls)

#if uncommented, writes each finished maze to a PNG image
cv2.imwrite("oof.png",output)

out.write(output) #write each image to the AVI file

def solve_maze(canvas,maze):
    Path = []
    if explore(canvas, maze,0,0,Path, []):
        draw_maze_solving(canvas,maze, Path, [], wait = 5)
        return Path
        
    return []

def is_valid_direction(maze, row, col, direction):
    #print("checking position", row, col)
    for wall in maze:
        if direction == (1,0):
            #print("checking south direction")
            if wall.first_cell[0] == row and wall.first_cell[1] == col and wall.orientation == 1:
                #south
                #print("found south passage", wall.print_wall())
                return True
        if direction == (0,1):
            #print("checking east direction")
            if wall.first_cell[0] == row and wall.first_cell[1] == col and wall.orientation == 0:
                #east
                #print("found east passage", wall.print_wall())
                return True
        if direction == (-1,0):
           # print("checking north direction")
            if wall.first_cell[0] == row-1 and wall.first_cell[1] == col and wall.orientation == 1:
                #north
                #print("found north passage", wall.print_wall())
                return True
        if direction == (0,-1):
            #print("checking west direction")
            if wall.first_cell[0] == row and wall.first_cell[1] == col-1 and wall.orientation == 0:
                #west
                #print("found west passage", wall.print_wall())
                return True
    #print("no valid passages found")
    return False

def explore(canvas,maze,row, col, path, visited_positions):
    position = (row,col)
    
    if row < 0 or col < 0 or row >= GRID_HEIGHT or col >= GRID_WIDTH or position in visited_positions:
        return False
    
    path.append(position)
    visited_positions.append(position)
    draw_maze_solving(canvas,maze, path, visited_positions, wait = .02)

    if col == GRID_WIDTH-1 and row == GRID_HEIGHT-1:
        return True
    
    for direction in DIRECTIONS:
        if is_valid_direction(maze, row, col, direction):
            if explore(canvas,maze, row+direction[0], col+direction[1], path, visited_positions):
                return True
    
    path.pop()
    draw_maze_solving(canvas,maze, path, visited_positions, wait = .02)

    return False
    
print(solve_maze(canvas,passage_walls))
tk.destroy()
#after everything, have to put this to finalize TK so it doesn't keep crashing...
tk.mainloop()