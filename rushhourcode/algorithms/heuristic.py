from ..classes.board import Board
import heapq
from typing import List, Tuple


class heuristic1:

    def __init__(self, board: Board) -> None:
        self.startBoard = board
        self.visit = set()
        self.pq: List[Tuple[float, int, Board]] = []
        heapq.heappush(self.pq, (0, 0, board))

    def costCalculator(self, board: Board) -> int:  # Admissable
        return board.number_blocking_cars()

    def run(self):
        while self.pq:
            cost, depth, currentBoard = heapq.heappop(self.pq)

            # When the game is solved return the winning path
            if currentBoard.isSolved():
                return currentBoard.get_path()

            # Check all moves that could be made and add the new board to the Priority Queue, ALSO THIS VERY MUCH THE SAME AS FOR BFS
            for newBoard in currentBoard.moves():
                # Check if you already have seen this board if so skip else add it to visit and Priority Queue
                if newBoard in self.visit:
                    continue
                self.visit.add(newBoard)
                
                costNewBoard = self.costCalculator(newBoard) + depth
                heapq.heappush(self.pq, (costNewBoard, depth+1, newBoard))
        
        return [self.startBoard]  ## CHANGE THIS LATER


class heuristic2(heuristic1):

    def costCalculator(self, board: Board) -> int:  # Admissable
        return board.number_of_blocking_and_blocking_blocking_cars()


class heuristic3(heuristic1):

    def costCalculator(self, board: Board) -> int:  # Board 4 6
        return 3*board.exit_distance() + 3*board.number_blocking_cars() - 14*board.moves_created()
