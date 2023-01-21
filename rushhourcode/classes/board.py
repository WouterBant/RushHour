from __future__ import annotations
from typing import Any, Optional
from .car import Car
import random


class Board:
    """
    Stores a set of car objects, keeps track of its size, the move to this board, and its parent.
    """

    def __init__(self, cars: set[Car], size: int,
                 move: Optional[tuple[str, int]] = None,
                 parentBoard: Optional[Board] = None) -> None:
        self.cars = cars
        self.size = size
        self.board: list[list[str]] = [["." for _ in range(self.size)] for _ in range(self.size)]
        self.place_cars()
        self.move = move
        self.parentBoard = parentBoard
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
                    newCars = set(self.cars)
                    newCars.remove(car)  # Remove the car before movement
                    newCars.add(move)  # Add the car after movement
                    steps = move.col - car.col + move.row - car.row  # Either the row or the column changes
                    moveMade = (car.name, steps)
                    parentBoard = self
                    newBoard = Board(newCars, self.size, moveMade, parentBoard)
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

    def number_of_blocking_and_blocking_blocking_cars(self) -> int:
        """
        Returns the number cars in the way of the red car plus a lowerbound for the steps it
        takes to move these blocking cars out of the way. Code is rather extensive, such that
        the best estimate is given without looking more than 2 moves ahead.
        """
        blockingCarsBlockersSeen = set()  # Don't move same car twice, may lead to overestimation
        col = self.size - 1
        blockingCarsBlockers = blockingCars = 0

        # Don't look further than maximum car length (3)
        lookUp = 3 if self.size == 6 else 4  # Only 2 spots above exitrow 6x6 board
        lookDown = 4

        while self.board[self.exitRow][col] != "X":
            if self.board[self.exitRow][col] != ".":  # Found a new blocking car
                blockingCars += 1
                blockCar = self.board[self.exitRow][col]  # Find out which car is blocking
                blockCarPosUp = blockCarPosDown = 0  # Find out how the blocking car is positioned
                freeMoveUp = freeMoveDown = 0  # Find out which spots the blocking car can go to
                blocksBlockCarUp = []  # Find out which cars are blocking the car from above
                blocksBlockCarDown = []  # Find out which cars are blocking the car from below

                for pos_y in range(1, lookUp):
                    if self.board[self.exitRow + pos_y][col] == blockCar:
                        blockCarPosUp = pos_y
                    elif self.board[self.exitRow + pos_y][col] == ".":
                        # Get contiguous number of empty spots
                        if freeMoveUp == pos_y - 1:
                            freeMoveUp = pos_y
                    elif self.board[self.exitRow + pos_y][col] not in blockingCarsBlockersSeen:
                        blocksBlockCarUp.append((pos_y, self.board[self.exitRow + pos_y][col]))
                        blockingCarsBlockersSeen.add(self.board[self.exitRow + pos_y][col])

                for neg_y in range(1, lookDown):
                    if self.board[self.exitRow - neg_y][col] == blockCar:
                        blockCarPosDown = neg_y
                    elif self.board[self.exitRow - neg_y][col] == ".":
                        # Get contiguous number of empty spots
                        if freeMoveDown == neg_y - 1:
                            freeMoveDown = neg_y
                    elif self.board[self.exitRow - neg_y][col] not in blockingCarsBlockersSeen:
                        blocksBlockCarDown.append((neg_y, self.board[self.exitRow - neg_y][col]))
                        blockingCarsBlockersSeen.add(self.board[self.exitRow - neg_y][col])

                #  See if the blocking car can already move out of the way
                if blockCarPosDown + 1 <= freeMoveUp or blockCarPosUp + 1 <= freeMoveDown:
                    # The before unmoved blockers of blocking car are not now also not moved
                    for pos, car in blocksBlockCarDown + blocksBlockCarUp:
                        blockingCarsBlockersSeen.remove(car)
                # If the blocking car length is 3 and the board has size 6, it has to move down
                elif blockCarPosDown + blockCarPosUp + 1 == 3 and lookUp == 3:
                    blockingCarsBlockers += len(blocksBlockCarDown)
                    # The blocking cars above are not moved
                    for pos, car in blocksBlockCarUp:
                        blockingCarsBlockersSeen.remove(car)
                # When length block car is 3, the blocker goes in the direction with the least blockers
                # Since we don't want to overestimate nothing is removed
                elif blockCarPosDown+blockCarPosUp + 1 == 3:
                    blockingCarsBlockers += min(len(blocksBlockCarDown), len(blocksBlockCarUp))
                else:
                    blockingCarsBlockers += min(len(blocksBlockCarDown), len(blocksBlockCarUp), 1)

            col -= 1
        return blockingCars + blockingCarsBlockers

    def moves_created(self) -> int:
        """Returns the difference in possible moves between the current and previous board."""
        return self.number_of_moves - self.parentBoard.number_of_moves

    def move_to_free_spot(self) -> bool:  ## TODO need something smart
        """Return if the previous moves was to a spot which is not reachable by any other car atm."""
        return True

    def get_path(self) -> list[Board]:
        """Returns the path to this board."""
        path = [self]
        board = self
        # Create the path by traversing back in the graph
        while board.parentBoard:
            board = board.parentBoard
            path.append(board)
        return path[::-1][1:]  # Order reversed since traversing is started at leaf board

    def __str__(self) -> str:
        """Magic method that returns a string representation of the board."""
        boardRepresentation = ""
        for row in self.board:
            for slot in row:
                boardRepresentation += f"{slot:<3}"
            boardRepresentation += "\n"
        return boardRepresentation

    def __hash__(self) -> int:
        """Makes it possible use boards in sets and as keys in dictionaries."""
        return hash(self.__str__())

    def __eq__(self, other: Any) -> bool:
        """Necessary for Priority Queue."""
        return isinstance(other, Board)
        # and self.__hash__() == other.__hash__()
