from ..classes.board import Board
from typing import Optional


class DepthFirst:
    """
    Tries to find a solution in a depth first manner with recursion. When the maximum depth
    is less than the least number of required steps, no solution will be found.
    """

    def __init__(self, startBoard: Board, max_depth: int) -> None:
        self.startBoard = startBoard
        self.max_depth = max_depth

    def dfs(self, currentBoard: Board, current_depth: int) -> Optional[list[Board]]:
        """
        Returns a solution if the maximum depth >= to the minimum number of steps
        necessary to solve the board. Else returns None. This solution is only guaranteed
        to be optimal if maximum depth = minimum number of steps to solve the board.
        """
        # Do not look further than the maximum allowed depth
        if current_depth > self.max_depth:
            return None

        if currentBoard.isSolved():
            return currentBoard.get_path()

        # Call the function recursively on all new boards
        for newBoard in currentBoard.moves():
            solution = self.dfs(newBoard, current_depth + 1)
            if solution:
                return solution

        return None
