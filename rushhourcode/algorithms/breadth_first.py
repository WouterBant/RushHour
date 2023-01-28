from ..classes.board import Board
from typing import Deque
from collections import deque
import sys


class BreadthFirst:
    """
    Looks at all possible boards at a the current depth before moving to the next depth.
    This guarantees it will find the minimum number of steps necessary to solve the board.
    """

    def __init__(self, startBoard: Board, display: bool = False) -> None:
        self.startBoard = startBoard
        self.visit = {startBoard}
        self.q: Deque[Board] = deque([startBoard])
        self.depth = 0
        self.display_bfs = display

    def availableMoves(self, currentBoard: Board) -> list[Board]:
        """Returns all available moves for the current board."""
        return currentBoard.moves()

    def handleNewBoard(self, newBoard: Board, currentBoard: Board) -> None:
        """Adds the new board to the visit set and the queue. Current board not used here."""
        self.visit.add(newBoard)
        self.q.append(newBoard)

    def reset(self) -> None:
        """Not necessary here but is used when used multiple times (shortened path random)."""
        pass

    def runBF(self) -> list[Board]:
        """Tries every possible move at every board, does not look at the same board twice."""
        while self.q:
            for _ in range(len(self.q)):
                currentBoard = self.q.popleft()

                # When the game is solved return the winning path
                if currentBoard.isSolved():
                    self.reset()
                    return currentBoard.get_path()

                # Check all moves that could be made and add the new board to the queue
                for newBoard in self.availableMoves(currentBoard):
                    # Check if you already have seen this board if so skip else add it to visit
                    if newBoard in self.visit:
                        continue
                    self.handleNewBoard(newBoard, currentBoard)

            if self.display_bfs:
                print(f"No solution found at depth {self.depth}.\n")
            self.depth += 1

        print("\nNo solution, try different parameters.")
        sys.exit()
