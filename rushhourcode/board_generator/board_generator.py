import random
from typing import Set, List, Any, Optional
import copy
from string import ascii_lowercase
import itertools


class Car:
    def __init__(
        self, name: str, orientation: str, col: int, row: int, length: int
    ) -> None:
        self.name = name
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length

    def __str__(self) -> str:
        return "Car({0}, {1}, {2}, {3}, {4})".format(
            self.name, self.orientation, self.col, self.row, self.length
        )

    def __hash__(self) -> int:
        return hash((self.name, self.col, self.row))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Car)


class Board:
    """Stores the set of cars in the board."""

    def __init__(self, cars: Set[Car]) -> None:
        self.cars = cars
        self.size = (
            max(x.col for x in cars) + 1
        )  # Does not work if no vertical car in last col and not efficient, maybe make parent class with size and board and make this class inherit
        self.board: list[list[str]] = [
            ["." for _ in range(self.size)] for _ in range(self.size)
        ]
        print(self.board)
        self.place_cars()
        self.move = None
        self.parentBoard = None
        self.number_of_moves = 0

    def place_cars(self) -> None:
        """Places the given car at its initial position."""
        for car in self.cars:
            if car.orientation == "H":
                for c in range(car.col, car.col + car.length):
                    print(car.row, c)
                    self.board[car.row][c] = car.name
            elif car.orientation == "V":
                for r in range(car.row, car.row + car.length):
                    print(r, car.col)
                    self.board[r][car.col] = car.name
            if car.name == "X":
                self.exitRow = car.row

    def moves(self) -> List["Board"]:
        """Returns all the moves that can be made for the current board."""
        possible_moves = []
        for car in self.cars:
            directions = ["Down", "Up"] if car.orientation == "V" else ["Left", "Right"]
            for direction in directions:
                move = self.moveCarFar(car, direction)
                if move:
                    newCars = copy.deepcopy(self.cars)
                    newCars.remove(car)  # Remove the car before movement
                    newCars.add(move)  # Add the car after movement
                    newBoard = Board(newCars)
                    steps = (
                        move.col - car.col + move.row - car.row
                    )  # Either the row or the column changes
                    newBoard.move = (
                        car.name,
                        steps,
                    )  # Is this the best way to do this???
                    newBoard.parentBoard = self  # Is this the best way to do this???
                    possible_moves.append(newBoard)
                    self.number_of_moves += 1
        return possible_moves

    def randomMove(self) -> Set[Car]:
        """Returns a random move out of all possible moves."""
        possibleMoves = self.moves()
        return random.choice(possibleMoves)

    def moveCarOne(self, car: Car, direction: str) -> Optional[Car]:
        """
        Tries to move the car in the given direction, returns the car after movement if possible else None.
        """
        if direction == "Down":
            if (
                car.row + car.length < self.size
                and self.board[car.row + car.length][car.col] == "."
            ):
                return Car(car.name, car.orientation, car.col, car.row + 1, car.length)
        elif direction == "Up":
            if car.row - 1 >= 0 and self.board[car.row - 1][car.col] == ".":
                return Car(car.name, car.orientation, car.col, car.row - 1, car.length)
        elif direction == "Right":
            if (
                car.col + car.length < self.size
                and self.board[car.row][car.col + car.length] == "."
            ):
                return Car(car.name, car.orientation, car.col + 1, car.row, car.length)
        elif direction == "Left":
            if car.col - 1 >= 0 and self.board[car.row][car.col - 1] == ".":
                return Car(car.name, car.orientation, car.col - 1, car.row, car.length)
        return None

    def moveCarFar(self, car: Car, direction: str) -> Car:
        """Moves the car in the given direction until no move could be made."""
        prev = None
        newCar = self.moveCarOne(car, direction)
        while newCar:
            prev = newCar
            newCar = self.moveCarOne(newCar, direction)
        return prev

    def isSolved(self) -> bool:
        """Return True if the red car is at the exit."""
        return self.board[self.exitRow][self.size - 1] == "X"

    def exit_distance(self) -> int:
        """Returns the distance between the red car and the exit."""
        col = self.size - 1
        while self.board[self.exitRow][col] != "X":
            col -= 1
        return self.size - 1 - col

    def number_blocking_cars(self) -> int:
        """Returns the number of cars that block the red car from the exit."""
        seen = set()
        col = self.size - 1
        cars = 0
        while self.board[self.exitRow][col] != "X":
            if (
                self.board[self.exitRow][col] != "."
                and self.board[self.exitRow][col] not in seen
            ):
                seen.add(self.board[self.exitRow][col])
                cars += 1
            col -= 1
        return cars

    def number_blocking_cars_blocked(self) -> int:  ## TODO need something smart
        """Returns the number of blocking cars that cannot move out of the way."""
        seen = set()
        col = self.size - 1
        cars = 0
        while self.board[self.exitRow][col] != "X":
            if (
                self.board[self.exitRow][col] != "."
                and self.board[self.exitRow][col] not in seen
            ):
                seen.add(self.board[self.exitRow][col])
                cars += 1
            col -= 1
        return cars

    def moves_created(self) -> int:
        """Returns the difference in possible moves between the current and previous board."""
        return self.number_of_moves - self.parentBoard.number_of_moves

    def move_to_free_spot(self) -> bool:  ## TODO need something smart
        """Return if the previous moves was to a spot which is not reachable by any ohter car atm."""
        return True

    def __str__(self) -> str:
        """Magic method that returns a string representation of the board."""
        boardRepresentation = ""
        for row in self.board:
            boardRepresentation += " ".join(row) + "\n"
        return boardRepresentation

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Board)


