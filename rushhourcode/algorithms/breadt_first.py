from typing import Deque, List
from ..classes.board import Board
from collections import deque


class BreadthFirst:

    def __init__(self, startBoard) -> None:
        self.visit = set()
        self.q: Deque[Board] = deque([startBoard])
        self.depth = 0
    
    def run(self) -> List[Board]:
        """Tries every possible move at every board, does not look at the same board twice."""        
        while self.q:
            for _ in range(len(self.q)):
                currentBoard = self.q.popleft()

                # When the game is solved return the winning path
                if currentBoard.isSolved():
                    return currentBoard.get_path()

                # Check all moves that could be made and add the new board to the queue
                for newBoard in currentBoard.moves():
                    # Check if you already have seen this board if so skip else add it to visit
                    if newBoard in self.visit:
                        continue
                    self.visit.add(newBoard)
                    self.q.append(newBoard)
            self.depth += 1
            print(self.depth)
        return [currentBoard]  # FIX THIS LATER, no solution found
