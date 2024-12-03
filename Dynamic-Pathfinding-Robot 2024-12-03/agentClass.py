from helpers import distance, check_collision
from nodeClass import Node

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

class NPC(Agent):
    def __init__(self, x, y, speed, size, rect, colour):
        super().__init__(x, y, speed, size, rect, colour)
        self.nodes = []

    def updateNodes(self, difference, direction):
        if direction == 'x':
            for node in self.nodes:
                node.x += difference
        elif direction == 'y':
            for node in self.nodes:
                node.y += difference
        else:
            print("ERROR")
    
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
                updateNodes(-difference_x, 'x')
            else:
                self.x -= self.speed
                updateNodes(-self.speed, 'x')
        elif difference_x < 0:
            if abs(difference_x) <= self.speed:
                self.x -= difference_x
                updateNodes(-difference_x, 'x')
            else:
                self.x += self.speed
                updateNodes(self.speed, 'x')
        if difference_y > 0:
            if abs(difference_y) <= self.speed:
                self.y -= difference_y
                updateNodes(-difference_y, 'y')
            else:
                self.y -= self.speed
                updateNodes(-self.speed, 'y')
        elif difference_y < 0:
            if abs(difference_y) <= self.speed:
                self.y -= difference_y
                updateNodes(-self.difference_y, 'y')
            else:
                self.y += self.speed
                updateNodes(self.speed, 'y')
        return True
    
    def Testupdate(self, screen_width):
        # Update agent position
        self.x += self.speed
        self.updateNodes(self.speed, 'x')
        # Reverse direction if the agent hits the edge of the screen
        if self.x + self.size > screen_width or self.x < 0:
            self.speed *= -1

            