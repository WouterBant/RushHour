# from classes.board import Board
from ..classes.board import Board


def random_find(board: Board) -> list[Board]:
    """ Tries random moves till a solution is found. """
    path = []
    while not board.isSolved():
        board = board.randomMove()
        path.append(board)
    return path