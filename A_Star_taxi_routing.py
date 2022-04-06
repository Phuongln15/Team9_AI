from queue import Queue, PriorityQueue
import pygame as py
import time
import math

#window size 
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 750

#simple color
white = (255, 255, 255)
black = (0, 0, 0)
red = (156, 50, 50)
green = (0, 255, 0)
light_green = (104, 255, 104)
red_light = (255, 50, 50)

class Grid:
    
    def __init__(self,rows, cols, window=None, width=None, height=None):
        self.rows = rows
        self.cols = cols
        self.window = window
        self.width = width
        self.height = height
        self.selected = None
        self.building_blocks = [[CityBlocks(i, j) for j in range(cols)] for i in range(rows)]
        self.x = 0
        self.y = 0
        if self.width is not None:
            self.dif = self.width // cols
        
        count = 0
        # making the grid as a graph with connections with each other when the grid is initialized
        for i in range(rows):
            for j in range(cols):
                
                self.building_blocks[i][j].make_values(count)
                count+=1
                
        for i in range(rows):
            for j in range(cols):
                if ( rows-1) > i > 0 and 0 < j < (cols-1):
                    self.building_blocks[i][j].make_connections(left=self.building_blocks[i][j - 1], right=self.building_blocks[i][j + 1], up=self.building_blocks[i - 1][j], down=self.building_blocks[i + 1][j])
            
                elif i == 0:
                    if j == 0:
                        self.building_blocks[i][j].make_connections(right=self.building_blocks[i][j + 1], down=self.building_blocks[i + 1][j])
                    elif j == cols - 1:
                        self.building_blocks[i][j].make_connections(left=self.building_blocks[i][j - 1], down=self.building_blocks[i + 1][j])
                    else:
                        self.building_blocks[i][j].make_connections(left=self.building_blocks[i][j - 1], right=self.building_blocks[i][j + 1], down=self.building_blocks[i + 1][j])
                elif i == (rows-1):
                    if j == 0:
                        self.building_blocks[i][j].make_connections(right=self.building_blocks[i][j + 1], up=self.building_blocks[i - 1][j])
                    elif j == cols - 1:
                        self.building_blocks[i][j].make_connections(left=self.building_blocks[i][j - 1], up=self.building_blocks[i - 1][j])
                    else:
                        self.building_blocks[i][j].make_connections(left=self.building_blocks[i][j - 1], right=self.building_blocks[i][j + 1], up=self.building_blocks[i - 1][j])
                    
                else:
                    if j == 0:
                        self.building_blocks[i][j].make_connections(right=self.building_blocks[i][j + 1], up=self.building_blocks[i - 1][j], down=self.building_blocks[i + 1][j])
                    else:
                        self.building_blocks[i][j].make_connections(left=self.building_blocks[i][j - 1], up=self.building_blocks[i - 1][j], down=self.building_blocks[i + 1][j])
            
            
    def get_cord(self,pos):
        #get position of the mouse when clicked in the box

        click_x = pos[0] // self.dif
       
        click_y = pos[1] // self.dif
        return (click_x, click_y)


    def draw(self):
        #the grid is drawn 
        self.window.fill((20, 100, 50))
        for i in range((self.rows+1)):
            
            py.draw.line(self.window, (255, 255, 255), (self.x, i * self.dif ), (self.width, i * self.dif), 1)
            py.draw.line(self.window, (244, 244, 244), (i * self.dif, self.y), (i * self.dif, self.height), 1)
    
    
    def select_start(self, row, col):#get starting position 
        py.draw.rect(self.window, (255, 0, 0), (row * self.dif, col * self.dif, self.dif, self.dif))
        
        
    def select_end(self, row, col):#get/draw end position
        py.draw.rect(self.window, (255, 153, 153), (row * self.dif, col * self.dif, self.dif, self.dif) )
                
        
    def get_cubes(self):
        return self.building_blocks
    
    
    def add_buildings(self, row, col):#method to add buildings
        self.building_blocks[row][col].building_cell()
    
    
    def remove_buildings(self, row, col):#method to add blocks to the path
        self.building_blocks[row][col].unblock_cell()

    

