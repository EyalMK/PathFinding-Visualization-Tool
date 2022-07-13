import pygame
import sys

# Colors
White = (255, 255, 255) # Default grid color.
Black = (0, 0, 0) # Barrier - a blocked node that can't be looked at.
Brown = (139, 35, 35) # Path.
Gold = (255, 215, 0) # Start node.
Blue = (0, 0, 139) # End node
Green = (0, 128, 0) # Denotes that a node is in the open set. Serves to draw the edge of a mini-grid containing the best path.
Red = (255, 0, 0) # Closed set nodes. Nodes that have been considered and passed on.
Grey = (128, 128, 105) # Default divider between each node.

class Node:
    def __init__(self, row, col, width, totalRows):
        self.width = width
        self.row = row
        self.col = col
        self.totalRows = totalRows
        self.x = row * width
        self.y = col * width
        self.type = White
        self.neighbors = []
        self.image = None
        self.rec = None

    def getPos(self):
        return self.row, self.col

    def isBarrier(self):
        return self.type == Black

    def reset(self):
        # Reset path.
        self.type = White

    def createStart(self):
        self.type = Gold

    def createEnd(self):
        self.type = Blue

    def createClosed(self):
        self.type = Red

    def createOpen(self):
        self.type = Green

    def createBarrier(self):
        self.type = Black

    def createPath(self, window):
        self.image = pygame.image.load("Assets/mario.png").convert() # Convert makes the blit faster.
        self.image = pygame.transform.scale(self.image, (self.width, self.width))
        self.rec = self.image.get_rect()
        self.rec.topleft = (self.x, self.y)

    def drawNode(self, window):
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