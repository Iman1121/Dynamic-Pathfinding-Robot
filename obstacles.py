from constants import *
import pygame

block_width = screen_width / 2
block_height = 50
block_x = screen_width / 4
block_y = agent_starting_y - block_height - 50  # Position the block above the agent
obstacle = pygame.Rect(block_x, block_y, block_width, block_height)
obstacle2 = pygame.Rect(block_x, block_y + 155, block_width, block_height)
obstacle3 = pygame.Rect(block_x, block_y + 255, block_width, block_height)
obstacles = [obstacle, obstacle2, obstacle3]


