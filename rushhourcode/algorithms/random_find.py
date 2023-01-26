from ..classes.board import Board


class RandomFind:
    """Tries random moves till a solution is found."""

    def __init__(self, startBoard: Board) -> None:
        self.startBoard = startBoard

    def runRandom(self) -> list[Board]:
        """Finds and returns the path to a solution."""
        path, board = [], self.startBoard
        while not board.isSolved():
            board = board.randomMove()
            path.append(board)
        return path
