import xml.etree.ElementTree as ET # This is for reading the xml file easier. :)
import math

def create_atmosphere():
    #######################################################################################################################################################################################################################################################
    ##########################################################  In this function, we create the atmosphere from the given xml file .                                                           ############################################################
    ##########################################################  This function take no inputs and returns an array that includes obstacles, robot starting place and its goal aka the battery.  ############################################################
    #######################################################################################################################################################################################################################################################

    tree = ET.parse('/Users/ImanAlipour/Documents/Programming/Python/AI_HWs/IMP1/SampleRoom.xml')  # This line reads the xml file and parses it, now we can use getElementsByName('folan') to find all of the elements we want.
    root = tree.getroot()

    number_of_rows = len(root)       # Assuming we have an n*m grid, I find n and m from xml file
    number_of_coloumns = len(root[0])    
    atmosphere = [['' for i in range(number_of_coloumns)] for j in range(number_of_rows)]   # We create an empty array and fill it up from what we read from input.
    #graphical_atmosphere = [['' for i in range(number_of_coloumns)] for j in range(number_of_rows)]
    robot_x_initial = 0
    robot_y_initial = 0

    for i in range(number_of_rows):
        for j in range(number_of_coloumns):
            atmosphere[i][j] = '' + root[i][j].text
            if(atmosphere[i][j] == 'robot'):
                robot_x_initial = i
                robot_y_initial = j
            if(atmosphere[i][j] == 'Battery'):
                battery_x = i
                battery_y = j
    return atmosphere, robot_x_initial, robot_y_initial, battery_x, battery_y

atmosphere, robot_x_initial, robot_y_initial, battery_x, battery_y = create_atmosphere()    # Create the atmosphere, all of the problems variables are in this atmosphere

def bfs_h(i, j):
    return 0
def manhatan_dist_h(i, j):
    return abs(battery_x - i + 1) + abs(battery_y - j + 1)
def euclidean_dist_h(i, j):
    return math.floor(math.sqrt(abs(battery_x - i + 1)**2 + abs(battery_y - j + 1)**2))
def g_n(i, j):
    return 1

def create_robot_initial_view():
    # Returns robots initial view
    number_of_rows = len(atmosphere)
    number_of_coloumns = len(atmosphere[0])
    view = [[' ' for i in range(number_of_coloumns+2)] for j in range(number_of_rows+2)]
    view[robot_x_initial+1][robot_y_initial+1] = u"\U0001F916"
    view[robot_x_initial][robot_y_initial+1] = '?'
    view[robot_x_initial+1][robot_y_initial] = '?'
    view[robot_x_initial+2][robot_y_initial+1] = '?'
    view[robot_x_initial+1][robot_y_initial+2] = '?'
    return view


def get_neighbors(robot_x, robot_y, view):
    neighbors = []
    if view[robot_x-1][robot_y] == '?':
        neighbors.append((euclidean_dist_h(robot_x-1, robot_y)+g_n(robot_x-1, robot_y), robot_x-1, robot_y))
    if view[robot_x][robot_y-1] == '?':
        neighbors.append((euclidean_dist_h(robot_x, robot_y-1)+g_n(robot_x, robot_y-1), robot_x, robot_y-1))
    if view[robot_x+1][robot_y] == '?':
        neighbors.append((euclidean_dist_h(robot_x+1, robot_y)+g_n(robot_x+1, robot_y), robot_x+1, robot_y))
    if view[robot_x][robot_y+1] == '?':
        neighbors.append((euclidean_dist_h(robot_x, robot_y+1)+g_n(robot_x, robot_y+1), robot_x, robot_y+1))
    return neighbors

