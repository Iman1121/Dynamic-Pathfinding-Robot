import math
import heapq
from envLayout import player_color, screen_height, screen_width
from pygame import draw

def find_path(starting_nodes, goal):
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

def distance(node1, node2):
    dx = node2.x - node1.x
    dy = node2.y - node1.y
    return math.sqrt(dx**2 + dy**2)

def totalDistance(nodes):
    total = 0
    for i in range(len(nodes)-1):
        total += distance(nodes[i], nodes[i+1])
    return total

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

def generatePath(node, nodes): # Generates path from node found in A*
    path = []
    cur_node = node
    while cur_node is not None:
        path.append(cur_node)
        cur_node = cur_node.parent
    
    for node in nodes:
        node.reset() # Reset nodes for next search
    return path

def nodeSubset(subset, fullset):
    counter = 2
    if len(subset) < 2:
        counter = len(subset)+1
    for i in range(1, counter):
        print(subset[-i])
        if subset[-i] not in fullset:
            return False
    return True

def visualizePath(path, screen):
    preNode = None
    for node in path:
        if preNode != None:
            draw.line(screen, player_color, preNode.get_loc(), node.get_loc(), 2)
        preNode = node

def check_collision(rect, obstacles):
    for obstacle in obstacles:
        if rect.colliderect(obstacle):
            return True
    
    if rect.left < 0 or rect.right > screen_width or rect.top < 0 or rect.bottom > screen_height:
        return True

    return False