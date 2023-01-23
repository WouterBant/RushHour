from ..classes.board import Board
from .depth_first import DepthFirst


class IterativeDeepening(DepthFirst):
    """
    Increments the maximum allowed depth and runs dfs with that depth.
    This is guaranteed to find the shortest solution since dfs will return a solution
    when the minimum number of steps required to solve the board is equal to the max depth.
    Memory efficient since only maxDepth boards are stored, but slow since starts searching
    again for each depth but than just till one layer deeper.
    """

    def __init__(self, startBoard: Board, maxDepth: int) -> None:
        self.solution = None
        DepthFirst.__init__(self, startBoard, maxDepth)

    def run(self) -> list[Board]:
        """Does a dfs with increasing depths, returns the path if a solution is found"""
        while not self.solution:
            self.maxDepth += 1  # Look one depth deeper
            self.solution = self.dfs(self.startBoard, current_depth=0)
            # print(self.maxDepth)
        return self.solution
