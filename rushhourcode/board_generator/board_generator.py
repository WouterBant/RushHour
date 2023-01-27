from ..classes.board import Board
from ..classes.car import Car
import itertools
import random
from string import ascii_uppercase
import sys


class Generator:
    """Class to generate random rush hour puzzles based on user input."""

    def __init__(self) -> None:
        self.size, tries, shuffles = self.get_size_tries_shuffles()
        self.area = self.size ** 2
        self.cars = set()
        self.board = Board(self.cars, self.size)
        self.generate_board(tries)
        self.shuffle_board(shuffles)
        self.hill_climb()

    def get_size_tries_shuffles(self) -> tuple[int, int, int]:
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

    def generate_board(self, tries: int) -> None:
        """Generates an empty board and add cars to it."""
        exit_row = (self.size + 1) // 2 - 1
        self.add_car(self.generate_red_car(exit_row, 0))

        # add cars with unique ID's, only if their position is valid
        gen = self.iter_all_strings()
        for _ in range(tries):
            car = self.generate_car("temporary id")
            if self.is_valid(car, exit_row):
                car.name = self.label_gen(gen)
                self.add_car(car)

    def shuffle_board(self, shuffles) -> None:
        """Makes a certain amount of random moves to shuffle the board."""
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

    def add_car(self, car: Car) -> None:
        """Adds a new car to the board."""
        if car.orientation == "H":
            for c in range(car.col, car.col + car.length):
                self.board.board[car.row][c] = car.name
        elif car.orientation == "V":
            for r in range(car.row, car.row + car.length):
                self.board.board[r][car.col] = car.name
        self.board.cars.add(car)

    def generate_red_car(self, row: int, col: int) -> Car:
        """Places the red car on the correct row."""
        name, orientation, length = "X", "H", 2
        red_car = Car(name, orientation, col, row, length)
        return red_car

    def generate_car(self, car_id: str) -> Car:
        """Generates random cars."""
        length = random.choices([2, 3], weights=[3, 1])[0]  # Ratio trucks/cars = 1/3
        orientation = random.choice(["H", "V"])
        if orientation == "H":
            col = random.randint(0, self.size - length)
            row = random.randint(0, self.size - 1)
        else:
            row = random.randint(0, self.size - length)
            col = random.randint(0, self.size - 1)
        car = Car(car_id, orientation, col, row, length)
        return car

    def is_valid(self, car: Car, exit_row: int):
        """
        Check if the the new car fits inside the borders of the board and does not block the red car.
        """
        if car.name == "X":
            return False
        if car.orientation == "H":
            for c in range(car.col, car.col + car.length):
                if c == self.size:
                    return False
                elif self.board.board[car.row][c] != "." or car.row == exit_row:
                    return False
        elif car.orientation == "V":
            for r in range(car.row, car.row + car.length):
                if r == self.size:
                    return False
                elif self.board.board[r][car.col] != "." or r == exit_row:
                    return False
        return True

    def hill_climb(self) -> None:
        """Reverse hill climber to make the boards a bit harder."""
        # When the difficulty of the board stays the same after 10 consecutive moves stop the hill climber
        sameValue = currentValue = 0
        while sameValue < 10:
            moves = [move for move in self.board.moves()]
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

    def get_board(self):
        return self.board.cars
