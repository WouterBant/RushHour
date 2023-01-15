# Import and initialize libraries
import csv
import pygame
import numpy as np

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

def drawGrid(current_board):
    blockSize = WINDOW_WIDTH/length
    color_dict = dict()
    for index_row, x in enumerate(np.arange(0, WINDOW_WIDTH, blockSize)):
        for index_col, y in enumerate(np.arange(0, WINDOW_HEIGHT, blockSize)):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

running = True
while running:
    SCREEN.fill(BLACK)

    number_loops = int(len(data)/length)

    for i in range(0, number_loops):
        current_board = data[i*length:i*length+length]
        drawGrid(current_board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()