import pygame
from nodeClass import Node
from agentClass import NPC

screen_width = 800
screen_height = 600

agent_size = 50
agent_starting_x = 0
agent_starting_y = screen_height // 2 - agent_size // 2

background_color = (0, 0, 0)  # Black background
player_color = (255, 0, 0)  # Red player
walker_colour = (0, 255, 0)  # Green A.I.
agent_color = (0, 0, 255)  # Blue agent
circle_color = (0, 255, 0, 100)  # Green with transparency (alpha = 100)
block_color = (100, 100, 100)  # Gray block

node_radius = 5  # Radius of each node 
buffer = 25  # Distance from the object to the nodes
num_nodes_per_side = 6  # Number of nodes on each side

block_width = screen_width / 2
block_height = 100
block_x = screen_width / 4
block_y = agent_starting_y - block_height - 50  # Position the block above the agent
obstacle = pygame.Rect(block_x, block_y, block_width, block_height)
obstacle2 = pygame.Rect(block_x, block_y + 155, block_width, block_height)
obstacles = [obstacle, obstacle2]

def getEnv(envNum):
    if envNum == 1:
        screen_width = 800
        screen_height = 600
        block_width = screen_width / 2
        block_height = 100
        block_x = screen_width / 4
        block_y = agent_starting_y - block_height - 50  # Position the block above the agent
        obstacle = pygame.Rect(block_x, block_y, block_width, block_height)
        obstacle2 = pygame.Rect(block_x, block_y + 155, block_width, block_height)
        obstacles = [obstacle, obstacle2]

        return screen_height, screen_width, obstacles, []

    if envNum == 2:
        screen_width = 800
        screen_height = 600
        block_width = screen_width / 2
        block_height = 100
        block_x = screen_width / 4
        block_y = agent_starting_y - block_height - 50  # Position the block above the agent
        obstacle = pygame.Rect(block_x, block_y, block_width, block_height)
        obstacle2 = pygame.Rect(block_x, block_y + 155, block_width, block_height)
        obstacles = [obstacle, obstacle2]

        agent_size = 100
        agent_x = 0  # Start at the left edge
        agent_y = 350
        agent_speed = 3  # Speed of the agent
        agent_obj = pygame.Rect(agent_x, agent_y, agent_size, agent_size)
        agent = NPC(agent_x, agent_y, agent_speed, agent_size, agent_obj, agent_color)

        return screen_height, screen_width, obstacles, [agent]

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
