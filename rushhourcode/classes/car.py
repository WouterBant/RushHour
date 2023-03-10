from typing import Any


class Car:
    """Contains the information for a car."""

    def __init__(self, name: str, orientation: str, col: int, row: int, length: int) -> None:
        self.name = name
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length

    def __str__(self) -> str:
        return "Car({0}, {1}, {2}, {3}, {4})".format(self.name, self.orientation, self.col, self.row, self.length)

    def __hash__(self) -> int:
        """Method which returns a hash based on the name, column, and row of a car."""
        return hash((self.name, self.col, self.row))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Car)
