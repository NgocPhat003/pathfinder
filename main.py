import pygame
import math
import queue
import queue 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

spot_width = 40


class Spot:
    def __init__(self, row, col, width):
        self.width = spot_width
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = WHITE

    def is_blocked(self):
        return self.color == BLACK
    
    def is_opened(self):
        return self.color == WHITE

    def update_coord(self):
        self.x = self.col * self.width
        self.y = self.row * self.width

    def draw(self, win):
	    pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        

def eucliean_distance(x1, y1, x2, y2):
        return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5

def connect_two_spot(grid, cur_spot: tuple, prev_spot: tuple, map):
    path = [] 
    if prev_spot[0] == cur_spot[0]:
        for match in range(0, abs(prev_spot[1] - cur_spot[1]) + 1):
            if cur_spot[1] > prev_spot[1]:
                
                path.append((prev_spot[0], prev_spot[1] + match))

            else:
                
                path.append((prev_spot[0], cur_spot[1] + match))

    elif prev_spot[1] == cur_spot[1]:
        for match in range(0, abs(prev_spot[0] - cur_spot[0]) + 1):
            if cur_spot[0] > prev_spot[0]:
                
                path.append((prev_spot[0] + match, prev_spot[1]))

            else:
                
                path.append((cur_spot[0] + match, cur_spot[1]))
    else:           
        positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
        x_next = prev_spot[0]
        y_next = prev_spot[1]
        
        while not (x_next == cur_spot[0] and y_next == cur_spot[1]):
            
            minimum = map.noRow * map.noCol
            x_tmp = x_next
            y_tmp = y_next
            for position in positions:
                if 0 < x_next + position[0] < map.noRow and 0 < y_next + position[1] < map.noCol:
                    if x_next + position[0] == cur_spot[0] and y_next + position[1] == cur_spot[1]:
                        x_tmp = cur_spot[0]
                        y_tmp = cur_spot[1]
                        break
                    z = grid[x_next + position[0]][y_next + position[1]]
                    if grid[x_next + position[0]][y_next + position[1]].color==WHITE:
                        path_weight = round(eucliean_distance(x_next + position[0], y_next + position[1], cur_spot[0], cur_spot[1]), 2)
                        
                        if position[0] == 0 or position[1] == 0:
                            path_weight += 1
                        else:
                            path_weight += 1.50
                        if path_weight < minimum:
                            minimum = path_weight
                            x_tmp = x_next + position[0]
                            y_tmp = y_next + position[1]

            x_next = x_tmp
            y_next = y_tmp
            path.append((x_next,y_next))
            
    return path

class Map():
    def __init__(self):
        self.noRow = 0
        self.noCol = 0
        self.start = Spot(0,0,spot_width)
        self.dest = Spot(0,0,spot_width)
        self.no_Of_obstacle = 0
        self.obstacle = []
        self.WIN_WIDTH = 0
        self.WIN_HEIGHT = 0
        
    
        

    def get_start_coord(self):
        
        return self.start.x, self.start.y

    def get_dest_coord(self):
        return self.dest.x, self.dest.y

    # Read file to create the map
    def read_input_file(self, filename: str):
        input_file = open(filename, "r")
        # Getting the dimension
        dimension_detail_line = input_file.readline().strip("\\ \n\r\t")
        self.noCol = int(dimension_detail_line.split(",")[0]) + 1
        self.noRow = int(dimension_detail_line.split(",")[1]) + 1

        self.WIN_WIDTH = self.noCol*spot_width
        self.WIN_HEIGHT = self.noRow*spot_width

        # Get location of the starting position and the destination
        start_end_point_detail_line = input_file.readline().strip("\\ \n\r\t")
        self.start.col = int(start_end_point_detail_line.split(",")[0])
        self.start.row = self.noRow - int(start_end_point_detail_line.split(",")[1]) - 1
        self.dest.col = int(start_end_point_detail_line.split(",")[2])
        self.dest.row = self.noRow - int(start_end_point_detail_line.split(",")[3]) - 1
        self.start.update_coord()
        self.dest.update_coord()


        # Get the number of obstacles and details about them
        no_of_obstacle_detail_line = input_file.readline().strip("\\ \n\r\t")
        self.no_Of_obstacle = int(no_of_obstacle_detail_line)
        for i in range(self.no_Of_obstacle):
            shape_coord = []
            shape_detail_line = input_file.readline().strip("\\ \n\r\t")
            temp = [int(i) for i in shape_detail_line.split(",")]  
            for j in range(0, len(temp), 2):
                shape_coord.append((temp[j] , self.noRow - temp[j+1] - 1))

            self.obstacle.append(shape_coord)
    
    
    # Create grid list 
    def create_grid(self, WIN_WIDTH, WIN_HEIGHT):
        grid = []
        
        for i in range(self.noCol):
            grid.append([])
            for j in range(self.noRow):
                spot = Spot(j, i, spot_width)
                spot.update_coord
                grid[i].append(spot)

        return grid
    
    # Drawing the grid
    def draw_grid(self, win):
       
        for i in range(self.noRow):
            pygame.draw.line(win, GREY, (0, i * spot_width), (self.WIN_WIDTH, i * spot_width))
            for j in range(self.noCol):
                pygame.draw.line(win, GREY, (j * spot_width, 0), (j * spot_width, self.WIN_HEIGHT))

    def draw_start_end_point(self, win, grid):
        self.start.color = ORANGE
        self.dest.color = GREEN
        grid[self.start.col][self.start.row].color = ORANGE
        grid[self.dest.col][self.dest.row].color = GREEN
        
        
    

    def draw_obstacle(self, grid):
        
        for i in range(0, self.no_Of_obstacle):
            path = [(self.obstacle[i][0][0],self.obstacle[i][0][1])]
            grid[self.obstacle[i][0][0]][self.obstacle[i][0][1]].color = BLACK
            for spot in range(1, len(self.obstacle[i])):
                cur_spot = self.obstacle[i][spot]
                prev_spot = self.obstacle[i][spot-1]
                path.extend(connect_two_spot(grid, cur_spot, prev_spot, self))
                
            path.extend(connect_two_spot(grid,self.obstacle[i][len(self.obstacle[i])-1],self.obstacle[i][0], self))
            for j in range(0, len(path)):
                grid[path[j][0]][path[j][1]].color = TURQUOISE  

         

    # Drawing the window
    def draw(self, win, grid):
        win.fill(WHITE)

        for col in grid:
            for spot in col:
                spot.draw(win)

        self.draw_grid(win)

        # Drawing border
        for i in range(0, self.noCol):
            grid[i][0].color = BLACK
        
        for y in range(0, self.noRow):
            grid[i][y].color = BLACK
            
        for j in range(0, self.noRow):
            grid[0][j].color = BLACK
            
        for z in range(0, self.noCol):
            grid[z][j].color = BLACK
        self.draw_start_end_point(win, grid)
        

        
        pygame.display.update()
 
                

            
              


      

def main():
    
    map = Map()
    map.read_input_file("input.txt")
    WIN_WIDTH = map.noCol*spot_width
    WIN_HEIGHT = map.noRow*spot_width
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    grid = map.create_grid(WIN_WIDTH, WIN_HEIGHT)
    
    run = True
    map.draw(WIN,grid)
    map.draw_obstacle(grid)

    while run:
        map.draw(WIN,grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

main()


    

    



    
