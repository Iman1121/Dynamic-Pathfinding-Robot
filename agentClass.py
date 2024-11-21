from helpers import distance
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
