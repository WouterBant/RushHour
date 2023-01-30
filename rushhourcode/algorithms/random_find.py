from ..classes.board import Board


class RandomFind:
    """Tries random moves till a solution is found."""

    def __init__(self, startBoard: Board, display: bool = False) -> None:
        self.startBoard = startBoard
        self.displayRandom = display
        self.count_to_display = 0

    def runRandom(self) -> list[Board]:
        """Finds and returns the path to a solution."""
        path, board = [], self.startBoard
        while not board.isSolved():
            board = board.randomMove()
            path.append(board)

            self.count_to_display += 1
            if self.displayRandom and self.count_to_display % 1000 == 0:
                print(f"\n{len(path)} boards visited, still looking for a solution ...")
        return path
