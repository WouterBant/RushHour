from typing import Optional, List
from ..classes.board import Board


def iterative_deepening(board: Board):  ## Memory efficient and finds best solution, but extremely slow.
    """Does a dfs with increasing depths, returns the path if a solution is found"""
    max_depth = 0
    while True:
        max_depth += 1
        solution = depth_first_search(board, 0, max_depth)
        print(max_depth)
        if solution:
            return solution

def depth_first_search(currentBoard: Board, current_depth=0, max_depth=500) -> Optional[list[Board]]:
    if current_depth > max_depth:
        return None

    if currentBoard.isSolved():
        path = []
        path.append(currentBoard)
        # Create the path by traversing back in the graph
        while currentBoard.parentBoard:
            currentBoard = currentBoard.parentBoard
            path.append(currentBoard)
        return path[::-1][1:]

    for newBoard in currentBoard.moves():
        solution = depth_first_search(newBoard, current_depth + 1, max_depth)
        if solution:
            return solution
