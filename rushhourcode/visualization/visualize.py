import csv, random, pygame, time, glob
import numpy as np

# Open the output file and store the data in a list
with open('output/boards_output.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)

# Create two lists, one for the cars with length=2 and another for length=3
sprites_two = []
sprites_three = []

# Append the corresponding car to the corresponding list
for file in glob.glob("rushhourcode/visualization/assets/*2.png"):
    sprites_two.append(file)

for file in glob.glob("rushhourcode/visualization/assets/*3.png"):
    sprites_three.append(file)

# Check the format of the board by getting the length of the first row
length = len(data[0])

# Initialize pygame
pygame.init()

# Set global variables for screen color and screensize
GREY = (105, 105, 105)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400


class Visualization:
    """This is a class for the visualization of the RushHour problem."""

    def __init__(self):
        """Initialization with the format of the board."""
        self.length_board = length

    def collect_car_positions(self, blockSize):
        """
        This method will collect all the information on the cars with regards to their positions and updates these car in the
        sprite dictionary. It takes an integer value as 'blockSize', representing the size of one block in the grid.
        And, it will return an integer value which represents a dictionary where a car-orientation (value) belongs to a car (key).
        """
        # Create dictionary for the car information
        car_info = dict()

        # Loop through the board and check for every car its size and orientation
        for index_row, x in enumerate(np.arange(0, WINDOW_WIDTH, blockSize)):
            for index_col, y in enumerate(np.arange(0, WINDOW_HEIGHT, blockSize)):
                char = current_board[index_col][index_row]
                # Check if current position on the board is not empty ('.')
                if char != ".":
                    if char not in car_info:
                        orientation = ''
                        size = 1
                        if index_row + 1 < self.length_board:
                            if current_board[index_col][index_row + 1] == char:
                                orientation = 'H'
                                size = 2
                                if index_row + 2 < self.length_board:
                                    if current_board[index_col][index_row + 2] == char:
                                        size = 3
                        if index_col + 1 < self.length_board:
                            if current_board[index_col + 1][index_row] == char:
                                orientation = 'V'
                                size = 2
                                if index_col + 2 < self.length_board:
                                    if current_board[index_col + 2][index_row] == char:
                                        size = 3
                        # If car not in sprite dictionary assign a sprite from correct sprite list and update
                        if char not in sprite_dict:
                            file = None
                            if size == 2:
                                file = random.choice(sprites_two)
                            if size == 3:
                                file = random.choice(sprites_three)
                            sprite_dict.update({char: file})
                        car_info.update({char: (x, y, orientation, size)})

        return car_info

    def drawGridSprites(self):
        """This method will draw all the cars on the grid using sprites. It will directly draw a car on the grid using its
        coordinates, orientation and size (this is scaled)."""

        # Get size of block in grid and information of each car
        blockSize = WINDOW_WIDTH / self.length_board
        car_info = self.collect_car_positions(blockSize)

        # Draw grid using the board information
        for index_row, x in enumerate(np.arange(0, WINDOW_WIDTH, blockSize)):
            for index_col, y in enumerate(np.arange(0, WINDOW_HEIGHT, blockSize)):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(surface=SCREEN, color=(90, 90, 90), rect=rect, width=1)

        # Draw each car on the screen
        for car in car_info.items():
            char = car[0]
            x, y, orientation, size = car[1]

            file_name = sprite_dict.get(char)

            # If the character is 'X' it means we have found the red car, so we give it its corresponding sprite
            if char == "X":
                sprite = pygame.image.load('rushhourcode/visualization/assets/rood.png').convert_alpha()
            # Else we give it the sprite of the given information
            else:
                sprite = pygame.image.load(file_name).convert_alpha()

            # Draw the cars using their orientation and scale these to the blocksize and its own length
            if orientation == "H":
                sprite = pygame.transform.rotate(sprite, 270)
                sprite = pygame.transform.scale(sprite, (blockSize * size, blockSize * 2))
                rect = sprite.get_rect(topleft=(x, y - blockSize * 0.5))
            if orientation == 'V':
                sprite = pygame.transform.scale(sprite, (blockSize * 2, blockSize * size))
                rect = sprite.get_rect(topleft=(x - blockSize * 0.5, y))
            # Print sprite on screen
            SCREEN.blit(sprite, rect)


# Draw pygame screen and set caption
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rushhour")

# Create variables that are used for the visualization
running = True
color_dict = dict()
sprite_dict = dict()
visualization = Visualization()

# Visualization loop
while running:
    # Calculate the amount of boards that need to be visualized
    number_loops = int(len(data) / length)

    # For each board visualize the configuration
    for i in range(0, number_loops):
        SCREEN.fill(GREY)
        current_board = data[i * length:i * length + length]
        visualization.drawGridSprites()
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
