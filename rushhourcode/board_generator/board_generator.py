import random
from typing import Set, List, Any, Optional
from string import ascii_uppercase
import itertools
from typing import List, Set
from ..classes.board import Board
from ..classes.car import Car
import sys

# a 6x6 board comes with 12 cars and 4 trucks, so I think
# it's fair to assume the ratio is 3:1 for any board

# the exit row on each board is either in the middle (odd size boards)
# or on the rows/2'th row (so row 3 for 6x6, or row 6 for 12x12)
class Generator:

    def __init__(self) -> None:
        self.size, tries, shuffles = self.get_size_tries_shuffles()
        self.area = self.size ** 2
        self.cars = set()
        self.board = Board(self.cars, self.size)
        self.generate_board(tries)
        self.shuffle_board(shuffles)
        self.hill_climb()

    def get_size_tries_shuffles(self) -> tuple[int, int,int]:
        """
        Get the size of the board, the number of times a vehicle is attempted to be placed on the board and how
        much the board should be shuffled.
        """
        try:
            size = int(input("(1/3) How big should the board be? Choose 6, 9 or 12: "))
            tries = int(input("(2/3) How often should a vehicle be tried to place? Choose a positive integer: "))
            shuffles = int(input("(3/3) How often should the board be shuffeled? Choose a positive integer: "))
            if size <= 0 or tries <= 0 or (size != 6 and size != 9 and size != 12):
                print("\nAll values should be positive integers.")
                sys.exit(5)
        except ValueError:
            print("\nAll values should be positive integers.")
            sys.exit(6)
        return (size, tries, shuffles)

    # generate an empty board and add cars
    def generate_board(self, tries: int) -> None:
        exit_row = (self.size + 1) // 2 - 1
        self.add_car(self.generate_exit_car(exit_row, 0))

        # add cars with unique ID's, only if their position is valid
        gen = self.iter_all_strings()
        for _ in range(tries):
            car = self.generate_car("temporary id")
            if self.is_valid(car, exit_row):
                car.name = self.label_gen(gen)
                self.add_car(car)
    
    # make a certain amount of random moves to shuffle the board
    def shuffle_board(self, shuffles) -> None:
        for _ in range(shuffles):
            self.board = self.board.randomMove()


    # ID generator from:
    # https://stackoverflow.com/questions/29351492/how-to-make-a-continuous-alphabetic-list-python-from-a-z-then-from-aa-ab-ac-e
    def iter_all_strings(self) -> str:
        size = 1
        while True:
            for s in itertools.product(ascii_uppercase, repeat=size):
                yield "".join(s)
            size += 1

    # this part also from:
    # https://stackoverflow.com/questions/29351492/how-to-make-a-continuous-alphabetic-list-python-from-a-z-then-from-aa-ab-ac-e
    def label_gen(self, gen) -> str:
        for s in gen:
            return s

    # add a new car to the board
    def add_car(self, car: Car):
        if car.orientation == "H":
            for c in range(car.col, car.col + car.length):
                self.board.board[car.row][c] = car.name
        elif car.orientation == "V":
            for r in range(car.row, car.row + car.length):
                self.board.board[r][car.col] = car.name
        self.board.cars.add(car)

    # generate the exit car on the correct row
    def generate_exit_car(self, row: int, col: int) -> Car:
        orientation: str = "H"
        name: str = "X"
        length: int = 2
        exit_car = Car(name, orientation, col, row, length)
        return exit_car

    # generate a random car or truck
    def generate_car(self, car_id: str) -> Car:
        lengths = [2, 3]
        orientations = ["H", "V"]
        length = random.choices(lengths, weights=[3, 1])[0] # ratio trucks/cars = 1 to 3
        orientation = random.choice(orientations)
        if orientation == "H":
            col = random.randint(0, self.size - length)
            row = random.randint(0, self.size - 1)
        else:
            row = random.randint(0, self.size - length)
            col = random.randint(0, self.size - 1)
        car = Car(car_id, orientation, col, row, length)
        return car

    # check if the new car has a valid position, e.g. doesn't overlap the board borders
    # and doesn't block the exit car
    def is_valid(self, car: Car, exit_row: int):
        if car.name == "X":
            return False
        if car.orientation == "H":
            for c in range(car.col, car.col + car.length):
                if c == self.size:
                    return False
                else:
                    if self.board.board[car.row][c] != "." or car.row == exit_row:
                        return False
        elif car.orientation == "V":
            for r in range(car.row, car.row + car.length):
                if r == self.size:
                    return False
                else:
                    if self.board.board[r][car.col] != "." or r == exit_row:
                        return False
        return True
    
    # hill climb algorithm to put the board in a more complex state
    def hill_climb(self) -> None:
        sameValue = currentValue = 0
        while sameValue < 10:
            moves: list[Board] = [move for move in self.board.moves()]
            hardestBoard = max(moves, key=lambda x: x.number_of_blocking_and_blocking_blocking_cars())
            valueHardestBoard = hardestBoard.number_of_blocking_and_blocking_blocking_cars()
            if valueHardestBoard < currentValue:
                break
            if valueHardestBoard == currentValue:
                sameValue += 1
            else:
                currentValue = valueHardestBoard
                self.board = hardestBoard
        return

        # score = self.board.number_of_blocking_and_blocking_blocking_cars()
        # keep making moves untill the score doesn't improve with any move

            # for move in self.board.moves():
            #     test_score = move.number_of_blocking_and_blocking_blocking_cars()
            #     difference = test_score - score
            #     # print(score, test_score)
            #     if test_score > score:
            #         score = test_score 
            #         self.board = move
    
    def get_board(self):
        return self.board.cars

