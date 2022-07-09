import pygame
import AStar
from queue import PriorityQueue

# Create PyGame window.
def createWindow():
    width = 800
    wind = pygame.display.set_mode((width, width))
    pygame.display.set_caption("A* Path Finding Visualization Tool")
    return wind, width

def H(p1, p2):
    # Manhattan distance.
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def createGrid(width, rows):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = AStar.Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def drawGrid(window, width, rows):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, AStar.Grey, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(window, AStar.Grey, (j * gap, 0), (j * gap, width))

def draw(window, grid, width, rows):
    window.fill(AStar.White) # Not efficient, need to look for a substitute. Although, it's common practice in PyGame.
    for row in grid:
        for node in row:
            node.drawN(window)

    drawGrid(window, width, rows)
    pygame.display.update()

def getPressedPos(pos, width, rows):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def getNodePos(grid, width, rows):
    pos = pygame.mouse.get_pos()
    row, col = getPressedPos(pos, width, rows)
    node = grid[row][col]

    return node

def reconstructPath(prevNode, current, draw):
    while current in prevNode:
        current = prevNode[current]
        current.createPath()
        draw()

def algorithm(draw, grid, startNode, endNode):
    cnt = 0 # Tie breaker if F scores are equal.
    openSet = PriorityQueue() # sorts by minimal fscore.
    openSet.put((0, cnt, startNode)) # (FScore, count, Node)
    prevNode = {}
    gScore = {node: float("infinity") for row in grid for node in row}
    gScore[startNode] = 0
    fScore = {node: float("infinity") for row in grid for node in row}
    fScore[startNode] = H(startNode.getPos(), endNode.getPos())

    openSetHash = {startNode} # Keep track of the items in priorityqueue

    while not openSet.empty(): # Empty denotes that we've considered every node and no optimal path has been found
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = openSet.get()[2] # 2 is the Node.
        openSetHash.remove(current)


        if current == endNode:
            reconstructPath(prevNode, endNode, draw)
            endNode.createEnd()
            startNode.createStart()
            return True

        for neighbor in current.neighbors:
            tmpGScore = gScore[current] + 1
            if tmpGScore < gScore[neighbor]:
                prevNode[neighbor] = current
                gScore[neighbor] = tmpGScore
                fScore[neighbor] = tmpGScore + H(neighbor.getPos(), endNode.getPos())
                if neighbor not in openSetHash:
                    cnt += 1
                    openSet.put((fScore[neighbor], cnt, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.createOpen()
        draw()

        if current != startNode: # if current node is not the start node and we've already considered it, close it by drawing it as red.
            current.createClosed()

    return False # didn't find a path.

def main(window, width):
    rows = 50
    grid = createGrid(width, rows)

    startNode = None
    endNode = None
    run = True
    startedAlgorithm = False

    while run:
        draw(window, grid, width, rows)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if startedAlgorithm:
                continue

            if pygame.mouse.get_pressed()[0]: # Left msb
                node = getNodePos(grid, width, rows)
                if not startNode and node != endNode:
                    startNode = node
                    startNode.createStart()
                elif not endNode and node != startNode:
                    endNode = node
                    endNode.createEnd()

                elif node != endNode and node != startNode:
                    node.createBarrier()

            elif pygame.mouse.get_pressed()[2]: # Right msb
                node = getNodePos(grid, width, rows)
                node.reset()

                if node == startNode:
                    startNode = None
                elif node == endNode:
                    endNode = None

            if event.type == pygame.KEYDOWN: # Start algorithm
                if event.key == pygame.K_SPACE and not startedAlgorithm and startNode and endNode:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)
                    algorithm(lambda: draw(window, grid, width, rows), grid, startNode, endNode)

                if event.key == pygame.K_c: # Clear
                    startNode = None
                    endNode = None
                    grid = createGrid(width, rows)

    pygame.quit()

if __name__ == '__main__':
    window, Width = createWindow()
    main(window, Width)