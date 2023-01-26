# Import and initialize libraries
import csv
import random
import pygame
import numpy as np
import time
import glob

# open the output file and store the data in a list
with open('output/boards_output.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)

sprites_two = []
sprites_three = []

for file in glob.glob("rushhourcode/visualization/assets/*2.png"):
    sprites_two.append(file)

for file in glob.glob("rushhourcode/visualization/assets/*3.png"):
    sprites_three.append(file)

# check the format of the board by getting the length of the first row
length = len(data[0])

# initialize pygame
pygame.init()

# set global variables for screencolor and screensize
GREY = (105,105,105)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

assets = "assets"

class Visualization:
    """This is a class for the visualization of the RushHour problem"""

    def __init__(self):
        self.length_board = length

    def collect_car_positions(self, blockSize):
        car_info = dict()

        for index_row, x in enumerate(np.arange(0, WINDOW_WIDTH, blockSize)):
            for index_col, y in enumerate(np.arange(0, WINDOW_HEIGHT, blockSize)):
                char = current_board[index_col][index_row]

                if char != ".":
                    if char not in car_info:
                        orientation = ''
                        size = 1
                        if (index_row + 1 < self.length_board):
                            if current_board[index_col][index_row + 1] == char:
                                orientation = 'H'
                                size = 2
                                if (index_row + 2 < self.length_board):
                                    if current_board[index_col][index_row + 2] == char:
                                        size = 3
                        if (index_col + 1 < self.length_board):
                            if current_board[index_col + 1][index_row] == char:
                                orientation = 'V'
                                size = 2
                                if (index_col + 2 < self.length_board):
                                    if current_board[index_col + 2][index_row] == char:
                                        size = 3

                        if char not in sprite_dict:
                            file = None
                            if size == 2:
                                file = random.choice(sprites_two)
                            if size == 3:
                                file = random.choice(sprites_three)
                            sprite_dict.update({char: file})
                        car_info.update({char: (x, y, orientation, size)})

        return car_info

    def drawGridSprites(self, current_board):

        blockSize = WINDOW_WIDTH / self.length_board
        car_info = self.collect_car_positions(blockSize)

        for index_row, x in enumerate(np.arange(0, WINDOW_WIDTH, blockSize)):
            for index_col, y in enumerate(np.arange(0, WINDOW_HEIGHT, blockSize)):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(surface=SCREEN, color=(90, 90, 90), rect=rect, width=1)

        for car in car_info.items():
            char = car[0]
            x, y, orientation, size = car[1]

            file_name = sprite_dict.get(char)

            if char == "X":
                sprite = pygame.image.load('rushhourcode/visualization/assets/rood.png').convert_alpha()
            else:
                sprite = pygame.image.load(file_name).convert_alpha()

            if orientation == "H":
                sprite = pygame.transform.rotate(sprite, 270)
                sprite = pygame.transform.scale(sprite, (blockSize * size, blockSize*2))
                rect = sprite.get_rect(topleft=(x, y - blockSize * 0.5))
            if orientation == 'V':
                sprite = pygame.transform.scale(sprite, (blockSize*2, blockSize*size))
                rect = sprite.get_rect(topleft=(x - blockSize * 0.5, y))
            SCREEN.blit(sprite, rect)


SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rushhour")

running = True
color_dict = dict()
sprite_dict = dict()
visualization = Visualization()

# visualization loop
while running:
    # calculate the amount of boards that need to be visualized
    number_loops = int(len(data)/length)

    # for each board visualize the configuration
    for i in range(0, number_loops):
        SCREEN.fill(GREY)
        current_board = data[i*length:i*length+length]
        visualization.drawGridSprites(current_board)
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