from car import Car


class Board:
    """ Stores the Rush Hour board, a '.' means empty. """

    def __init__(self, dim: int) -> None:
        self.dim = dim
        self.board = [["." for _ in range(dim)] for _ in range(dim)]

    def placeCar(self, car: Car, row: int, col: int) -> None:
        carName = car.name
        carOrientation = car.orientation
        carLength = car.length
        if carOrientation == "H":
            for c in range(col, col + carLength):
                self.board[row][c] = carName
        else:
            for r in range(row, row + carLength):
                self.board[r][col] = carName

    def moveCarOne(self, car: Car, dir: str) -> bool:
        """
        Tries to move the car in the given direction, returns True if possible else False.
        """
        if car.orientation == "V":
            if dir == "Down":
                if car.row + car.length < self.dim and self.board[car.row + car.length][car.col] == ".":
                    self.board[car.row][car.col] = "."
                    car.row += 1
                    self.board[car.row + car.length - 1][car.col] = car.name
                    return True
            elif dir == "Up":
                if car.row - 1 >= 0 and self.board[car.row - 1][car.col] == ".":
                    self.board[car.row + car.length - 1][car.col] = "."
                    car.row -= 1
                    self.board[car.row][car.col] = car.name
                    return True
        elif car.orientation == "H":
            if dir == "Right":
                if car.col + car.length < self.dim and self.board[car.row][car.col + car.length] == ".":
                    self.board[car.row][car.col] = "."
                    car.col += 1
                    self.board[car.row][car.col + car.length - 1] = car.name
                    return True
            elif dir == "Left":
                if car.col - 1 >= 0 and self.board[car.row][car.col - 1] == ".":
                    self.board[car.row][car.col + car.length - 1] = "."
                    car.col -= 1
                    self.board[car.row][car.col] = car.name
                    return True
        return False

    def moveCarFar(self, car: Car, dir: str) -> None:
        """
        Moves the car in the given direction until no move could be made.
        """
        while True:
            if not self.moveCarOne(car, dir):
                break

    def __str__(self) -> str:
        """
        Magic method that returns a string representation of the board.
        """
        boardRepresentation = ''
        for row in self.board:
            boardRepresentation += ' '.join(row) + '\n'
        return boardRepresentation
