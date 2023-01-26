from .car import Car
from .board import Board

import csv


class RushHour:
    
    def __init__(self, filename: str) -> None:
        self.cars: set[Car] = set()
        self.load_cars(filename)

    def load_cars(self, filename: str) -> None:
        with open(filename) as file:
            file.readline()  # Skip over header
            for new_line in file.readlines():
                line = new_line.strip("\n").split(",")
                name, orientation = line[:2]
                col, row, length = int(line[2]) - 1, int(line[3]) - 1, int(line[4])
                new_car = Car(name, orientation, col, row, length)
                self.cars.add(new_car)

    def load_board(self, size: int) -> None:  # WAAR GEBRUIKEN WE DIT
        game_board = Board(self.cars, size)
        for car in self.cars:
            y, x = car.row, car.col
            if car.orientation == "H":
                for i in range(0, car.length):
                    game_board.board[y][x + i] = car.name
            elif car.orientation == "V":
                for j in range(0, car.length):
                    game_board.board[y + j][x] = car.name

    def output_path(self, moves: list[list[str]]) -> None:
        with open("output/output.csv", "w", newline="") as move_file:
            move_writer = csv.writer(move_file, delimiter=",")
            move_writer.writerow(["car", "move"])
            for car, move in moves:
                move_writer.writerow([car, move])

    def output_boards(self, boards: list[list[str]]) -> None:
        with open("output/boards_output.csv", "w", newline="") as boards_file:
            boards_writer = csv.writer(boards_file, delimiter=",")
            for b in boards:
                boards_writer.writerows(b.board)