def explore(node, view, x, y):
    cost, i, j = node
    if i == 0 or j == 0 or i == len(atmosphere)+1 or j == len(atmosphere[0])+1:
        view[i][j] = '#'
        i = x
        j = y
    elif atmosphere[i-1][j-1] == 'obstacle':
        view[i][j] = '#'
        i = x
        j = y
    elif atmosphere[i-1][j-1] == 'empty':
        view[i][j] = '' + u"\U0001F916"
        view[x][y] = 'X'
        if view[i+1][j] != 'X' and view[i+1][j] != '#':
            view[i+1][j] = '?'
        if view[i][j+1] != 'X' and view[i][j+1] != '#':
            view[i][j+1] = '?'
        if view[i][j-1] != 'X' and view[i][j-1] != '#':
            view[i][j-1] = '?'
        if view[i-1][j] != 'X' and view[i-1][j] != '#':
            view[i-1][j] = '?'
    else:
        view[i][j] = 'Y'
        view[x][y] = 'X'
    return i, j

def print_view(view):
    s = [[str(e) for e in row] for row in view]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '|\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))
    print()
    print()

def a_star():
    # Returns a path from start to end
    frontier = []
    reached_goal = 0
    robot_x = robot_x_initial+1
    robot_y = robot_y_initial+1
    robot_view = create_robot_initial_view()
    moves = 0

    while reached_goal == 0:
        new_neighbors = get_neighbors(robot_x, robot_y, robot_view)
        for i in new_neighbors:
            if i not in frontier:
                frontier.append(i)
        print('Current frontier(f_n, x, y): ' + str(frontier))
        node_to_be_explored = frontier.pop(frontier.index(min(frontier, key = lambda t: t[0]))) # Select a node to explore, remove it from frontier
        moves += 1
        print()
        print('Node, chosen to be extended(f_n, x, y): ' + str(node_to_be_explored))
        print()
        print_view(robot_view)
        robot_x, robot_y = explore(node_to_be_explored, robot_view, robot_x, robot_y)
        if robot_view[robot_x][robot_y] == 'Y':
            print('End of algorithm.')
            print()
            reached_goal == 1
            print_view(robot_view)
            print()
            print('I found the battery with ' + str(moves) + ' number of moves! :)')
            print()
            break
        elif len(frontier) == 0:
            print('End of algorithm.')
            print()
            print_view(robot_view)
            print()
            print('Goal is unreachable! :(')
            print()
            reached_goal == -1
            break
    return moves

def get_neighbors2(robot_x, robot_y, view):
    neighbors = []
    if view[robot_x-1][robot_y] == '?':
        neighbors.append((bfs_h(robot_x-1, robot_y)+g_n(robot_x-1, robot_y), robot_x-1, robot_y))
    if view[robot_x][robot_y-1] == '?':
        neighbors.append((bfs_h(robot_x, robot_y-1)+g_n(robot_x, robot_y-1), robot_x, robot_y-1))
    if view[robot_x+1][robot_y] == '?':
        neighbors.append((bfs_h(robot_x+1, robot_y)+g_n(robot_x+1, robot_y), robot_x+1, robot_y))
    if view[robot_x][robot_y+1] == '?':
        neighbors.append((bfs_h(robot_x, robot_y+1)+g_n(robot_x, robot_y+1), robot_x, robot_y+1))
    return neighbors

def bfs():
    # Returns a path from start to end
    frontier = []
    reached_goal = 0
    robot_x = robot_x_initial+1
    robot_y = robot_y_initial+1
    robot_view = create_robot_initial_view()
    moves = 0

    while reached_goal == 0:
        new_neighbors = get_neighbors2(robot_x, robot_y, robot_view)
        for i in new_neighbors:
            if i not in frontier:
                frontier.append(i)
        print('Current frontier(f_n, x, y): ' + str(frontier))
        node_to_be_explored = frontier.pop(frontier.index(min(frontier, key = lambda t: t[0]))) # Select a node to explore, remove it from frontier
        moves += 1
        print()
        print('Node, chosen to be extended(f_n, x, y): ' + str(node_to_be_explored))
        print()
        print_view(robot_view)
        robot_x, robot_y = explore(node_to_be_explored, robot_view, robot_x, robot_y)
        if robot_view[robot_x][robot_y] == 'Y':
            reached_goal == 1
            print()
            print('End of algorithm.')
            print_view(robot_view)
            print()
            print('I found the battery with ' + str(moves) + ' number of moves! :)')
            print()
            break
    return moves
        

#a_star()
bfs()

for i in atmosphere:
    print(i)
print()