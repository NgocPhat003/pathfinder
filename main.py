import pygame
import math
from queue import PriorityQueue 
from queue import Queue
import itertools
import sys

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf',20)
spot_width = 25




                
# Function to calculate heuristic value
def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5

# Class for storing spot's information
class Spot:
    def __init__(self, row, col, width):
        self.width = spot_width
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.neighbors = []
        

    def get_pos(self):
        return self.col , self.row

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_path(self):
        self.color = PURPLE
    
    def make_end(self):
        self.color = YELLOW

    def is_blocked(self):
        return self.color == GREY or self.color == TURQUOISE
    
    def is_opened(self):
        return self.color == WHITE

    def update_coord(self):
        self.x = self.col * self.width
        self.y = self.row * self.width

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid, map):
        self.neighbors = []
        if (self.row > 1 and self.col < map.noCol - 2 and not grid[self.col + 1 ][self.row - 1].is_blocked()) : # UPRIGHT
            self.neighbors.append(grid[self.col + 1][self.row - 1])

        if self.col > 1 and not grid[self.col - 1][self.row].is_blocked(): # LEFT
            self.neighbors.append(grid[self.col - 1][self.row])

        if self.row > 1 and self.col > 1 and not grid[self.col - 1][self.row - 1].is_blocked(): # UPLEFT
            self.neighbors.append(grid[self.col - 1][self.row - 1])

        if self.row > 1 and not grid[self.col][self.row - 1].is_blocked(): # UP
            self.neighbors.append(grid[self.col][self.row - 1])

        if self.row < map.noRow - 2 and self.col > 1 and not grid[self.col - 1][self.row + 1].is_blocked(): # DOWNLEFT
            self.neighbors.append(grid[self.col - 1][self.row + 1])

        if self.col < map.noCol - 2 and not grid[self.col + 1][self.row].is_blocked(): # RIGHT
            self.neighbors.append(grid[self.col + 1][self.row])

        if self.row < map.noRow - 2 and not grid[self.col][self.row + 1].is_blocked(): # DOWN
            self.neighbors.append(grid[self.col][self.row + 1])

        if self.row < map.noRow - 2 and self.col < map.noCol - 2 and not grid[self.col + 1][self.row + 1].is_blocked(): # DOWNRIGHT
            self.neighbors.append(grid[self.col + 1][self.row + 1])


