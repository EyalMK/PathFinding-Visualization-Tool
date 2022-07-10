import pygame
import AStar
from queue import PriorityQueue

def createWindow():
    """
        Creates a PyGame 800x800 window, gives it a title and returns the window with the width.
    """
    width = 800
    wind = pygame.display.set_mode((width, width))
    pygame.display.set_caption("A* Path Finding Visualization Tool")
    return wind, width

def H(p1, p2):
    """
        Calculates the Manhattan distance. P1,P2 are points - (rowNumber,colNumber).
        Returns the distance of the edge between the two points.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def createGrid(width, rows):
    """
        Creates a matrix of nodes. In every row, there are width // rows (gap) nodes.
        Returns the grid.
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = AStar.Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def drawGrid(window, width, rows):
    """
        Draws grey lines between each row and column that denote a divider.
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, AStar.Grey, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(window, AStar.Grey, (j * gap, 0), (j * gap, width))

def draw(window, grid, width, rows):
    """
        Draws every node in the grid (window) white. The default color.
    """
    window.fill(AStar.White)
    for row in grid:
        for node in row:
            node.drawNode(window)

    drawGrid(window, width, rows) # Draw dividers.
    pygame.display.update()

def getPressedPos(pos, width, rows):
    """
        Gets the size of each node (rectangle), pos = (x,y) where mouse was pressed.
        Returns the row and column where the mouse was pressed.
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def getNodePos(grid, width, rows):
    """
        Gets the x,y position where mouse was pressed, getPressedPos returns the row, column where x,y is.
        Returns the node at row,col (where mouse was pressed).
    """
    pos = pygame.mouse.get_pos()
    row, col = getPressedPos(pos, width, rows)
    node = grid[row][col]

    return node

def reconstructPath(prevNode, current, draw):
    """
        Recreates the path by FScore in the open set. Draws every node's original source node (previous node)
        starting from the end node.
    """
    while current in prevNode:
        current = prevNode[current]
        current.createPath()
        draw()

def algorithm(draw, grid, startNode, endNode):
    """
        The A* algorithm. Explained in README.md.
    """
    cnt = 0 # Tie breaker if F scores are equal.
    openSet = PriorityQueue() # sorts by minimal FScore.
    openSet.put((0, cnt, startNode)) # (FScore, count, Node)
    prevNode = {} # Nodes that denote every node's original source node in the open set.
    gScore = {node: float("infinity") for row in grid for node in row}
    gScore[startNode] = 0
    fScore = {node: float("infinity") for row in grid for node in row}
    fScore[startNode] = H(startNode.getPos(), endNode.getPos())

    openSetHash = {startNode} # Keep track of the items in PriorityQueue

    while not openSet.empty(): # Empty denotes that we've considered every node and no optimal path has been found
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = openSet.get()[2] # 2 is the Node in each set in the open set.
        openSetHash.remove(current)


        if current == endNode: # if current node is the end node, reconstruct the optimal path and finish.
            reconstructPath(prevNode, endNode, draw)
            endNode.createEnd()
            startNode.createStart()
            return True

        for neighbor in current.neighbors: # Check every neighbor in the neighbor list for this node object.
            tmpGScore = gScore[current] + 1
            if tmpGScore < gScore[neighbor]: # If this GScore is more optimal than the neighbor's.
                prevNode[neighbor] = current # neighbor originated from current node. - Next node is neighbor.
                gScore[neighbor] = tmpGScore
                fScore[neighbor] = tmpGScore + H(neighbor.getPos(), endNode.getPos()) # Calculate Manhattan distance and FScore.
                if neighbor not in openSetHash: # If this node hasn't already been checked while checking another node's neighbors.
                    cnt += 1
                    openSet.put((fScore[neighbor], cnt, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.createOpen()
        draw()

        if current != startNode: # if current node is not the start node and we've already considered it, close it by drawing it as red.
            current.createClosed()

    return False # didn't find a path.

def eventController(window, grid, width, rows):
    startNode = None
    endNode = None
    run = True
    startedAlgorithm = False

    while run:
        draw(window, grid, width, rows) # Draw default grid and nodes.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if startedAlgorithm: # If the algorithm started, it cannot be interrupted.
                continue

            if pygame.mouse.get_pressed()[0]:  # Left msb
                node = getNodePos(grid, width, rows)
                if not startNode and node != endNode:
                    startNode = node
                    startNode.createStart()
                elif not endNode and node != startNode:
                    endNode = node
                    endNode.createEnd()

                elif node != endNode and node != startNode:
                    node.createBarrier()

            elif pygame.mouse.get_pressed()[2]:  # Right msb
                node = getNodePos(grid, width, rows)
                node.reset()

                if node == startNode:
                    startNode = None
                elif node == endNode:
                    endNode = None

            if event.type == pygame.KEYDOWN:  # Start algorithm
                startedAlgorithm = True
                if event.key == pygame.K_SPACE and startedAlgorithm and startNode and endNode:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)
                    algorithm(lambda: draw(window, grid, width, rows), grid, startNode, endNode)
                    startedAlgorithm = False

                if event.key == pygame.K_c:  # Reset window.
                    startedAlgorithm = False
                    startNode = None
                    endNode = None
                    grid = createGrid(width, rows)

    pygame.quit()

def main():
    rows = 50

    window, width = createWindow()
    grid = createGrid(width, rows)
    eventController(window, grid, width, rows)

if __name__ == '__main__':
    main()