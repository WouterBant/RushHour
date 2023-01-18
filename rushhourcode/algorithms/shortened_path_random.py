from ..classes.board import Board
from typing import List


def shortened_path_random_find(board: Board) -> List[Board]:
    """Tries random moves till a solution is found. Shortens the found path."""
    while not board.isSolved():
        board = board.randomMove()

    child_dic = {}
    child_dic[board] = -1  # The last board does not have a child
    while board.parentBoard:
        parent = board.parentBoard
        if parent in child_dic:  # Shorten path here
            newChild = child_dic[parent]
            child_dic[parent] = newChild
        else:
            child_dic[parent] = board
        board = board.parentBoard
    path = []
    while board in child_dic:
        path.append(board)
        board = child_dic[board]
    return path[1:]
