import pygame.draw
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
        return self.type == Black

    def isStart(self):
        return self.type == Orange

    def isEnd(self):
        return self.type == Turquoise

    def reset(self):
        # Reset path.
        self.type = White

    def createStart(self):
        self.type = Orange

    def createEnd(self):
        self.type = Turquoise

    def createClosed(self):
        self.type = Red

    def createOpen(self):
        self.type = Green

    def createBarrier(self):
        self.type = Black

    def createPath(self):
        self.type = Purple

    def drawN(self, window):
        pygame.draw.rect(window, self.type, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        self.neighbors = []
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isBarrier(): # If the down neighbor isn't a barrier and isn't an edge of the grid
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier(): # If the up neighbor isn't a barrier and isn't an edge of the grid
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isBarrier(): # If the right neighbor isn't a barrier and isn't an edge of the grid
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier(): # If the left neighbor isn't a barrier and isn't an edge of the grid
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        # Less than - compare F scores.
        return False
