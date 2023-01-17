# Import and initialize libraries
import csv
import random
import pygame
import numpy as np
import time

# open the output file and store the data in a list
with open('../../output/boards_output.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)
# check the format of the board by getting the length of the first row
length = len(data[0])

# initialize pygame
pygame.init()

# set global variables for screencolor and screensize
GREY = (105,105,105)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400


def drawGrid(current_board):
    """Function to draw a grid on the screen and checks for every point on the board whether this is a car or not. If so,
    the blocks gets a color and if not, it remains grey."""
    blockSize = WINDOW_WIDTH/length
    # list with colors for cars
    colorlist = ['blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'cyan', 'brown', (232, 3, 252), (206, 252, 3), (3, 252, 152), (187, 216, 255)]
    # interate through the grid and data
    for index_row, x in enumerate(np.arange(0, WINDOW_WIDTH, blockSize)):
        for index_col, y in enumerate(np.arange(0, WINDOW_HEIGHT, blockSize)):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            char = current_board[index_col][index_row]
            # check if the point on the board is not empty
            if char != ".":
                # if the point on the board is 'X', this is the red car
                if char == 'X':
                    color = 'red'
                # check if the car is already in dictionary, if so get the color from the dictionary
                elif char in color_dict:
                    color = color_dict.get(char)
                # if the car is not in the dictionary, choose a color from the list (randomly) and remove this color
                else:
                    color = random.choice(colorlist)
                    color_dict.update({char: color})
                    colorlist.remove(color)
                # draw the car
                pygame.draw.rect(surface=SCREEN, color=color, rect=rect, width=0)
                continue
            # draw empty space
            pygame.draw.rect(surface=SCREEN, color=(90, 90, 90), rect=rect, width=1)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

running = True
color_dict = dict()

# visualization loop
while running:
    # calculate the amount of boards that need to be visualized
    number_loops = int(len(data)/length)

    # for each board visualize the configuration
    for i in range(0, number_loops):
        SCREEN.fill(GREY)
        current_board = data[i*length:i*length+length]
        drawGrid(current_board)
        # check if the event=QUIT is given set running to FALSE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # check if running is False, then break from the loop
        if not running:
            break
        # display the grid on the screen and sleep for 0.5 seconds for visual purposes
        pygame.display.flip()
        time.sleep(0.5)

pygame.quit()