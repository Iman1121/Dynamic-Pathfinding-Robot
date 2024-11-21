import pygame
import sys
import math
import heapq
from obstacles import obstacles

# Initialize pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
transparent_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Player with Transparent Circle")

class Agent:
    def __init__(self, x, y, speed, size, rect, colour):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.rect = rect
        self.colour = colour
        self.frontier = []

    def get_obj(self):
        return self.rect

    def traverse(self, goal, detection_range):
        x = goal.x
        y = goal.y
        if distance(Node(self.x + self.size // 2, self.y + self.size // 2), goal) < detection_range: # Check if goal is in range
            return False
        difference_x = (self.x + self.size // 2) - x
        difference_y = (self.y + self.size // 2) - y
        if difference_x > 0:
            if abs(difference_x) <= self.speed:
                self.x -= difference_x
            else:
                self.x -= self.speed
        elif difference_x < 0:
            if abs(difference_x) <= self.speed:
                self.x -= difference_x
            else:
                self.x += self.speed
        if difference_y > 0:
            if abs(difference_y) <= self.speed:
                self.y -= difference_y
            else:
                self.y -= self.speed
        elif difference_y < 0:
            if abs(difference_y) <= self.speed:
                self.y -= difference_y
            else:
                self.y += self.speed
        return True

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = node_color  # Initial color of the node
        self.adjacency = []
        self.g = 0
        self.h = 0
        self.parent = None

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __gt__(self, other):
        self_f = self.g + self.h
        other_f = other.g + other.h
        return self_f > other_f

    def __lt__(self, other):
        self_f = self.g + self.h
        other_f = other.g + other.h
        return self_f < other_f

    def get_loc(self):
        return (self.x, self.y)
    
    def reset(self):
        self.g = 0
        self.h = 0
        self.parent = None

    def detect_agent(self, agent_x, agent_y, obstacles):
        # Calculate the distance between the node and the player
        distance = math.sqrt((self.x - agent_x) ** 2 + (self.y - agent_y) ** 2)
        line_of_sight = (self.x, self.y, agent_x, agent_y)

        # Check if the line of sight intersects the obstacles
        obstructed = False
        for obstacle in obstacles:
            if obstacle.clipline(line_of_sight):
                obstructed = True

        # Change color if within detection range and not obstructed
        if distance <= detection_range and not obstructed:
            self.color = detected_color # FIX1
            return True
        else:
            self.color = node_color
            return False
# Initialize pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
transparent_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Player with Transparent Circle")

# Colors
background_color = (0, 0, 0)  # Black background
player_color = (255, 0, 0)  # Red player
walker_colour = (0, 255, 0)  # Green A.I.
agent_color = (0, 0, 255)  # Blue agent
circle_color = (0, 255, 0, 100)  # Green with transparency (alpha = 100)
block_color = (100, 100, 100)  # Gray block
node_color = (255, 255, 0)  # Yellow nodes
detected_color = (255, 0, 255)  # Magenta for detected nodes

# Player settings
player_size = 50
player_x = 400
player_y = 50
player_speed = 8
player = pygame.Rect(player_x, player_y, player_size, player_size)

# A.I. settings
walker_size = 25
walker_x = screen_width // 2 - player_size // 2
walker_y = screen_height - player_size - 10  # Place the player at the bottom
walker_speed = 4
walker_obj = pygame.Rect(walker_x, walker_y, walker_size, walker_size)
walker = Agent(walker_x, walker_y, walker_speed, walker_size, walker_obj, walker_colour)

# Agent settings
agent_size = 50
agent_x = 0  # Start at the left edge
agent_y = screen_height // 2 - agent_size // 2
agent_speed = 3  # Speed of the agent

# Block settings
# block_width = screen_width / 2
# block_height = 100
# block_x = screen_width / 4
# block_y = agent_y - block_height - 50  # Position the block above the agent



# Detection range
detection_range = 60  # Nodes within this distance will change color

# Create a surface for the transparent circle
circle_surface = pygame.Surface((detection_range * 2, detection_range * 2), pygame.SRCALPHA)
ai_detect = pygame.Surface((detection_range * 2, detection_range * 2), pygame.SRCALPHA)
pygame.draw.circle(circle_surface, circle_color, (detection_range, detection_range), detection_range)
pygame.draw.circle(ai_detect, circle_color, (detection_range, detection_range), detection_range)

def distance(node1, node2):
    dx = node2.x - node1.x
    dy = node2.y - node1.y
    return math.sqrt(dx**2 + dy**2)

def visualizePath(path):
    preNode = None
    for node in path:
        if preNode != None:
            pygame.draw.line(screen, player_color, preNode.get_loc(), node.get_loc(), 2)
        preNode = node


nodes = []
node_radius = 5  # Radius of each node
buffer = 25  # Distance from the object to the nodes
num_nodes_per_side = 6  # Number of nodes on each side

# Define the goal node (if needed)
goal = Node(400, 50)
nodes.append(goal)

# display nodes around obstacles
for obstacle in obstacles:
    # Calculate step sizes for evenly spaced nodes (excluding corners)
    step_x = obstacle.width / (num_nodes_per_side - 1)
    step_y = obstacle.height / (num_nodes_per_side - 1)

    # Define the corners
    corners = [
        (obstacle.x - buffer, obstacle.y - buffer),  # Top-left corner
        (obstacle.x + obstacle.width + buffer, obstacle.y - buffer),  # Top-right corner
        (obstacle.x - buffer, obstacle.y + obstacle.height + buffer),  # Bottom-left corner
        (obstacle.x + obstacle.width + buffer, obstacle.y + obstacle.height + buffer),  # Bottom-right corner
    ]

    # Add corner nodes
    for corner in corners:
        nodes.append(Node(*corner))

    # Top side (between top-left and top-right corners)
    for i in range(1, num_nodes_per_side - 1):
        x = obstacle.x + i * step_x
        y = obstacle.y - buffer
        nodes.append(Node(x, y))

    # Bottom side (between bottom-left and bottom-right corners)
    for i in range(1, num_nodes_per_side - 1):
        x = obstacle.x + i * step_x
        y = obstacle.y + obstacle.height + buffer
        nodes.append(Node(x, y))

    # Left side (between top-left and bottom-left corners)
    for i in range(1, num_nodes_per_side - 1):
        x = obstacle.x - buffer
        y = obstacle.y + i * step_y
        nodes.append(Node(x, y))

    # Right side (between top-right and bottom-right corners)
    for i in range(1, num_nodes_per_side - 1):
        x = obstacle.x + obstacle.width + buffer
        y = obstacle.y + i * step_y
        nodes.append(Node(x, y))

#Set adjacencies
def setAdjacencies(nodes, obstacles):
    for node1 in nodes:
        node1.adjacency = []
        for node2 in nodes:
            obstructed = False
            for obstacle in obstacles:
                if obstacle.clipline(node1.get_loc(), node2.get_loc()):
                    obstructed = True
            if not obstructed:
                # pygame.draw.line(screen, (255,0,0), node1.get_loc(), node2.get_loc(), 1)
                node1.adjacency.append(node2)

# A* Search
def find_path(starting_nodes, goal):
    path_cost = 0
    visited = set()
    frontier = []
    for node in starting_nodes:
        node.g = distance(node, goal) # Set new distance
        heapq.heappush(frontier, node) # Add node

    while frontier:
        cur_node = heapq.heappop(frontier)

        if cur_node == goal:
            return cur_node

        visited.add(cur_node)

        for neighbor in cur_node.adjacency:
            if neighbor not in visited and neighbor not in frontier:
                heuristic = distance(neighbor, goal)
                neighbor.g = cur_node.g + distance(neighbor, cur_node)

                neighbor.parent = cur_node

                heapq.heappush(frontier, neighbor)

    print('No valid path from start to goal')
    return []

def generatePath(node): # Generates path from node found in A*
    path = []
    cur_node = node
    while cur_node is not None:
        path.append(cur_node)
        cur_node = cur_node.parent
    
    for node in nodes:
        node.reset() # Reset nodes for next search
    return path

def totalDistance(nodes):
    total = 0
    for i in range(len(nodes)-1):
        total += distance(nodes[i], nodes[i+1])
    return total

def nodeSubset(subset, fullset):
    counter = 2
    if len(subset) < 2:
        counter = len(subset)+1
    for i in range(1, counter):
        print(subset[-i])
        if subset[-i] not in fullset:
            return False
    return True

path = []
setAdjacencies(nodes, obstacles)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement to test environment
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Move up
        player_y -= player_speed
    if keys[pygame.K_s]:  # Move down
        player_y += player_speed
    if keys[pygame.K_a]:  # Move left
        player_x -= player_speed
    if keys[pygame.K_d]:  # Move right
        player_x += player_speed
    if keys[pygame.K_t]:
        player_x = 400
        player_y = 50
    if keys[pygame.K_g]:
        player_x = 400
        player_y = 450

    # Handling A* in real time
    obstructed = False
    for obstacle in obstacles:
        if obstacle.clipline((walker.x, walker.y, goal.x, goal.y)):
            obstructed = True
    if distance(Node(walker.x, walker.y), goal) < detection_range and not obstructed:
        path = []
        walker.frontier = []
        walker.traverse(goal, detection_range - 20)
        # print("Leashing")
    elif path == [] and walker.frontier != []:
        path = generatePath(find_path(walker.frontier, goal))
    elif path != []:
            # print("Pathing: ", path[-1])
            checkPath = generatePath(find_path(walker.frontier, goal))
            if len(path) == 1 and obstructed:
                    path = checkPath
            elif totalDistance(checkPath) < totalDistance(path) and not nodeSubset(checkPath, path):
                print("Poof")
                print(checkPath[-1])
                print(path[-2])
                path = checkPath 
            elif not walker.traverse(path[-1], 5):
                path.pop()
    else:
        walker.traverse(goal, detection_range - 20)
        # print("Elsing")
    
    # Update the player's rectangle position
    player.update(player_x, player_y, player_size, player_size)
    goal.x = player_x + player_size // 2
    goal.y = player_y + player_size // 2

    # Update A.I. position
    walker.get_obj().update(walker.x, walker.y, walker.size, walker.size)

    # Update agent position
    agent_x += agent_speed
    # Reverse direction if the agent hits the edge of the screen
    if agent_x + agent_size > screen_width or agent_x < 0:
        agent_speed *= -1

    # Check each node for detection
    walker.frontier = []
    for node in nodes:
        if node.detect_agent(walker.x + walker.size // 2, walker.y + walker.size // 2, obstacles) and node is not goal:
            walker.frontier.append(node)

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw the large blocks
    for obstacle in obstacles:
        pygame.draw.rect(screen, block_color, obstacle)

    # Draw the player
    pygame.draw.rect(screen, player_color, player)

    #Draw A.I.
    pygame.draw.rect(screen, walker_colour, walker.get_obj())

    # Draw the moving agent
    # pygame.draw.rect(screen, agent_color, (agent_x, agent_y, agent_size, agent_size))

    # Draw the transparent circle around the player
    ai_position = (walker.x + walker.size // 2 - detection_range, walker.y + walker.size // 2 - detection_range)

    # screen.blit(circle_surface, circle_position)
    screen.blit(ai_detect, ai_position)
    
    # Draw the nodes around the block
    for node in nodes:
        pygame.draw.line(transparent_surface, (0,0,0,0), node.get_loc(), (walker.x + walker.size // 2, walker.y + walker.size // 2), 5)
        pygame.draw.circle(screen, node.color, node.get_loc(), node_radius)
    
    # Test pathfinding
    setAdjacencies(nodes, obstacles)
    if walker.frontier != []:
        visualizePath(generatePath(find_path(walker.frontier, goal)))
    
    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(30)

# Quit pygame
pygame.quit()
sys.exit()
