import math
import heapq
# from envLayout import player_color, screen_height, screen_width
from pygame import draw

player_color = (255, 0, 0)  # Red player

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
def setAdjacencies(nodes, obstacles, screen):
    for node1 in nodes:
        node1.adjacency = []
        for node2 in nodes:
            obstructed = False
            for obstacle in obstacles:
                obstructed1, obstructed2, obstructed3 = clipline_with_parallels(obstacle, node1.get_loc(), node2.get_loc())
                # if obstacle.clipline(node1.get_loc(), node2.get_loc()):
                if obstructed1 or obstructed2 or obstructed3:
                    obstructed = True
            if not obstructed:
                # draw.line(screen, (255,0,0), node1.get_loc(), node2.get_loc(), 1)
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
        if subset[-i] not in fullset:
            print(subset[-i])
            return False
    return True

def visualizePath(path, screen):
    preNode = None
    for node in path:
        if preNode != None:
            draw.line(screen, player_color, preNode.get_loc(), node.get_loc(), 2)
        preNode = node

def check_collision(rect, obstacles, screen_height, screen_width):
    for obstacle in obstacles:
        if rect.colliderect(obstacle):
            return True
    
    if rect.left < 0 or rect.right > screen_width or rect.top < 0 or rect.bottom > screen_height:
        return True

    return False

def point_on_line(agent_loc, goal_loc, distance):
    x1, y1 = agent_loc
    x2, y2 = goal_loc
    
    # Calculate the direction vector from p1 to p2
    dx = x2 - x1
    dy = y2 - y1
    
    # Compute the magnitude of the direction vector
    magnitude = math.sqrt(dx**2 + dy**2)
    
    # Normalize the direction vector
    unit_dx = dx / magnitude
    unit_dy = dy / magnitude
    
    # Scale the unit vector by the desired distance and add to p1
    new_x = x1 + distance * unit_dx
    new_y = y1 + distance * unit_dy
    
    return new_x, new_y

def clipline_with_parallels(rect, p1, p2, distance=12):
    """
    Clips a line and two parallel lines to a pygame.Rect.
    
    Args:
        rect (pygame.Rect): The rectangle to clip against.
        p1 (tuple): Starting point of the main line (x1, y1).
        p2 (tuple): Ending point of the main line (x2, y2).
        distance (int): The distance of the parallel lines from the main line.
    """
    def parallel_points(p1, p2, distance):
        """Calculate parallel line points at a given distance."""
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length == 0:
            return (p1, p1), (p2, p2)  # Avoid division by zero
        
        # Unit vector perpendicular to the line
        perp_dx, perp_dy = -dy / length, dx / length
        
        # Points for the two parallel lines
        offset1 = (perp_dx * distance, perp_dy * distance)
        offset2 = (-perp_dx * distance, -perp_dy * distance)
        
        p1_offset1 = (p1[0] + offset1[0], p1[1] + offset1[1])
        p2_offset1 = (p2[0] + offset1[0], p2[1] + offset1[1])
        
        p1_offset2 = (p1[0] + offset2[0], p1[1] + offset2[1])
        p2_offset2 = (p2[0] + offset2[0], p2[1] + offset2[1])
        
        return (p1_offset1, p2_offset1), (p1_offset2, p2_offset2)
    
    # Calculate parallel lines
    parallel1, parallel2 = parallel_points(p1, p2, distance)
    
    # Clip the lines
    main_clip = rect.clipline(p1, p2)
    parallel1_clip = rect.clipline(parallel1[0], parallel1[1])
    parallel2_clip = rect.clipline(parallel2[0], parallel2[1])
    
    # Return results
    return main_clip, parallel1_clip, parallel2_clip