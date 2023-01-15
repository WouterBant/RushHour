from typing import Deque
from ..classes.board import Board
from collections import deque


def breadth_first_search(board: Board, max_depth: float = float("infinity")) -> list[Board]:
    """ Tries every possible move at every board, does not look at the same board twice. """
    visit = set()
    q: Deque[Board] = deque()
    q.append(board)
    depth = 0

    while q and depth <= max_depth:
        for _ in range(len(q)):
            currentBoard = q.popleft()

            # When the game is solved return the winning path
            if currentBoard.isSolved():
                path = []
                path.append(currentBoard)
                # Create the path by traversing back in the graph
                while currentBoard.parentBoard:
                    currentBoard = currentBoard.parentBoard
                    path.append(currentBoard)
                return path[::-1][1:]  # Order reversed since traversing is started at leaf board

            # Check all moves that could be made and add the new board to the queue
            for newBoard in currentBoard.moves():
                # Check if you already have seen this board if so skip else add it to visit
                if newBoard in visit:
                    continue
                visit.add(newBoard)
                q.append(newBoard)
        depth += 1
        print(depth)
    return [board]
