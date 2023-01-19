from typing import Deque, List
from ..classes.board import Board
from collections import deque


def breadth_first_search(board: Board) -> List[Board]:
    """Tries every possible move at every board, does not look at the same board twice."""
    visit = set()
    q: Deque[Board] = deque([board])
    depth = 0

    while q:
        for _ in range(len(q)):
            currentBoard = q.popleft()

            # When the game is solved return the winning path
            if currentBoard.isSolved():
                return currentBoard.get_path()

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