# a 6x6 board comes with 12 cars and 4 trucks, so I think
# it's fair to assume the ratio is 3:1 for any board

# the exit row on each board is either in the middle (odd size boards)
# or on the rows/2'th row (so row 3 for 6x6, or row 6 for 12x12)
class Generator:
    def __init__(self, size: int):
        self.size = size
        self.area = size ** 2
        self.board: List[List[str]] = [
            ["." for _ in range(self.size)] for _ in range(self.size)
        ]
        self.cars = set()
        self.generate_board()

    def generate_board(self):
        exit_row = (self.size + 1) // 2 - 1
        self.add_car(self.generate_exit_car(exit_row, 0))
        gen = self.iter_all_strings()
        for i in range(100):

            car = self.generate_car("temporary id")
            if self.is_valid(car, exit_row):
                car.name = self.label_gen(gen)
                self.add_car(car)

        non_shuffeled_board = Board(self.cars)
        print(non_shuffeled_board)

    # ID generator from:
    # https://stackoverflow.com/questions/29351492/how-to-make-a-continuous-alphabetic-list-python-from-a-z-then-from-aa-ab-ac-e
    def iter_all_strings(self):
        size = 1
        while True:
            for s in itertools.product(ascii_lowercase, repeat=size):
                yield "".join(s)
            size += 1

    # this part also from:
    # https://stackoverflow.com/questions/29351492/how-to-make-a-continuous-alphabetic-list-python-from-a-z-then-from-aa-ab-ac-e
    def label_gen(self, gen):
        for s in gen:
            return s

    def add_car(self, car: Car):
        if car.orientation == "H":
            for c in range(car.col, car.col + car.length):
                self.board[car.row][c] = car.name
        elif car.orientation == "V":
            for r in range(car.row, car.row + car.length):
                self.board[r][car.col] = car.name
        self.cars.add(car)

    def generate_exit_car(self, row: int, col: int):
        orientation: str = "H"
        name: str = "X"
        length: int = 2
        exit_car = Car(name, orientation, col, row, length)
        return exit_car

    def generate_car(self, car_id: str):
        lengths = [2, 3]
        orientations = ["H", "V"]
        length = random.choices(lengths, weights=[3, 1])[0]
        orientation = random.choice(orientations)
        if orientation == "H":
            col = random.randint(0, self.size - length)
            row = random.randint(0, 5)
        else:
            row = random.randint(0, self.size - length)
            col = random.randint(0, 5)
        car = Car(car_id, orientation, col, row, length)
        return car

    def is_valid(self, car: Car, exit_row: int):
        if car.orientation == "H":
            for c in range(car.col, car.col + car.length):
                if c == self.size:
                    return False
                else:
                    if self.board[car.row][c] != "." or car.row == exit_row:
                        return False
        elif car.orientation == "V":
            for r in range(car.row, car.row + car.length):
                if r == self.size:
                    return False
                else:
                    if self.board[r][car.col] != "." or r == exit_row:
                        return False
        return True


if __name__ == "__main__":
    generated_board = Generator(6)
