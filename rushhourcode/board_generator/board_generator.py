import random
from typing import Set, List, Any, Optional
from string import ascii_uppercase
import itertools
from typing import List, Set
from ..classes.board import Board
from ..classes.car import Car

# a 6x6 board comes with 12 cars and 4 trucks, so I think
# it's fair to assume the ratio is 3:1 for any board

# the exit row on each board is either in the middle (odd size boards)
# or on the rows/2'th row (so row 3 for 6x6, or row 6 for 12x12)
class Generator:
    def __init__(self, size: int, tries: int, shuffles: int) -> None:
        self.size = size
        self.tries = tries 
        self.shuffles = shuffles
        self.area = size ** 2
        self.cars = set()
        self.board = Board(self.cars, self.size)
        self.generate_board()
        self.shuffle_board()
        self.hill_climb()

    def generate_board(self) -> None:
        exit_row = (self.size + 1) // 2 - 1
        self.add_car(self.generate_exit_car(exit_row, 0))
        gen = self.iter_all_strings()
        for _ in range(self.tries):

            car = self.generate_car("temporary id")
            if self.is_valid(car, exit_row):
                car.name = self.label_gen(gen)
                self.add_car(car)
    
    def shuffle_board(self) -> None:
        for _ in range(self.shuffles):
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

    def add_car(self, car: Car):
        if car.orientation == "H":
            for c in range(car.col, car.col + car.length):
                self.board.board[car.row][c] = car.name
        elif car.orientation == "V":
            for r in range(car.row, car.row + car.length):
                self.board.board[r][car.col] = car.name
        self.board.cars.add(car)

    def generate_exit_car(self, row: int, col: int) -> Car:
        orientation: str = "H"
        name: str = "X"
        length: int = 2
        exit_car = Car(name, orientation, col, row, length)
        return exit_car

    def generate_car(self, car_id: str) -> Car:
        lengths = [2, 3]
        orientations = ["H", "V"]
        length = random.choices(lengths, weights=[3, 1])[0]
        orientation = random.choice(orientations)
        if orientation == "H":
            col = random.randint(0, self.size - length)
            row = random.randint(0, self.size - 1)
        else:
            row = random.randint(0, self.size - length)
            col = random.randint(0, self.size - 1)
        car = Car(car_id, orientation, col, row, length)
        return car

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
    
    def hill_climb(self) -> None:
        score = self.board.number_of_blocking_and_blocking_blocking_cars()
        difference = -1
        while difference != 0:
            for move in self.board.moves():
                test_score = move.number_of_blocking_and_blocking_blocking_cars()
                difference = test_score - score
                print(score, test_score)
                if test_score > score:
                    score = test_score 
                    self.board = move 
        print(self.board.n_cars(), self.board.n_trucks(), self.board.orientation_grade())

