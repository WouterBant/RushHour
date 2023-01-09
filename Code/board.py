from car import Car

class Board:

    def __init__(self, dim: int) -> None:
        self.dim = dim
        self.board = [["."] * dim ] * dim

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
        print(self.board)
        
    
    def moveCarOne(self, car, dir):
        if car.orientation == "V":
            if dir == "Down":
                if car.row + car.length + 1 < self.dim and self.board[car.row + car.length + 1][car.col] == ".":
                    self.board[car.row][car.col] = "."
                    car.row += 1
                    self.board[car.row + car.length][car.col] = car.name
                    return True
                return False
            else:
                if car.row - 1 >= 0 and self.board[car.row - 1][car.col] == ".":
                    self.board[car.row + car.length][car.col] = "."
                    car.row -= 1
                    self.board[car.row][car.col] = car.name
                    return True
                return False
        else:
            pass

        

    def moveCarFar(self, car):
        pass
