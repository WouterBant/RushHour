from typing import Optional, List
from ..classes.board import Board


class IterativeDeepening:

    def __init__(self, startBoard: Board) -> None:
        self.startBoard = startBoard
        self.currentMaxDepth = 0
        self.solution = None

    def DepthFirstSearch(self, currentBoard: Board, currentDepth) -> Optional[list[Board]]:
        if currentDepth > self.currentMaxDepth:
            return None

        if currentBoard.isSolved():
            return currentBoard.get_path()

        for newBoard in currentBoard.moves():
            solution = self.DepthFirstSearch(newBoard, currentDepth + 1)
            if solution:
                return solution

        return None

    def run(self):  ## Memory efficient and finds best solution, but extremely slow.
        """Does a dfs with increasing depths, returns the path if a solution is found"""
        while not self.solution:
            self.currentMaxDepth += 1
            self.solution = self.DepthFirstSearch(self.startBoard, 0)
            print(self.currentMaxDepth)
        return self.solution
