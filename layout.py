import pygame
from constants import *
from nodeClass import Node

block_width = screen_width / 2
block_height = 100
block_x = screen_width / 4
block_y = agent_starting_y - block_height - 50  # Position the block above the agent
obstacle = pygame.Rect(block_x, block_y, block_width, block_height)
obstacle2 = pygame.Rect(block_x, block_y + 155, block_width, block_height)
obstacles = [obstacle, obstacle2]


def getNodes(obstacles, goal):
    nodes = []
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
        
    return nodes
