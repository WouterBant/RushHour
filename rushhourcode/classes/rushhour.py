from .board import Board
from .car import Car
import csv


class RushHour:

    def __init__(self, filename: str = "", randomBoard: set[Car] = None, fromFile: bool = True) -> None:
        """Loads a set of cars from a file or from a random board."""
        if fromFile:
            self.cars: set[Car] = set()
            self.load_cars(filename)
        else:
            self.cars = set(randomBoard)

    def load_cars(self, filename: str) -> None:
        """Loads the cars from the file in a set."""
        with open(filename) as file:
            file.readline()  # Skip over header
            for new_line in file.readlines():
                line = new_line.strip("\n").split(",")
                name, orientation = line[:2]
                col, row, length = int(line[2]) - 1, int(line[3]) - 1, int(line[4])
                new_car = Car(name, orientation, col, row, length)
                self.cars.add(new_car)

    def output_path(self, path: list[Board]) -> None:
        """Outputs the moves from the most recent found solution to a csv file."""
        moves = [board.move for board in path]
        with open("output/output.csv", "w", newline="") as move_file:
            move_writer = csv.writer(move_file, delimiter=",")
            move_writer.writerow(["car", "move"])
            for car, move in moves:
                move_writer.writerow([car, move])

    def output_boards(self, boards: list[list[str]]) -> None:
        """Outputs the boards in the path from the most recent found solution to a csv file."""
        with open("output/boards_output.csv", "w", newline="") as boards_file:
            boards_writer = csv.writer(boards_file, delimiter=",")
            for b in boards:
                boards_writer.writerows(b.board)
