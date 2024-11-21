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
node_color = (255, 255, 0)  # Yellow nodes
detected_color = (255, 0, 255)  # Magenta for detected nodes

detection_range = 60  # Nodes within this distance will change color

node_radius = 5  # Radius of each node 
buffer = 25  # Distance from the object to the nodes
num_nodes_per_side = 6  # Number of nodes on each side

# Player settings
player_size = 50
player_x = 400
player_y = 50
player_speed = 8

# A.I. settings
walker_size = 25
walker_x = screen_width // 2 - player_size // 2
walker_y = screen_height - player_size - 10  # Place the player at the bottom
walker_speed = 4