# Class to store the detail of the input file
class Map():
    def __init__(self):
        self.noRow = 0
        self.noCol = 0
        self.start = Spot(0,0,spot_width)
        self.dest = Spot(0,0,spot_width)
        self.no_Of_waypoint = 0
        self.waypoints = []
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
        start_end_point_detail = [int(i) for i in start_end_point_detail_line.split(",")]
        self.no_Of_waypoint = (len(start_end_point_detail) - 4) / 2
        self.start.col = start_end_point_detail[0]
        self.start.row = self.noRow - start_end_point_detail[1] - 1
        self.dest.col = start_end_point_detail[2]
        self.dest.row = self.noRow - start_end_point_detail[3] - 1
        self.start.update_coord()
        self.dest.update_coord()
        if self.no_Of_waypoint > 0:
            for i in range(4, len(start_end_point_detail), 2):
                waypoint = Spot(0, 0, spot_width)
                waypoint.col = start_end_point_detail[i]
                waypoint.row = self.noRow - start_end_point_detail[i+1] - 1
                waypoint.update_coord()
                
                self.waypoints.append(waypoint)


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
    
    
    # Create grid list which store all the spot on screen
    def create_grid(self):
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
            pygame.draw.line(win, BLACK, (0, i * spot_width), (self.WIN_WIDTH, i * spot_width))
            for j in range(self.noCol):
                pygame.draw.line(win, BLACK, (j * spot_width, 0), (j * spot_width, self.WIN_HEIGHT))

    def draw_start_end_point(self, win, grid):     
        self.start.color = ORANGE
        self.dest.color = GREEN
        grid[self.start.col][self.start.row].color = ORANGE
        grid[self.dest.col][self.dest.row].color = YELLOW
        # for i in range(len(self.waypoints)):
        #     grid[self.waypoints[i].col][self.waypoints[i].row] = BLUE
        
        
    #Drawing the obstacles

    def draw_obstacle(self, grid): 
        def connect_two_spot(grid, cur_spot: tuple, prev_spot: tuple, map):
            path = [] 
            def eucliean_distance(x1, y1, x2, y2):
                return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5
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
                        if 0 < x_next + position[0] < map.noCol and 0 < y_next + position[1] < map.noRow:
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
            
        for z in range(int(self.no_Of_waypoint)):
            x = self.waypoints[z].col 
            y = self.waypoints[z].row 
            grid[x][y].color = BLUE

    # Function to draw the found path from the algorithm
    def reconstruct_path(self, came_from, current, draw, weight):
        weight = -1
        last = current
        while current in came_from:
            if current.col == last.col or current.row == last.row:
                weight += 1
            else:
                weight += 1.5
            last = current
            current = came_from[current]
            current.make_path()

        if current.col == last.col or current.row == last.row:
            weight += 1
        else:
            weight += 1.5

        draw()
            
        return weight
    
    # A* algorithm
    def astar(self, draw, grid, start, end, weight):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for col in grid for spot in col}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start] = h(start.get_pos(), end.get_pos())
        

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                weight = self.reconstruct_path(came_from, end, draw, weight)
                end.make_end()
                return True, weight

            for neighbor in current.neighbors:
                if neighbor.col == current.col or neighbor.row == current.row:
                    temp_g_score = g_score[current] + 1
                else:
                    temp_g_score = g_score[current] + 1.5

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()

            if current != start:
                current.make_closed()

        return False

    # BFS algorithm
    def BFS(self, draw, grid, start, end, weight):
        open_set = Queue()
        count = 0
        open_set.put((count, start))
        came_from = {}
        
        open_set_hash = {start}
        
        
        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[1]
            open_set_hash.remove(current)
            

            if current == end:
                weight = self.reconstruct_path(came_from, end, draw, weight)
                if end.color != BLUE:
                    end.make_end()
                return True, weight

            for neighbor in current.neighbors:
                if neighbor.color != RED and neighbor.color != ORANGE :
                    if neighbor not in open_set_hash:
                        came_from[neighbor] = current
                        count += 1
                        open_set.put((count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()

            if current != start:
                current.make_closed()
        return False

    # Djastra algorithm
    def Blind(self, draw, grid, start, end, weight):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for col in grid for spot in col}
        g_score[start] = 0
        
        

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                weight = self.reconstruct_path(came_from, end, draw, weight)
                end.make_end()
                return True, weight

            for neighbor in current.neighbors:
                if neighbor.col == current.col or neighbor.row == current.row:
                    temp_g_score = g_score[current] + 1
                else:
                    temp_g_score = g_score[current] + 1.5

                if temp_g_score < g_score[neighbor]:
                    
        
                    if neighbor not in open_set_hash:
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        count += 1
                        open_set.put((g_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()

            if current != start:
                current.make_closed()

        return False

    # Function to find path to destination that goes through all checkpoint
    def waypoint_pathfinder(self,grid, draw):
        def calculate_path_distance(path):
            total_distance = 0
            for i in range(len(path) - 1):
                total_distance += h(path[i].get_pos(), path[i+1].get_pos())
            return total_distance
        minimum = float('inf')
        shortest_path = None
        waypoint_permutations = itertools.permutations(self.waypoints)

        for perm in waypoint_permutations:
            path = [self.start] + list(perm) + [self.dest]
            distance = calculate_path_distance(path)
            if distance < minimum:
                minimum = distance
                shortest_path = path

        def astar_only_path(map, draw, grid, start, end, isEnd):
            weight = 0
            count = 0
            open_set = PriorityQueue()
            open_set.put((0, count, start))
            came_from = {}
            g_score = {spot: float("inf") for col in grid for spot in col}
            g_score[start] = 0
            f_score = {spot: float("inf") for row in grid for spot in row}
            f_score[start] = h(start.get_pos(), end.get_pos())
        

            open_set_hash = {start}

            while not open_set.empty():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                current = open_set.get()[2]
                open_set_hash.remove(current)

                if current == end:
                    weight = map.reconstruct_path(came_from, end, draw, weight)
                    if isEnd:
                        end.make_end()
                    else:
                        start.color = BLUE
                    return True, weight

                for neighbor in current.neighbors:
                    if neighbor.col == current.col or neighbor.row == current.row:
                        temp_g_score = g_score[current] + 1
                    else:
                        temp_g_score = g_score[current] + 1.5

                    if temp_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                        if neighbor not in open_set_hash:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            open_set_hash.add(neighbor)
                            

                draw()

            return False
        weight = 0
        isEnd = False
        for i in range(len(shortest_path) - 1):
            if i == len(shortest_path) - 1:
                isEnd = True
            x1 = shortest_path[i].col
            y1 = shortest_path[i].row
            x2 = shortest_path[i+1].col
            y2 = shortest_path[i+1].row
            weight += astar_only_path(self, draw, grid, grid[x1][y1], grid[x2][y2], isEnd)[1]
        
        return weight


    # Drawing the window
    def draw(self, win, grid, weight):
        win.fill(WHITE)

        for col in grid:
            for spot in col:
                spot.draw(win)

        self.draw_grid(win)

        # Drawing border
        for i in range(0, self.noCol):
            grid[i][0].color = GREY
        
        for y in range(0, self.noRow):
            grid[i][y].color = GREY
            
        for j in range(0, self.noRow):
            grid[0][j].color = GREY
            
        for z in range(0, self.noCol):
            grid[z][j].color = GREY
        self.draw_start_end_point(win, grid)
        
        weight_cost = "Cost: " + str(weight)
        text = font.render(weight_cost, True, RED)
        textRect = text.get_rect()
        textRect.center = (100, 15)
        win.blit(text,textRect)

        
        pygame.display.update()
 
                

            
              
def main():
    map = Map()
    file_name = 0
    option = 0
    if len(sys.argv) == 5:
        for i in range(len(sys.argv) - 1):
            if sys.argv[i] == "--file":
                file_name = sys.argv[i + 1]
            elif sys.argv[i] == "--option":
                option = sys.argv[i + 1]

        if file_name is None or file_name == "":
            print("Cannot find file")
            exit(0)
        if option is None or option == "":
            print("Invalid option")
            exit(0)

    map.read_input_file(file_name)
    WIN_WIDTH = map.noCol*spot_width
    WIN_HEIGHT = map.noRow*spot_width
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    grid = map.create_grid()
    weight = 0
    run = True
    
    
    map.draw(WIN,grid,weight)
    map.draw_obstacle(grid)
    for col in grid:
        for spot in col:
            spot.update_neighbors(grid,map)

    
    while run:
        map.draw(WIN,grid, weight)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                weight = 0
                if event.key == pygame.K_SPACE and map.start and map.dest:
                    if option == "astar":
                        weight = map.astar(lambda: map.draw(WIN, grid,weight), grid, grid[map.start.col][map.start.row], grid[map.dest.col][map.dest.row], weight)[1]  
                    elif option == "greedy":
                        weight = map.BFS(lambda: map.draw(WIN, grid,weight), grid, grid[map.start.col][map.start.row], grid[map.dest.col][map.dest.row], weight)[1]
                    elif option == "blind":
                        weight = map.Blind(lambda: map.draw(WIN, grid,weight), grid, grid[map.start.col][map.start.row], grid[map.dest.col][map.dest.row], weight)[1]
                    elif option == "waypoints":
                        weight = map.waypoint_pathfinder(grid, lambda: map.draw(WIN, grid,weight))

                    
                    
                    

main()



    

    



    