class CityBlocks:
    
    
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.value = None
        self.blocked = False
    
    
    def make_values(self, value):#add value to each building
        self.value = value
    
    
    def make_connections(self, left=None, right=None, up=None, down=None): #make the graph of each building block in the graph
        self.left = left
        self.right = right
        self.up = up
        self.down = down
    
    
    def value(self):
        return self.value 
        
        
    def print_row_col(self):
        return self.row, self.column   
        
        
    def show_connections(self):
    
        return [self.left, self.right, self.up, self.down]
    
    
    def building_cell(self):#turns the cube into a blocked cube
        self.blocked = True
    
    
    def unblock_cell(self):
        self.blocked = False
    
    
    def get_cell_condition(self):
        return self.blocked


#button function 
#x=top-left corner of the rectangle x-coordinate
#y=top-left corner of the rectangle y-coordinate
#w=width of the rectangle
#h=height of the rectangle
#ic=inactive button color
#ac=if button is pressed
def button (msg, x, y, w, h, ic, ac, action=None, parameters=None):
    mouse = py.mouse.get_pos()
    click = py.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        py.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameters:
                action(parameters)
            else:
                action()
        
    else:
        py.draw.rect(screen, ic, (x, y, w, h))
    
    smallText = smallfont.render(msg, True, black)
    textRect = smallText.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(smallText, textRect) 



def intro():
    
    while True:
        for event in py.event.get():
            
            if event.type == py.QUIT:
                py.quit()
                quit()
            
                
        screen.fill((200, 100, 50))
        textSurface = myfont.render("AStar for Taxi Routing", True, white )
        textRect = textSurface.get_rect()
        textRect.center = (WINDOW_WIDTH/2), (WINDOW_HEIGHT/16)
        screen.blit(textSurface, textRect)
        
        
        button("Start", 250, 450, 100, 50, green, light_green, a_star_loop)
        
        py.display.update()
        clock.tick(15)
        
        
def d(current, neighbor):
    x1, y1 = current.print_row_col()
    x2, y2 = current.print_row_col()
    
    return abs(x2-x1) + abs(y2-y1)


def heuristic(node, e):
    x1, y1 = node.print_row_col()
    x2, y2 = e.print_row_col()
    
    return abs(x2-x1) + abs(y2-y1)


def a_star(s, e, rows, cols):
    openSet = PriorityQueue()
    
    openSet.put((heuristic(s, e), 0, s))
    parentMap = {}
    visited = [False for i in range(rows * cols)]
    gScore = { i: float('inf') for i in range(rows*cols)}
    gScore[s.value] = 0
    traversal = []
    fScore = { i: float('inf') for i in range(rows*cols)}
    fScore[s.value] = 0
    
    count = 2500
    while not openSet.empty():
        current = openSet.get()
        
        if current[2] == e:            
            break
        
        for neighbor  in current[2].show_connections():
            if neighbor and not neighbor.get_cell_condition():
                tentative_gScore = gScore[current[2].value] + d(current[2], neighbor)
                traversal.append(neighbor)
                # print(tentative_gScore)
                if tentative_gScore < gScore[neighbor.value]:
                    
                    count -= 1
                    parentMap[neighbor] = current[2]
                    gScore[neighbor.value] = tentative_gScore
                    fScore[neighbor.value] = gScore[neighbor.value] + heuristic(neighbor, e)
                    
                    openSet.put((fScore[neighbor.value], count,  neighbor))
                        
                    
                    visited[neighbor.value] = True
                    
    return parentMap, traversal




