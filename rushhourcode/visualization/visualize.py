# Import and initialize the pygame library
import csv
import pygame

csv_file = None

with open('../../output/boards_output.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)

for row in data:
    length = len(row)

pygame.init()

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

def drawGrid():
    blockSize = int(WINDOW_WIDTH/length) #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

# Set up the drawing window
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Run until the user asks to quit
running = True
while running:
    SCREEN.fill(BLACK)
    drawGrid()

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()