# Import and initialize libraries
import csv
import random
import pygame
import numpy as np
import time

csv_file = None

with open('../../output/boards_output.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)

for row in data:
    length = len(row)

pygame.init()

BLACK = (0, 0, 0)
WHITE = (105,105,105)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

def drawGrid(current_board):
    blockSize = WINDOW_WIDTH/length
    colorlist = ['blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'cyan', 'brown', (232, 3, 252), (206, 252, 3), (3, 252, 152)]
    for index_row, x in enumerate(np.arange(0, WINDOW_WIDTH, blockSize)):
        for index_col, y in enumerate(np.arange(0, WINDOW_HEIGHT, blockSize)):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            char = current_board[index_col][index_row]
            if char != ".":
                if char == 'X':
                    color = 'red'
                elif char in color_dict:
                    color = color_dict.get(char)
                else:
                    color = random.choice(colorlist)
                    color_dict.update({char: color})
                    colorlist.remove(color)
                pygame.draw.rect(surface=SCREEN, color=color, rect=rect, width=0)
                continue
            pygame.draw.rect(surface=SCREEN, color=(90, 90, 90), rect=rect, width=1)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

running = True
color_dict = dict()

while running:
    number_loops = int(len(data)/length)

    for i in range(0, number_loops):
        SCREEN.fill(WHITE)
        current_board = data[i*length:i*length+length]
        drawGrid(current_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        pygame.display.flip()
        time.sleep(0.5)

pygame.quit()