def a_star_loop():
    
    gridSurface = py.Surface((601, 600))
    state = True
    rows = 50
    cols = 50
    grid = Grid(rows, cols, gridSurface, 601, 600 )
    clicked = None
    run = True
    once = True
    complete_first_time = False
    end = False
    start = False
    find = False
    starting_position = None
    end_position = None
    cubes_ = grid.get_cubes()
    make_wall = False
    del_wall = False
    buildings = {}
    diff = WINDOW_WIDTH // 50
    
    while run:
        
        #drawing the grid
        grid.draw()
        screen.fill(white)
              
        button("Start position", 10, 610, 100, 50, red, red_light)
        
        button("End position", 120, 610, 100, 50, red, red_light)
        
        button("Add buildings", 330, 610, 100, 50, red, red_light)
        button("Remove buildings", 440, 610, 100, 50, red, red_light)
        
        
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            if event.type == py.MOUSEBUTTONDOWN:
                pos = py.mouse.get_pos()
                clicked = grid.get_cord(pos)
                
        if state:            
            if clicked:
                
                if (10 + 100) > pos[0] > 10 and (610 + 50) > pos[1] > 610:
                    start = True
                    
                if (120 + 100) > pos[0] > 120 and (610 + 50) > pos[1] > 610:
                    start = False
                    end = True
                if end_position and starting_position:
                    if not once:
                        if (230 + 100) > pos[0] > 230 and (680 + 50) > pos[1] > 680:
                            find = True
                            end = False
                if (330 + 100) > pos[0] > 330 and (610 + 50) > pos[1] > 610:
                    start = False
                    end = False
                    find = False
                    make_wall = True    
                if (440 + 140) > pos[0] > 440 and (610 + 50) > pos[1] > 610:
                    start = False
                    end = False
                    find = False
                    make_wall = False
                    del_wall = True 
                    
                
            if start: # if start is clicked then we can then select some box in the grid and it will be highlighted in red color
                    if buildings: #showing the blocked boxes
                        for i in buildings.values():
                            py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))
                    
                    grid.select_start(clicked[0], clicked[1])
                    starting_position = clicked
                    screen.blit(gridSurface, (0, 0))
                    py.display.update() 
                    
                        
            elif end: # likewise for the end position but in pink color
                    if buildings: #showing the blocked boxes
                        for i in buildings.values():
                            py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))
                    
                                        
                    grid.select_end(clicked[0], clicked[1]) 
                    end_position = clicked
                    if starting_position:
                        grid.select_start(starting_position[0], starting_position[1])
                    
                            
                    button("Find path", 230, 680, 100, 50, red, red_light)
                    screen.blit(gridSurface, (0, 0))
                    py.display.update()  
            elif find: # the path finding occurs in here
                if buildings: #showing the blocked boxes
                    for i in buildings.values():
                        py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))
                            
                               
                if (starting_position[0] < 50 and starting_position[1] <  50) and (end_position[0] < 50 and end_position[1] < 50):  
                    grid.select_start(starting_position[0], starting_position[1])
                    
                    
                    # the function returns the dictionary of the path that it took to get the end position but is in reverse order and also the traversal path
                    path, traversal = a_star(  cubes_[ int( starting_position[0]  ) ]  [ int( starting_position[1] ) ]   , cubes_[ int( end_position[0] ) ]  [ int(end_position[1]) ], rows, cols)
                    for i in traversal: #shows the traversal
                        bo = py.draw.rect(screen, (255, 100, 100), (i.print_row_col()[0] * diff, i.print_row_col()[1] * diff, diff, diff), 1)
                        py.time.delay(5)
                        py.display.update(bo)
                    
                    # starting node
                    curr = cubes_[ int( end_position[0] ) ]  [ int(end_position[1]) ]
                    curr = path[curr]
                    grid.select_end(curr.print_row_col()[0], curr.print_row_col()[1])
                    # to highlight the path 
                    while curr != cubes_[ int( starting_position[0]  ) ]  [ int( starting_position[1]) ]:
                            
                            bo = py.draw.rect(gridSurface, (255, 0, 0), (curr.print_row_col()[0] * diff, curr.print_row_col()[1] * diff, diff, diff), 1)
                            if not complete_first_time:
                                screen.blit(gridSurface, (0, 0))
                                py.display.update(bo)
                                py.time.delay(3)
                                
                            curr = path[curr]
                    state = False # to pause the loop---kind of!
                    
                    
                    if not complete_first_time:  
                        complete_first_time = True
                        
                        screen.blit(gridSurface, (0, 0))
                        py.display.update()
                else:
                    if (starting_position[0] > 50 or starting_position[1] >  50):
                        button("Please Select a Starting Position!", 602, 10, 400, 50, red, red)
                        screen.blit(gridSurface, (0, 0))
                        py.display.update()
                    elif (end_position[0] > 50 or end_position[1] >  50):
                        button("Please select an End Position!", 602, 0, 400, 50, red, red)
                        screen.blit(gridSurface, (0, 0))
                        py.display.update()
                    else:
                        button("Please select both Positions!", 602, 0, 400, 50, red, red)
                        screen.blit(gridSurface, (0, 0))
                        py.display.update()
            elif make_wall:
                if (clicked[0] < 50 and clicked[1] <  50):  #to ensure that the clicked has tuple that is on the grid
                    bo = py.draw.rect(gridSurface, (0, 0, 0), (clicked[0] * diff, clicked[1] * diff, diff, diff))
                    buildings[  cubes_[clicked[0]] [clicked[1]].value  ] = clicked
                    grid.add_buildings(clicked[0], clicked[1])
                    screen.blit(gridSurface, (0, 0))
                    py.display.update(bo)            
            elif del_wall:
                if (clicked[0] < 50 and clicked[1] <  50):  #to ensure that the clicked has tuple that is on the grid            
                    if buildings:
                        try:
                            del buildings[  cubes_[clicked[0]] [clicked[1]].value  ]
                            grid.remove_buildings(clicked[0], clicked[1])
                            for i in buildings.values():
                                py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))
                            if starting_position and end_position:
                                button("Find path", 230, 680, 100, 50, red, red_light)
                                grid.select_start(starting_position[0], starting_position[1])
                                grid.select_end(end_position[0], end_position[1])
                            screen.blit(gridSurface, (0, 0))
                            py.display.update()
                        except Exception:
                            pass
                        
        
        else:# same function but it just shows the same path but it will show all the path at once 
            if buildings: #showing the blocked boxes
                        for i in buildings.values():
                            py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))
                        
        
            grid.select_start(starting_position[0], starting_position[1])
            
            curr = cubes_[ int( end_position[0] ) ]  [ int(end_position[1]) ]
            grid.select_end(curr.print_row_col()[0], curr.print_row_col()[1])
            curr = path[curr]
            
            while curr != cubes_[ int( starting_position[0]  ) ]  [ int( starting_position[1]) ]:
                    
                    py.draw.rect(gridSurface, (255, 0, 100), (curr.print_row_col()[0] * diff, curr.print_row_col()[1] * diff, diff, diff), 1)
                    
                        
                    curr = path[curr]
                    
            
            button("Refresh", 230, 680, 100, 50, red, red_light, a_star_loop )
            
            screen.blit(gridSurface, (0, 0))               
            py.display.update()
                
                            
        if once:
            once = False
            screen.blit(gridSurface, (0, 0))
            py.display.update()  
            
            
        clock.tick(60)
    py.quit()
    quit()
    
#####################*************************#######################



if __name__ == "__main__":
    #intialize pygame
    py.init()
    key = None
    py.display.set_caption("Taxi Routing")
    myfont = py.font.SysFont('Comic Sans MS', 30) 
    smallfont = py.font.SysFont('Comic Sans MS', 12)   
    screen = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = py.time.Clock()
    intro()    