import pygame
from nodeClass import Node
from agentClass import NPC
import random

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

def getEnv(envNum, numobjects = 0):
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

        agent = NPC(0, 350, 3, 100, agent_color) #agentx, agenty, agentspeed, agent size, agent color
        moving_agents = [agent]

        return screen_height, screen_width, obstacles, moving_agents
    
    if envNum == 5:
        # Complex environment with obstacles scattered across a larger area
        screen_width = 1200
        screen_height = 800
        obstacles = [
            pygame.Rect(200, 200, 250, 75),
            pygame.Rect(600, 200, 250, 75),
            pygame.Rect(400, 375, 250, 75),
            pygame.Rect(750, 500, 250, 75),
            pygame.Rect(200, 500, 250, 75),
            pygame.Rect(600, 650, 250, 75)
        ]
        moving_agents = []
        return screen_height, screen_width, obstacles, moving_agents
    if envNum == 6:
        # Complex environment with obstacles scattered across a larger area
        screen_width = 800
        screen_height = 600
        obstacles = [
            pygame.Rect(175, 250, 200, 100),
            pygame.Rect(475, 250, 200, 100),
        ]
        moving_agents = []
        moving_agents.append(NPC(0, 100, 7, 75, agent_color)) #agentx, agenty, agentspeed, agent size, agent color
        moving_agents.append(NPC(0, 350, 7, 75, agent_color))
        return screen_height, screen_width, obstacles, moving_agents
    
    if envNum == 7:
        # Random environment with 5 obstacles maintaining at least 75px space
        screen_width = 800
        screen_height = 600
        min_distance = 75
        block_width = 100
        block_height = 50

        obstacles = []
        for _ in range(numobjects):
            while True:
                x = random.randint(0, screen_width - block_width)
                y = random.randint(0, screen_height - block_height)
                new_obstacle = pygame.Rect(x, y, block_width, block_height)
                valid_position = all(
                    new_obstacle.colliderect(
                        pygame.Rect(
                            obs.x - min_distance, obs.y - min_distance,
                            obs.width + 2 * min_distance, obs.height + 2 * min_distance
                        )
                    ) == False for obs in obstacles
                )
                if valid_position:
                    obstacles.append(new_obstacle)
                    break

        # agent_x = random.randint(0, screen_width - agent_size)
        # agent_y = random.randint(0, screen_height - agent_size)
        # agent_obj = pygame.Rect(agent_x, agent_y, agent_size, agent_size)
        moving_agents = []
        return screen_height, screen_width, obstacles, moving_agents

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
