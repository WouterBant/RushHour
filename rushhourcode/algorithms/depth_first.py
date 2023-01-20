from ..classes.board import Board
from typing import Optional


class DepthFirst:

    def __init__(self, startBoard: Board, maxDepth: int) -> None:
        self.startBoard = startBoard
        self.maxDepth = maxDepth

    def dfs(self, currentBoard: Board, currentDepth: int)-> Optional[list[Board]]:
        if currentDepth > self.maxDepth:
            return None

        if currentBoard.isSolved():
            return currentBoard.get_path()

        for newBoard in currentBoard.moves():
            solution = self.dfs(newBoard, currentDepth + 1)
            if solution:
                return solution

        return None
