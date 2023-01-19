from ..classes.board import Board
from typing import List
from collections import deque, defaultdict
import copy

def shortened_path_random_find(board: Board) -> List[Board]:
    """Tries random moves till a solution is found. Shortens the found path."""
    startBoard = board
    adj = defaultdict(set)

    for n in range(5):  # Solve it 5 times
        board = copy.deepcopy(startBoard)
        path = []
        path.append(startBoard)
        while not board.isSolved():
            board = board.randomMove()
            path.append(board)

        for par, child in zip(path, path[1:]):
            adj[par].add(child)
        print(f"Solved {n}")
        print(f"Pathlength: {len(path)}")

    # Do a bfs on the nodes retrieved from the n random solutions
    visit = set()
    visit.add(startBoard)
    q = deque([startBoard])
    depth = 0
    while q:
        for _ in range(len(q)):
            currentBoard = q.popleft()

            # When the game is solved return the winning path
            if currentBoard.isSolved():
                path = []
                path.append(currentBoard)
                # Create the path by traversing back in the graph
                while currentBoard.parentBoard:
                    currentBoard = currentBoard.parentBoard
                    path.append(currentBoard)
                return path[::-1][1:]  # Order reversed since traversing is started at leaf board

            # Check all moves that could be made and add the new board to the queue
            for newBoard in adj[currentBoard]:
                # Check if you already have seen this board if so skip else add it to visit
                if newBoard in visit:
                    continue
                visit.add(newBoard)
                q.append(newBoard)
                newBoard.parentBoard = currentBoard
        depth += 1
    return [board]
