from ..classes.board import Board
from typing import Optional


class DepthFirst:
    """
    Tries to find a solution in a depth first manner with recursion. When the maximum depth
    is less than the least number of required steps, no solution will be found.
    """

    def __init__(self, startBoard: Board, maxDepth: int) -> None:
        self.startBoard = startBoard
        self.maxDepth = maxDepth

    def dfs(self, currentBoard: Board, currentDepth: int) -> Optional[list[Board]]:
        """
        Returns a solution if the maximum depth >= to the minimum number of steps
        necessary to solve the board. Else returns None. This solution is only guaranteed
        to be optimal if maximum depth = minimum number of steps to solve the board.
        """
        # Do not look further than the maximum allowed depth
        if currentDepth > self.maxDepth:
            return None

        if currentBoard.isSolved():
            return currentBoard.get_path()

        # Call the function recursively on all new boards
        for newBoard in currentBoard.moves():
            solution = self.dfs(newBoard, currentDepth + 1)
            if solution:
                return solution

        return None
