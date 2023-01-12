from car import Car
import random
import copy


class Board:
    """Stores the Rush Hour board, a '.' means empty."""

    def __init__(self, cars: set[Car]) -> None:  ## set for O(1) removal
        self.cars = cars
        self.board = None
        self.size = 6

    def make_board(self) -> None:
        """
        Places the given car at its initial position.
        """
        if self.board:
            return
        self.board = [["." for _ in range(6)] for _ in range(6)]  ## for all sizes
        for car in self.cars:
            if car.orientation == "H":
                for c in range(car.col, car.col + car.length):
                    self.board[car.row][c] = car.name
            elif car.orientation == "V":
                for r in range(car.row, car.row + car.length):
                    self.board[r][car.col] = car.name
            if car.name == "X":  # Find other way
                self.exitRow = car.row

    def moves(self):
        self.make_board()
        boardOriginal = copy.deepcopy(self.board)
        carsOriginal = copy.deepcopy(self.cars)
        # for i in carsOriginal:
        #     print(i)
        # print(boardOriginal)
        possible_moves = []
        for car in carsOriginal:
            directions = ['Down', 'Up'] if car.orientation == 'V' else ['Left', 'Right']
            for direction in directions:
                # print(car.name, direction)
                move = self.moveCarFar(car, direction)
                if move:
                    # print("W")
                    # print(car, move)
                    # newCars = self.cars.copy()
                    # for i in carsOriginal:
                    #     print(i)
                    newCars = copy.deepcopy(carsOriginal)
                    # assert newCars == carsOriginal
                    # for i in newCars:
                    #     print(i)
                    # for i in carsOriginal:
                    #     print(i)
                    # print(car, move)
                    newCars.remove(car)
                    newCars.add(move)
                    # for i in newCars:
                    #     print(i)
                    possible_moves.append(newCars)
                self.board = copy.deepcopy(boardOriginal)
                # print(self.board)
        # print(len(possible_moves))
        # for i in possible_moves:
        #     b = Board(i)
        #     print(b)
        # for i in carsOriginal:
        #     print(i)
        # return -1
        return possible_moves

    def randomMove(self):
        possibleMoves = self.moves()
        return random.choice(possibleMoves)

    def __hash__(self) -> int:
        return hash(self.__repr__)

    def __eq__(self, other):
        return isinstance(other, Board)

    def moveCarOne(self, car: Car, direction: str) -> Car:
        """
        Tries to move the car in the given direction, returns True if possible else False.
        """
        if direction == "Down":
            if (
                    car.row + car.length < self.size
                    and self.board[car.row + car.length][car.col] == "."
            ):
                newCar = Car(car.name, car.orientation, car.col, car.row + 1, car.length)
                return newCar
        elif direction == "Up":
            if car.row - 1 >= 0 and self.board[car.row - 1][car.col] == ".":
                newCar = Car(car.name, car.orientation, car.col, car.row - 1, car.length)
                return newCar
        elif direction == "Right":
            if (
                    car.col + car.length < self.size
                    and self.board[car.row][car.col + car.length] == "."
            ):
                newCar = Car(car.name, car.orientation, car.col + 1, car.row, car.length)
                return newCar
        elif direction == "Left":
            if car.col - 1 >= 0 and self.board[car.row][car.col - 1] == ".":
                newCar = Car(car.name, car.orientation, car.col - 1, car.row, car.length)
                return newCar
        return None

    def moveCarFar(self, car: Car, direction: str) -> Car:
        """
        Moves the car in the given direction until no move could be made.
        """
        prev = None
        newCar = self.moveCarOne(car, direction)
        while newCar:
            prev = newCar
            newCar = self.moveCarOne(newCar, direction)
        # if not prev:
        #     print("hi")
        return prev

    def isSolved(self) -> bool:
        """
        Return True if the red car is at the exit.
        """
        self.make_board()
        return self.board[2][5] == "X"
        return self.board[self.exitRow][self.size - 1] == "X"

    def __str__(self) -> str:
        """
        Magic method that returns a string representation of the board.
        """
        self.make_board()
        boardRepresentation = ""
        for row in self.board:
            boardRepresentation += " ".join(row) + "\n"
        return boardRepresentation
