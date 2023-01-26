from ..classes.board import Board
from .breadth_first import BreadthFirst
from .random_find import RandomFind
from collections import deque, defaultdict


class ShortenedPathRandom(BreadthFirst, RandomFind):
    """
    Runs path compression on batches of size batch_size. Path compression is also used
    on a collection of the compressed paths from each batch. This is done to minimize the total
    number of boards Breadth First has to look at, but still making use of the
    information provided about the solution by the different random searches.
    """

    def __init__(self, startBoard: Board, batch_size: int, number_batches: int) -> None:
        self.batch_size = batch_size
        self.number_batches = number_batches
        self.adj = None
        BreadthFirst.__init__(self, startBoard)  # Find shortest path with bfs
        RandomFind.__init__(self, startBoard)

    def availableMoves(self, currentBoard: Board) -> set[Board]:
        """Returns all available moves for the current board."""
        return self.adj[currentBoard]

    def handleNewBoard(self, newBoard: Board, currentBoard: Board) -> None:
        """Adds the new board to the visit set and the queue. Also updates its parent."""
        self.visit.add(newBoard)
        self.q.append(newBoard)
        newBoard.parentBoard = currentBoard  # Path compression happens here

    def reset(self) -> None:
        """Makes the queue and visit set of breadth first are ready to be used again."""
        self.visit = {self.startBoard}
        self.q = deque([self.startBoard])

    def run(self) -> list[Board]:
        """Runs path compression on the random found solutions."""
        adj_batches = defaultdict(set)  # Maps parents to children for the compressed paths
        for batch in range(self.number_batches):
            adj_batch = defaultdict(set)
            for _ in range(self.batch_size):
                path = self.runRandom()  # Get a random solution

                # Map all parents to their child(s) for the current iteration
                adj_batch[self.startBoard].add(path[0])
                for parent, child in zip(path, path[1:]):
                    adj_batch[parent].add(child)

            # Compress the paths found in this batch
            self.adj = adj_batch  # Used to get available moves
            path_compressed: list[Board] = self.runBF()
            print(f"Length compressed from batch {batch+1}: {len(path_compressed)}")

            # From the compressed path also map the parents to their child
            adj_batches[path_compressed[0].parentBoard].add(path_compressed[0])
            for parent, child in zip(path_compressed, path_compressed[1:]):
                adj_batches[parent].add(child)

        self.adj = adj_batches  # Used to get available moves
        return self.runBF()  # Return the path compression of the already compressed paths
