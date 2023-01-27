from ..classes.board import Board
import heapq
import sys


class AStar1:
    """
    Uses the number of cars blocking the red car to determine which board to look at first and the number of previous steps.
    This is admissable, since for all these cars at least one move is necessary to be able to solve the board.
    And thus finds the minimum number of steps required to solve the board.
    """

    def __init__(self, board: Board, display: bool = False) -> None:
        self.startBoard = board
        self.visit = set()
        self.pq: list[tuple[float, int, Board]] = []
        heapq.heappush(self.pq, (0, 0, board))
        self.display = display
        self.count_to_display = 0

    def costCalculator(self, board: Board) -> int:  # Admissable
        """Returns the number of cars in front of the red car"""
        return board.number_blocking_cars()

    def run(self) -> list[Board]:
        while self.pq:
            cost, depth, currentBoard = heapq.heappop(self.pq)

            # Display depth if user wants that
            if self.count_to_display % 1000 == 0 and self.display:
                print(f"The current depth is {depth}\n")
            self.count_to_display += 1

            # When the game is solved return the winning path
            if currentBoard.isSolved():
                return currentBoard.get_path()

            # Look at all moves that could be made
            for newBoard in currentBoard.moves():
                # Check if you already have seen this board if so skip else add it to visit and Priority Queue
                if newBoard in self.visit:
                    continue
                self.visit.add(newBoard)

                # Compute the cost and push the board to the Priority Queue
                costNewBoard = self.costCalculator(newBoard) + depth
                heapq.heappush(self.pq, (costNewBoard, depth + 1, newBoard))

        print("\nNo solution, try different parameters.")
        sys.exit()


class AStar2(AStar1):
    """
    Uses the number of cars blocking the red car and a lower bound for the number of steps necessary
    to move these 'blockers' out of the way to determine which board to look at first and the number of previous steps.
    This is admissable, since all these steps are required.
    And thus finds the minimum number of steps required to solve the board.
    """

    def costCalculator(self, board: Board) -> int:  # Admissable
        """
        Returns the sum of the number of cars in front of the red car and a lower bound to move these
        blocker out of the way.
        """
        return board.number_of_blocking_and_blocking_blocking_cars()


class AStar3(AStar1):
    """
    This version also makes use of the distance the red car has from the exit and the number of additional moves
    the new board has in comparison to the parent board.
    """

    def costCalculator(self, board: Board) -> int:  # Board 4 6
        return 3 * board.exit_distance() + 3 * board.number_blocking_cars() - 14 * board.moves_created()
