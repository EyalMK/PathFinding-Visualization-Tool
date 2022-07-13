import pygame
import AStar
import sys

class PopUpButton():
    def __init__(self, text, x = 0, y = 0, width = 100, height = 50):
        self.text = text
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.imgNormal = pygame.Surface((width, height))
        self.imgNormal.fill(AStar.White)

        self.img = self.imgNormal
        self.rect = self.img.get_rect()

        font = pygame.font.Font('freesansbold.ttf', 15)
        txtImg = font.render(text, True, AStar.Black)
        txtRec = txtImg.get_rect(center = self.rect.center)

        self.imgNormal.blit(txtImg, txtRec)

        # Can't be used before 'blit'.
        self.rect.topleft = (x, y)
        self.hovered = False

    def update(self, window):
        if self.hovered:
            pygame.draw.rect(window, AStar.Green, pygame.Rect(self.x, self.y, self.width, self.height),  2, 2) # Draw rectangle border.
        else:
            pygame.draw.rect(window, AStar.Black, pygame.Rect(self.x, self.y, self.width, self.height), 2, 2)  # Draw rectangle border.
            self.img = self.imgNormal

    def draw(self, window):
        window.blit(self.img, self.rect)

    def eventHandler(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                return

def createWindow():
    """
        Creates a PyGame 800x800 window, gives it a title and returns the window with the width.
    """
    width = 500
    wind = pygame.display.set_mode((width, width))
    pygame.display.set_caption("A* Path Finding Visualization Tool")
    return wind, width

def drawGrid(window, width, rows):
    """
        Draws grey lines between each row and column that denote a divider.
    """
    recSize = width // rows
    for i in range(rows):
        pygame.draw.line(window, AStar.Grey, (0, i * recSize), (width, i * recSize))
    for j in range(rows):
        pygame.draw.line(window, AStar.Grey, (j * recSize, 0), (j * recSize, width))

def PopUp(text):
    width = 1000
    height = 600
    maxFps = 60

    pygame.init()

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("A* Path Finding Visualization Tool")

    font = pygame.font.Font('freesansbold.ttf', 25)
    txtImg = font.render(text, True, AStar.Black)
    txtRec = txtImg.get_rect()
    txtRec.center = (width // 2, height // 2)

    pygame.display.flip()
    clock = pygame.time.Clock()
    isRunning = True

    bttn = PopUpButton('quit', 800, 500, 100, 40)

    while isRunning:
        pygame.display.update()
        clock.tick(maxFps)

        if isRunning: # If it's still running after escape/mouse was pressed on button.
            window.fill(AStar.White)
            bttn.draw(window)
            window.blit(txtImg, txtRec)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if pygame.mouse.get_pressed()[0]:
                isRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isRunning = False
            pygame.display.update()
            bttn.eventHandler(event)

        bttn.update(window)

    sys.exit() # Stop the program and exit. We've finished the algorithm.