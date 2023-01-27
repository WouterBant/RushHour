# this file contains the car class for a RushHour board

from typing import Any

class Car:
    """This is a class for a car on the RushHour board"""

    def __init__(self, name: str, orientation: str, col: int, row: int, length: int) -> None:
        """This method initializes a car with a given name, orientation, column, row and length"""
        self.name = name
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length

    def __str__(self) -> str:
        """Method which returns a string with a car and its name, orientation, column, row and length"""
        return "Car({0}, {1}, {2}, {3}, {4})".format(self.name, self.orientation, self.col, self.row, self.length)

    def __hash__(self) -> int:
        """Method which returns and hashes the name, column and row of a car"""
        return hash((self.name, self.col, self.row))

    def __eq__(self, other: Any) -> bool:
        """Method which returns True if self and other are equal"""
        return isinstance(other, Car)
