import pygame
import math
from queue import PriorityQueue

# Colors
Red = (255, 0, 0) # In the closed set - node that has been looked at.
White = (255, 255, 255) # Node that hasn't been looked at.
Black = (0, 0, 0) # Barrier - not a node to visit.
Purple = (128, 0, 128) # Path
Orange = (255, 165, 0) # Start node
Turquoise = (64, 244, 208) # End node.
Green = (0, 255, 0) # In the open set.
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Grey = (128, 128, 128)

class Node:
    """
    The class's methods involving colors and their purpose are commented above.
    x,y - coordinates/indexing each position/node.
    """
    def __init__(self, row, col, width, totalRows):
        self.width = width
        self.row = row
        self.col = col
        self.totalRows = totalRows
        self.x = row * width
        self.y = col * width
        self.type = White
        self.neighbors = []

    def getPos(self):
        return self.row, self.col

    def isOpen(self):
        return self.type == Green

    def isClosed(self):
        return self.type == Red

    def isBarrier(self):
        return self.color == Black

    def isStart(self):
        return self.color == Orange

    def isEnd(self):
        return self.color == Turquoise

    def reset(self):
        # Reset path.
        self.color = White

    def makeClosed(self):
        self.color = Red

    def makeOpen(self):
        self.color = Green

    def makeBarrier(self):
        self.color = Black

    def makeEnd(self):
        self.color = Turquoise

    def makePath(self):
        self.color = Purple

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        pass

    def __lt__(self, other):
        # Less than - compare F scores.
        return False
