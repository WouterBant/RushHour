from typing import Optional
from ..classes.board import Board
from .breadth_first import BreadthFirst


class Beam(BreadthFirst):
    """
    Runs breadth first search on a give number of next boards (nodes_to_expand). These boards are chosen on being most 
    promising. How promising a board is determined by the compute_cost method. This heuristic is not guaranteed to return 
    a solution and if it returns a solution it is not guaranteed to be the one with the least amount of steps.
    """

    def __init__(self, startBoard: Board, nodes_to_expand: int) -> None:
        self.nodes_to_expand = nodes_to_expand
        BreadthFirst.__init__(self, startBoard)

    def availableMoves(self, currentBoard: Board) -> list[Board]:
        """Returns the most promising boards that will be considered by breadth first search."""
        possible_moves = currentBoard.moves()
        if len(possible_moves) <= self.nodes_to_expand:
            return possible_moves
        return sorted(possible_moves, key=lambda x: self.compute_cost(x))[:self.nodes_to_expand]

    def compute_cost(self, board: Board) -> int:
        """Determines how promising a board is, boards with a higher cost are less promising."""
        return board.number_of_blocking_and_blocking_blocking_cars()

    def run(self) -> Optional[list[Board]]:
        return self.runBF()
