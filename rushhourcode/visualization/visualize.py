import csv
import glob
import random
import pygame
import numpy as np
import time
from typing import Any

class Visualization:
    """This is a class for the visualization of the RushHour problem."""

    def __init__(self) -> None:
        """Initialization with the format of the board."""
        self.data = self.data_loader()
        self.length = len(self.data[0])

        # load sprites into corresponding lists
        self.sprites_two = []
        self.sprites_three = []
        self.sprite_loader()

        # variables for pygame
        pygame.init()
        self.WINDOW_HEIGHT = 400
        self.WINDOW_WIDTH = 400
        self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    def data_loader(self) -> list[list[str]]:
        """This method will load data from an output file as 2D array"""
        # Open the output file and store the data in a list
        with open('output/boards_output.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            data = list(csv_reader)
        return data

    def sprite_loader(self) -> None:
        """This method will load the correct sprites in the correct lists from the class object"""
        # Append the corresponding car to the corresponding list
        for file in glob.glob("visualization_assets/*2.png"):
            self.sprites_two.append(file)

        for file in glob.glob("visualization_assets/*3.png"):
            self.sprites_three.append(file)

    def collect_car_positions(self, blockSize: int, current_board: list[list[str]], sprite_dict: dict[str, Any]) -> dict[str, tuple[int, int, str, int]]:
        """
        This method will collect all the information on the cars in regard to their positions and updates these car in the
        sprite dictionary. It takes an integer value as 'blockSize', representing the size of one block in the grid.
        And, it will return an integer value which represents a dictionary where a car-orientation (value) belongs to a car (key).
        """
        # Create dictionary for the car information
        car_info = dict()

        # Loop through the board and check for every car its size and orientation
        for index_row, x in enumerate(np.arange(0, self.WINDOW_WIDTH, blockSize)):
            for index_col, y in enumerate(np.arange(0, self.WINDOW_HEIGHT, blockSize)):
                char = current_board[index_col][index_row]
                # Check if current position on the board is not empty ('.')
                if char != ".":
                    if char not in car_info:
                        orientation = ''
                        size = 1
                        if index_row + 1 < self.length:
                            if current_board[index_col][index_row + 1] == char:
                                orientation = 'H'
                                size = 2
                                if index_row + 2 < self.length:
                                    if current_board[index_col][index_row + 2] == char:
                                        size = 3
                        if index_col + 1 < self.length:
                            if current_board[index_col + 1][index_row] == char:
                                orientation = 'V'
                                size = 2
                                if index_col + 2 < self.length:
                                    if current_board[index_col + 2][index_row] == char:
                                        size = 3
                        # If car not in sprite dictionary assign a sprite from correct sprite list and update
                        if char not in sprite_dict:
                            file = None
                            if size == 2:
                                file = random.choice(self.sprites_two)
                            if size == 3:
                                file = random.choice(self.sprites_three)
                            sprite_dict.update({char: file})
                        car_info.update({char: (x, y, orientation, size)})

        return car_info

    def drawGridSprites(self, current_board: list[list[str]], sprite_dict: dict[str, Any]) -> None:
        """This method will draw all the cars on the grid using sprites. It will directly draw a car on the grid using its
        coordinates, orientation and size (this is scaled)."""

        # Get size of block in grid and information of each car
        blockSize = self.WINDOW_WIDTH / self.length
        car_info = self.collect_car_positions(blockSize, current_board, sprite_dict)

        # Draw grid using the board information
        for index_row, x in enumerate(np.arange(0, self.WINDOW_WIDTH, blockSize)):
            for index_col, y in enumerate(np.arange(0, self.WINDOW_HEIGHT, blockSize)):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(surface=self.SCREEN, color=(90, 90, 90), rect=rect, width=1)

        # Draw each car on the screen
        for car in car_info.items():
            char = car[0]
            x, y, orientation, size = car[1]

            file_name = sprite_dict.get(char)

            # If the character is 'X' it means we have found the red car, so we give it its corresponding sprite
            if char == 'X':
                sprite = pygame.image.load('visualization_assets/rood.png').convert_alpha()
            # Else we give it the sprite of the given information
            else:
                sprite = pygame.image.load(file_name).convert_alpha()

            # Draw the cars using their orientation and scale these to the blocksize and its own length
            if orientation == 'H':
                sprite = pygame.transform.rotate(sprite, 270)
                sprite = pygame.transform.scale(sprite, (blockSize * size, blockSize * 2))
                rect = sprite.get_rect(topleft=(x, y - blockSize * 0.5))
            if orientation == 'V':
                sprite = pygame.transform.scale(sprite, (blockSize * 2, blockSize * size))
                rect = sprite.get_rect(topleft=(x - blockSize * 0.5, y))
            # Print sprite on screen
            self.SCREEN.blit(sprite, rect)

    def run_visualization(self) -> None:
        """This method will run the visualization"""
        # set caption
        pygame.display.set_caption("Rushhour")

        # Create variables that are used for the visualization
        running = True
        GREY = (105, 105, 105)
        sprite_dict = dict()

        # Visualization loop
        while running:
            # Calculate the amount of boards that need to be visualized
            number_loops = int(len(self.data) / self.length)

            # For each board visualize the configuration
            for i in range(0, number_loops):
                self.SCREEN.fill(GREY)
                current_board = self.data[i * self.length:i * self.length + self.length]
                self.drawGridSprites(current_board, sprite_dict)
                # Check if the event=QUIT is given set running to FALSE
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                # Check if running is False, then break from the loop
                if not running:
                    break
                # Display the grid on the screen and sleep for 0.5 seconds for visual purposes
                pygame.display.flip()
                time.sleep(0.5)

        pygame.quit()
