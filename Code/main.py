from car import Car
from board import Board
from sys import argv
from typing import List
import csv


class RushHour:
    """Create the RushHour game"""

    def __init__(self, filename: str) -> None:
        """Initialises the Class"""

        self.cars: List = []
        self.load_cars(filename)
        self.load_board()

    def load_cars(self, filename: str) -> None:
        """Load all cars from the textfile"""

        with open(filename) as f:
            f.readline()
            for line in f:
                line = line.split(",")
                name: str = line[0]
                orientation: str = line[1]
                col: int = int(line[2]) - 1
                row: int = int(line[3]) - 1
                length: int = int(line[4].replace("\n", ""))
                new_car: Car = Car(
                    name=name,
                    orientation=orientation,
                    col=col,
                    row=row,
                    length=length,
                )
                self.cars.append(new_car)

    def load_board(self) -> None:
        """Initialise the board and implements the cars"""

        game_board = Board(6)
        for car in self.cars:
            y: int = car.row
            x: int = car.col
            if car.orientation == "H":
                for i in range(0, car.length):
                    game_board.board[y][x + i] = car.name
            elif car.orientation == "V":
                for j in range(0, car.length):
                    game_board.board[y + j][x] = car.name
        print(game_board)

    def output(self, moves):
        with open('new_file.csv', 'w', newline='') as csvfile:
            csv.csvwriter.writerow(['car', 'move'])
            for car, move in moves:
                csv.csvwriter.writerow([car, move])


if __name__ == "__main__":

    if len(argv) != 2:
        print("Usage: python main.py [filename]")
        exit(1)
    gamename = f"gameboards/{argv[1]}.csv"
    game = RushHour(gamename)
