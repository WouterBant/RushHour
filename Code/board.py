from car import Car


class Board:
    """Stores the Rush Hour board, a '.' means empty."""

    def __init__(self, size: int) -> None:  ## instead give all the cars in a list or deepcopy
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]

    def placeCar(self, car: Car, row: int, col: int) -> None:
        """
        Places the given car at its initial position.
        """
        if car.orientation == "H":
            for c in range(col, col + car.length):
                self.board[row][c] = car.name
        elif car.orientation == "V":
            for r in range(row, row + car.length):
                self.board[r][col] = car.name
        if car.name == "X":
            self.exitRow = car.row

    def moveCarOne(self, car: Car, direction: str) -> bool:
        """
        Tries to move the car in the given direction, returns True if possible else False.
        """
        if car.orientation == "V":
            if direction == "Down":
                if (
                    car.row + car.length < self.size
                    and self.board[car.row + car.length][car.col] == "."
                ):
                    self.board[car.row][car.col] = "."
                    car.row += 1
                    self.board[car.row + car.length - 1][car.col] = car.name
                    return True
            elif direction == "Up":
                if car.row - 1 >= 0 and self.board[car.row - 1][car.col] == ".":
                    self.board[car.row + car.length - 1][car.col] = "."
                    car.row -= 1
                    self.board[car.row][car.col] = car.name
                    return True
        elif car.orientation == "H":
            if direction == "Right":
                if (
                    car.col + car.length < self.size
                    and self.board[car.row][car.col + car.length] == "."
                ):
                    self.board[car.row][car.col] = "."
                    car.col += 1
                    self.board[car.row][car.col + car.length - 1] = car.name
                    return True
            elif direction == "Left":
                if car.col - 1 >= 0 and self.board[car.row][car.col - 1] == ".":
                    self.board[car.row][car.col + car.length - 1] = "."
                    car.col -= 1
                    self.board[car.row][car.col] = car.name
                    return True
        return False

    def moveCarFar(self, car: Car, direction: str) -> None:
        """
        Moves the car in the given direction until no move could be made.
        """
        while self.moveCarOne(car, direction):
            pass

    def isSolved(self) -> bool:
        """
        Return True if the red car is at the exit.
        """
        return self.board[self.exitRow][self.size - 1] == "X"

    def __str__(self) -> str:
        """
        Magic method that returns a string representation of the board.
        """
        boardRepresentation = ""
        for row in self.board:
            boardRepresentation += " ".join(row) + "\n"
        return boardRepresentation
