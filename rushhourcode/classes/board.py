from __future__ import annotations
from typing import Any, Optional
from .car import Car
import random
import copy


class Board:
    """Stores the set of cars in the board."""

    def __init__(self, cars: set[Car], size: int) -> None:
        self.cars = cars
        self.size = max(x.col for x in cars) + 1 # Does not work if no vertical car in last col and not efficient, maybe make parent class with size and board and make this class inherit
        self.board: list[list[str]] = [["." for _ in range(self.size)] for _ in range(self.size)]
        self.place_cars()
        self.move = None
        self.parentBoard = None
        self.number_of_moves = 0

    def place_cars(self) -> None:
        """Places the given car at its initial position."""
        for car in self.cars:
            if car.orientation == "H":
                for c in range(car.col, car.col + car.length):
                    self.board[car.row][c] = car.name
            elif car.orientation == "V":
                for r in range(car.row, car.row + car.length):
                    self.board[r][car.col] = car.name
            if car.name == "X":
                self.exitRow = car.row

    def moves(self) -> list[Board]:
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
                    steps = move.col - car.col + move.row - car.row # Either the row or the column changes
                    newBoard.move = (car.name, steps)  # Is this the best way to do this???
                    newBoard.parentBoard = self  # Is this the best way to do this???
                    possible_moves.append(newBoard)
                    self.number_of_moves += 1
        return possible_moves

    def randomMove(self) -> set[Car]:
        """Returns a random move out of all possible moves."""
        possibleMoves = self.moves()
        return random.choice(possibleMoves)

    def moveCarOne(self, car: Car, direction: str) -> Optional[Car]:
        """
        Tries to move the car in the given direction, returns the car after movement if possible else None.
        """
        if direction == "Down":
            if car.row + car.length < self.size and self.board[car.row + car.length][car.col] == ".":
                return Car(car.name, car.orientation, car.col, car.row + 1, car.length)
        elif direction == "Up":
            if car.row - 1 >= 0 and self.board[car.row - 1][car.col] == ".":
                return Car(car.name, car.orientation, car.col, car.row - 1, car.length)
        elif direction == "Right":
            if car.col + car.length < self.size and self.board[car.row][car.col + car.length] == ".":
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
        col = self.size - 1
        cars = 0
        while self.board[self.exitRow][col] != "X":
            if self.board[self.exitRow][col] != ".":
                cars += 1
            col -= 1
        return cars

    def number_blocking_cars_blocked(self) -> int:  ## TODO need something smart
        """Returns the number of blocking cars that cannot move out of the way."""
        seen = set()
        col = self.size - 1
        cars = 0
        lookUp = 3 if self.size == 6 else 4
        # print(self.exitRow)
        y1 = y2 = blockCarLength = 0
        while self.board[self.exitRow][col] != "X":
            if self.board[self.exitRow][col] != ".":
                blockCar = self.board[self.exitRow][col]
                blocksBlockCar = []
                blockCarLength = 1
                y1 = y2 = cars = 0
                # print(self)
                for pos_y in range(1, lookUp):
                    if self.board[self.exitRow + pos_y][col] == blockCar:
                        blockCarLength += 1
                    elif self.board[self.exitRow + pos_y][col] == ".":
                        y1 = pos_y
                        # print("hi")
                    else:
                        blocksBlockCar.append(self.board[self.exitRow + pos_y][col])
                        y1 = pos_y
                        break
                for neg_y in range(1, 4):
                    if self.board[self.exitRow - neg_y][col] == blockCar:
                        blockCarLength += 1
                    elif self.board[self.exitRow - neg_y][col] == ".":
                        y2 = neg_y
                    else:
                        blocksBlockCar.append(self.board[self.exitRow - neg_y][col])
                        y2 = neg_y
                        break
                print(self, y1, y2, blockCarLength)
                if blockCarLength > y1 and blockCarLength > y2:
                    new = True
                    for i in blocksBlockCar:
                        if i in seen:
                            new = False
                        else:
                            seen.add(i)
                    if new:
                        cars += 1
                print(cars)
            col -= 1
        # print(self, cars, y1, y2, blockCarLength)
        # y
        return cars

    def moves_created(self) -> int:
        """Returns the difference in possible moves between the current and previous board."""
        return self.number_of_moves - self.parentBoard.number_of_moves

    def move_to_free_spot(self) -> bool:  ## TODO need something smart
        """Return if the previous moves was to a spot which is not reachable by any other car atm."""
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
