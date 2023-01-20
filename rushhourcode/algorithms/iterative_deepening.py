from typing import Optional, List
from ..classes.board import Board
from .depth_first import DepthFirst


class IterativeDeepening(DepthFirst):

    def __init__(self, startBoard: Board, maxDepth: int) -> None:
        self.solution = None

        DepthFirst.__init__(self, startBoard, maxDepth)

    def run(self) -> list[Board]:  ## Memory efficient and finds best solution, but extremely slow.
        """Does a dfs with increasing depths, returns the path if a solution is found"""
        while not self.solution:
            self.maxDepth += 1
            self.solution = self.dfs(self.startBoard, 0)
            print(self.maxDepth)
        return self.solution
