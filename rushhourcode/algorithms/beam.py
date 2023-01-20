from typing import Optional
from ..classes.board import Board
from .breadth_first import BreadthFirst

class Beam(BreadthFirst):
    """Only looks at a fixed number of next states. Is not guaranteed to return a solution."""

    def __init__(self, startBoard, nodesToExpand: int) -> None:
        self.nodesToExpand = nodesToExpand

        BreadthFirst.__init__(self, startBoard)

    def availableMoves(self, currentBoard: Board) -> list[Board]:
        """Returns all available moves for the current board."""
        possible_moves = currentBoard.moves()
        if len(possible_moves) <= self.nodesToExpand:
            return possible_moves
        return sorted(possible_moves, key=lambda x: self.compute_cost(x))[:self.nodesToExpand]
        
    def compute_cost(self, board: Board) -> int:
        return board.number_of_blocking_and_blocking_blocking_cars()

    def run(self) -> Optional[list[Board]]:
        return self.runBF()

    