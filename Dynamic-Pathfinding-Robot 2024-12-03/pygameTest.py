import pygame
import sys
import envLayout
from nodeClass import Node, detection_range
from helpers import *
from agentClass import Agent, NPC

obstacles = envLayout.obstacles

# Initialize pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((screen_width, screen_height))
transparent_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Player with Transparent Circle")

player_size = 25
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
walker = Agent(walker_x, walker_y, walker_speed, walker_size, walker_obj, envLayout.walker_colour)

# Agent settings
agent_size = 100
agent_x = 0  # Start at the left edge
agent_y = 350
agent_speed = 3  # Speed of the agent
agent_obj = pygame.Rect(agent_x, agent_y, agent_size, agent_size)
agent = NPC(agent_x, agent_y, agent_speed, agent_size, agent_obj, envLayout.agent_color)

# Create a surface for the transparent circle
circle_surface = pygame.Surface((detection_range * 2, detection_range * 2), pygame.SRCALPHA)
ai_detect = pygame.Surface((detection_range * 2, detection_range * 2), pygame.SRCALPHA)
pygame.draw.circle(circle_surface, envLayout.circle_color, (detection_range, detection_range), detection_range)
pygame.draw.circle(ai_detect, envLayout.circle_color, (detection_range, detection_range), detection_range)

# Define the goal node (if needed)
goal = Node(400, 50)
nodes = envLayout.getNodes(obstacles, goal)
agent.nodes = envLayout.getNodes([agent.get_obj()], goal)

for node in agent.nodes:
    nodes.append(node)

path = []
obstacles.append(agent.get_obj())
setAdjacencies(nodes, obstacles, screen)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement to test environment
    keys = pygame.key.get_pressed()
    newy = player_y
    newx = player_x
    if keys[pygame.K_w]:  # Move up
        newy -= player_speed
    if keys[pygame.K_s]:  # Move down
        newy += player_speed
    if keys[pygame.K_a]:  # Move left
        newx -= player_speed
    if keys[pygame.K_d]:  # Move right
        newx += player_speed
    if keys[pygame.K_t]:
        newx = 400
        newy = 50
    if keys[pygame.K_g]:
        newx = 400
        newy = 450

    # Handling A* in real time

    point = point_on_line((walker.x + walker.size // 2, walker.y + walker.size // 2), goal.get_loc(), detection_range)
    obstructed = False
    for obstacle in obstacles:
        # center = obstacle.clipline(walker.x + walker.size // 2, walker.y + walker.size // 2, point[0], point[1])
        # corner1 = obstacle.clipline(walker.x, walker.y + walker.size, point2[0], point2[1])
        # corner2 = obstacle.clipline(walker.x + walker.size, walker.y, point3[0], point3[1])
        # corner3 = obstacle.clipline(walker.x + walker.size, walker.y + walker.size, point4[0], point4[1])
        # corner4 = obstacle.clipline(walker.x, walker.y, point5[0], point5[1])
       
        obstructed1, obstructed2, obstruced3 = clipline_with_parallels(obstacle, (walker.x + walker.size // 2, walker.y + walker.size // 2), (point[0], point[1]), walker.size // 2)

        if obstructed1 or obstructed2 or obstruced3:
            obstructed = True
    if obstructed:
        if walker.frontier != []:
            checkPath = generatePath(find_path(walker.frontier, goal), nodes)
            
        if path == [] and walker.frontier != []:
            path = checkPath
        elif len(path) == 1 and walker.frontier != []:
            path = checkPath
        elif totalDistance(checkPath) < totalDistance(path) and (checkPath[1] != path[1]):
            path = checkPath 
        elif not walker.traverse(path[-1], 5):
            path.pop()
            # print("Elsing")

        pygame.draw.line(screen, (255,255,255), (walker.x, walker.y), (path[-1].x, path[-1].y), 25)
    else:
        path = []
        walker.frontier = []
        walker.traverse(goal, detection_range - 20)
        # print("Leashing")
    
    # Update the player's rectangle position
    newPlayer = pygame.Rect(newx, newy, player_size, player_size)
    if not check_collision(newPlayer, obstacles):
        player_y = newy
        player_x = newx
        player.update(player_x, player_y, player_size, player_size)

        


    goal.x = player_x + player_size // 2
    goal.y = player_y + player_size // 2

    agent.Testupdate(screen_width)

    # Update A.I. position
    walker.get_obj().update(walker.x, walker.y, walker.size, walker.size)
    agent.get_obj().update(agent.x, agent.y, agent.size, agent.size)


    # Check each node for detection
    walker.frontier = []
    for node in nodes:
        if node.detect_agent(walker.x + walker.size // 2, walker.y + walker.size // 2, obstacles) and node is not goal:
            walker.frontier.append(node)


    # draw

    # Fill the screen with the background color
    screen.fill(envLayout.background_color)

    # Draw the large blocks
    for obstacle in obstacles:
        pygame.draw.rect(screen, envLayout.block_color, obstacle)

    # Draw the player
    pygame.draw.rect(screen, player_color, player)

    #Draw A.I.
    pygame.draw.rect(screen, envLayout.walker_colour, walker.get_obj())

    # Draw the moving agent
    pygame.draw.rect(screen, envLayout.agent_color, agent.get_obj())

    # Draw the transparent circle around the player
    ai_position = (walker.x + walker.size // 2 - detection_range, walker.y + walker.size // 2 - detection_range)

    # screen.blit(circle_surface, circle_position)
    screen.blit(ai_detect, ai_position)
    
    # Draw the nodes around the block
    for node in nodes:
        # pygame.draw.line(screen, (255,255,255), node.get_loc(), (walker.x + walker.size // 2, walker.y + walker.size // 2), 2)
        pygame.draw.circle(screen, node.color, node.get_loc(), envLayout.node_radius)

    # Test pathfinding
    setAdjacencies(nodes, obstacles, screen)
    if walker.frontier != []:
        visualizePath(generatePath(find_path(walker.frontier, goal), nodes), screen)

    point = point_on_line((walker.x + walker.size // 2, walker.y + walker.size // 2), goal.get_loc(), detection_range)

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(30)

# Quit pygame
pygame.quit()
sys.exit()
