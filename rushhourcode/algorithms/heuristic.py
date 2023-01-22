from ..classes.board import Board
import heapq
from typing import List, Tuple
import sys


class Heuristic1:
    """
    Uses the number of cars blocking the red car to determine which board to look at first.
    This is admissable, since for all these cars at least one move is necessary.
    And thus finds the minimum number of steps required to solve the board.
    """

    def __init__(self, board: Board) -> None:
        self.startBoard = board
        self.visit = set()
        self.pq: List[Tuple[float, int, Board]] = []
        heapq.heappush(self.pq, (0, 0, board))

    def costCalculator(self, board: Board) -> int:  # Admissable
        """Returns the number of cars in front of the red car"""
        return board.number_blocking_cars()

    def run(self) -> list[Board]:
        while self.pq:
            cost, depth, currentBoard = heapq.heappop(self.pq)

            # When the game is solved return the winning path
            if currentBoard.isSolved():
                return currentBoard.get_path()

            # Look at all moves that could be made
            for newBoard in currentBoard.moves():
                # Check if you already have seen this board if so skip else add it to visit and Priority Queue
                if newBoard in self.visit:
                    continue
                self.visit.add(newBoard)

                costNewBoard = self.costCalculator(newBoard) + depth
                heapq.heappush(self.pq, (costNewBoard, depth + 1, newBoard))

        print("\nNo solution, try different parameters.")
        sys.exit()


class Heuristic2(Heuristic1):
    """
    Uses the number of cars blocking the red car and a lower bound for the number of steps necessary
    to move these 'blockers' out of the way to determine which board to look at first.
    This is admissable, since all these steps are required.
    And thus finds the minimum number of steps required to solve the board.
    """
    def costCalculator(self, board: Board) -> int:  # Admissable
        """
        Returns the sum of the number of cars in front of the red car and a lower bound to move these
        blocker out of the way.
        """
        return board.number_of_blocking_and_blocking_blocking_cars()


class Heuristic3(Heuristic1):

    def costCalculator(self, board: Board) -> int:  # Board 4 6
        return 3 * board.exit_distance() + 3 * board.number_blocking_cars() - 14 * board.moves_created()
