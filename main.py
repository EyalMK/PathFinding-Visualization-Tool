import pygame.draw
import AStar

# Create PyGame window.
def createWindow():
    Width = 800
    window = pygame.display.set_mode((Width, Width))
    pygame.display.set_caption("A* Path Finding Visualization Tool")

def main():
    createWindow()

if __name__ == '__main__':
    main()