from ..classes.board import Board
from typing import List


def random_find(board: Board) -> List[Board]:
    """Tries random moves till a solution is found."""
    path = []
    while not board.isSolved():
        board = board.randomMove()
        path.append(board)
    return path
