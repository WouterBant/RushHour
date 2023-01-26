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

def collect_car_positions(blockSize):
    car_info = dict()

    for index_row, x in enumerate(np.arange(0, WINDOW_WIDTH, blockSize)):
        for index_col, y in enumerate(np.arange(0, WINDOW_HEIGHT, blockSize)):
            char = current_board[index_col][index_row]

            if char != ".":
                if char not in car_info:
                    orientation = ''
                    size = 1
                    if (index_row + 1 < length):
                        if current_board[index_col][index_row + 1] == char:
                            orientation = 'H'
                            size = 2
                            if (index_row + 2 < length):
                                if current_board[index_col][index_row + 2] == char:
                                    size = 3
                    if (index_col + 1 < length):
                        if current_board[index_col + 1][index_row] == char:
                            orientation = 'V'
                            size = 2
                            if (index_col + 2 < length):
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

def drawGridSprites(current_board):
    blockSize = WINDOW_WIDTH / length
    car_info = collect_car_positions(blockSize)

    for index_row, x in enumerate(np.arange(0, WINDOW_WIDTH, blockSize)):
        for index_col, y in enumerate(np.arange(0, WINDOW_HEIGHT, blockSize)):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(surface=SCREEN, color=(90, 90, 90), rect=rect, width=1)

    for car in car_info.items():
        char = car[0]
        x, y, orientation, size = car[1]

        file_name = sprite_dict.get(char)

        sprite = None
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




# player_car = pygame.image.load(assets + '/rood2.png').convert_alpha()
# SCREEN.blit(player_car, (x, y))


SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rushhour")

running = True
color_dict = dict()
sprite_dict = dict()

# visualization loop
while running:
    # calculate the amount of boards that need to be visualized
    number_loops = int(len(data)/length)

    # for each board visualize the configuration
    for i in range(0, number_loops):
        SCREEN.fill(GREY)
        current_board = data[i*length:i*length+length]
        drawGridSprites(current_board)
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