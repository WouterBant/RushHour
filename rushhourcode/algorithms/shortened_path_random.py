from ..classes.board import Board
from typing import List
from collections import deque, defaultdict
from .random_find import RandomFind


class ShortenedPathRandom(RandomFind):

    def __init__(self, startBoard: Board, batch_size: int, number_batches: int) -> None:
        self.batch_size = batch_size
        self.number_batches = number_batches

        RandomFind.__init__(self, startBoard)

    def run(self):
        adj_batches = defaultdict(set)
        for batch in range(self.number_batches):
            adj_batch = defaultdict(set)
            for _ in range(self.batch_size):
                path = self.runRandom()
                print(len(path))
                adj_batch[self.startBoard].add(path[0])
                for parent, child in zip(path, path[1:]):
                    adj_batch[parent].add(child)
            path_compressed = self.get_shortest_path(adj_batch)
            adj_batches[path_compressed[0].parentBoard].add(path_compressed[0])
            print(f"Length compressed from batch {batch+1}: {len(path_compressed)}")
            for parent, child in zip(path_compressed, path_compressed[1:]):
                adj_batches[parent].add(child)
        return self.get_shortest_path(adj_batches)

    def get_shortest_path(self, adj):
        visit = set()
        visit.add(self.startBoard)
        q = deque([self.startBoard])
        depth = 0
        while q:
            for _ in range(len(q)):
                currentBoard = q.popleft()

                # When the game is solved return the winning path
                if currentBoard.isSolved():
                    return currentBoard.get_path()

                # Check all moves that could be made and add the new board to the queue
                for newBoard in adj[currentBoard]:
                    # Check if you already have seen this board if so skip else add it to visit
                    if newBoard in visit:
                        continue
                    visit.add(newBoard)

                    q.append(newBoard)
                    newBoard.parentBoard = currentBoard  # Update the parent board
            depth += 1
