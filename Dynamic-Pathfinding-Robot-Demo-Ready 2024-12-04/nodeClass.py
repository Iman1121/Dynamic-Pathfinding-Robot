from math import sqrt
from betterClipline import clipline_with_parallels

detection_range = 120  # Nodes within this distance will change color
node_color = (255, 255, 0)  # Yellow nodes
detected_color = (255, 0, 255)  # Magenta for detected nodes

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
        self.parent = None

    def detect_agent(self, agent_x, agent_y, obstacles):
        # Calculate the distance between the node and the player
        distance = sqrt((self.x - agent_x) ** 2 + (self.y - agent_y) ** 2)
        line_of_sight = (self.x, self.y, agent_x, agent_y)
        node = (self.x, self.y)
        agent = (agent_x, agent_y)

        # Check if the line of sight intersects the obstacles
        obstructed = False
        for obstacle in obstacles:
            obstructed1, obstructed2, obstructed3 = clipline_with_parallels(obstacle, node, agent)
            if obstructed1 or obstructed2 or obstructed3:
                obstructed = True
                break
            # if obstacle.clipline(line_of_sight):
                # obstructed = True

        # Change color if within detection range and not obstructed
        if distance <= detection_range and not obstructed:
            self.color = detected_color # FIX1
            return True
        else:
            self.color = node_color
            return False
