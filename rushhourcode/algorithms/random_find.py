from ..classes.board import Board
from typing import List


class RandomFind:
    """Tries random moves till a solution is found."""

    def __init__(self, startBoard: Board) -> None:
        self.startBoard = startBoard

    def runRandom(self) -> List[Board]:
        path = []
        board = self.startBoard
        while not board.isSolved():
            board = board.randomMove()
            path.append(board)
        return path
