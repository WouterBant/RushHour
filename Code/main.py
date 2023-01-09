from car import Car
from board import Board
from sys import argv


class RushHour:
    def __init__(self, filename):

        self.cars = []
        self.load_cars(filename)

    def load_cars(self, filename):
        print(filename)
        with open(filename) as f:
            for line in f:
                newline = f.readline().split(",")
                print(newline)


if __name__ == "__main__":

    if len(argv) != 2:
        print("Usage: python main.py [filename]")
        exit(1)
    gamename = f"gameboards/{argv[1]}.csv"
    print(gamename)
    game = RushHour(gamename)
