from __future__ import annotations
from typing import Any, Optional
from .car import Car
import random


class Board:
    """
    Stores a set of car objects, keeps track of its size, the move to this board, and its parent.
    """

    def __init__(self, cars: set[Car], size: int, move: Optional[tuple[str, int]] = None,
                 parentBoard: Optional[Board] = None) -> None:
        self.cars, self.size, self.move, self.parentBoard = cars, size, move, parentBoard
        self.exitRow = 2 if self.size == 6 else (4 if self.size == 9 else 5)
        self.place_cars()

    def place_cars(self) -> None:
        """Places the given car at its initial position."""
        self.board: list[list[str]] = [["." for _ in range(self.size)] for _ in range(self.size)]
        for car in self.cars:
            if car.orientation == "H":
                for c in range(car.col, car.col + car.length):
                    self.board[car.row][c] = car.name
            elif car.orientation == "V":
                for r in range(car.row, car.row + car.length):
                    self.board[r][car.col] = car.name

    def moves(self) -> list[Board]:
        """Returns all the moves that can be made for the current board."""
        possible_moves = []
        for initialCar in self.cars:
            directions = ["Down", "Up"] if initialCar.orientation == "V" else ["Left", "Right"]
            for direction in directions:
                movedCar = self.moveCarFar(initialCar, direction)  # Always move the car as far as possible
                if movedCar:  # When the car was able to move
                    newCars = set(self.cars); newCars.remove(initialCar); newCars.add(movedCar)  # Replace old with new car
                    steps = movedCar.col - initialCar.col + movedCar.row - initialCar.row  # Either row or column changes
                    newBoard = Board(newCars, self.size, move=(initialCar.name, steps), parentBoard=self)
                    possible_moves.append(newBoard)
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
        """Moves the car in the given direction until no move can be made."""
        # When newCar becomes None the move was not possible so return prev
        prev, newCar = None, self.moveCarOne(car, direction)
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
        col, blockingCars = self.size - 1, 0
        while self.board[self.exitRow][col] != "X":
            if self.board[self.exitRow][col] != ".":
                blockingCars += 1
            col -= 1
        return blockingCars
    
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

                # Find out which cars are blocking the car from above and below
                blocksBlockCarUp = []
                blocksBlockCarDown = []

                for pos_y in range(1, lookUp):
                    if self.board[self.exitRow + pos_y][col] == blockCar:
                        blockCarPosUp = pos_y

                    elif self.board[self.exitRow + pos_y][col] == ".":
                        # Get contiguous number of empty spots
                        if freeMoveUp == pos_y - blockCarPosUp - 1:
                            freeMoveUp += 1

                    elif self.board[self.exitRow + pos_y][col] not in blockingCarsBlockersSeen:
                        blocksBlockCarUp.append(self.board[self.exitRow + pos_y][col])
                        blockingCarsBlockersSeen.add(self.board[self.exitRow + pos_y][col])

                for neg_y in range(1, lookDown):
                    if self.board[self.exitRow - neg_y][col] == blockCar:
                        blockCarPosDown = neg_y

                    elif self.board[self.exitRow - neg_y][col] == ".":
                        # Get contiguous number of empty spots
                        if freeMoveDown == neg_y - blockCarPosDown - 1:
                            freeMoveDown += 1

                    elif self.board[self.exitRow - neg_y][col] not in blockingCarsBlockersSeen:
                        blocksBlockCarDown.append(self.board[self.exitRow - neg_y][col])
                        blockingCarsBlockersSeen.add(self.board[self.exitRow - neg_y][col])

                #  See if the blocking car can already move out of the way
                if blockCarPosDown + 1 <= freeMoveUp or blockCarPosUp + 1 <= freeMoveDown:
                    for car in blocksBlockCarDown + blocksBlockCarUp:
                        blockingCarsBlockersSeen.remove(car)  # These blockers are not moved

                # If the blocking car length is 3 and the board has size 6, it has to move down
                elif blockCarPosDown + blockCarPosUp + 1 == 3 and lookUp == 3:
                    blockingCarsBlockers += len(blocksBlockCarDown)

                    for car in blocksBlockCarUp:  # The blockers above are not moved
                        blockingCarsBlockersSeen.remove(car)

                # When length block car is 3, the blocker goes in the direction with the least blockers
                elif blockCarPosDown + blockCarPosUp + 1 == 3:
                    blockingCarsBlockers += min(len(blocksBlockCarDown), len(blocksBlockCarUp))

                # When length block car is 2 at least 1 additional move is necessary
                else:
                    return 1
                    # return min(len(blocksBlockCarDown), len(blocksBlockCarUp), 1)

            col -= 1
        return blockingCars + blockingCarsBlockers
    
    def n_cars(self) -> int:
        """Returns the number of cars on the board."""
        # return sum(1 for car in self.cars if car.length == 2)
        counter = 0
        for car in self.cars:
            if car.length == 2:
                counter += 1
        return counter

    def n_trucks(self) -> int:
        """Returns the number of trucks on the board."""
        # return sum(1 for car in self.cars if car.length == 3)
        counter = 0
        for car in self.cars:
            if car.length == 3:
                counter += 1
        return counter
    
    def orientation_grade(self) -> int:
        """Gives a grade based on the orientation of all cars."""
        # return sum(car.length if car.orientation == "H" else -car.length for car in self.cars)
        grade = 0
        for car in self.cars:
            if car.orientation == "H":
                grade += car.length 
            elif car.orientation == "V":
                grade -= car.length
        return grade

    def moves_created(self) -> int:
        """Returns the difference in possible moves between the current and previous board."""
        return len(self.moves()) - len(self.parentBoard.moves())

    def get_path(self) -> list[Board]:
        """Returns the path to this board by traversing back up in the graph of boards.."""
        path, board = [], self
        while board.parentBoard:
            path.append(board)
            board = board.parentBoard
        return path[::-1] # Order reversed since traversing is started at leaf board

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
