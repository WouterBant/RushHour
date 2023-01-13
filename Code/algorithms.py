from rushhour import RushHour
from board import Board

import collections
import time
from sys import argv
import copy


def randomFind(board: Board) -> list[Board]:
    """ Tries random moves till a solution is found. """
    path = []
    while not board.isSolved():
        board = Board(board.randomMove())
        path.append(board)
    return path


def breadth_first_search(board, max_depth=100):
    """ Tries every possible move at every board, does not look at the same board twice. """
    visit = set()
    path = [board]
    q = collections.deque()
    q.append(path)
    depth = 0

    while q and depth <= max_depth:
        for _ in range(len(q)):
            path = q.popleft()
            currentBoard = path[-1]

            # Check if you already have seen this board if so skip else add it to visit
            if currentBoard in visit:
                print("hi")
                continue
            visit.add(currentBoard)

            # When the game is solved return the winning path
            if currentBoard.isSolved():
                return path

            # Check all moves that could be made and add the new board to the queue
            for newBoard in currentBoard.moves():
                copyPath = copy.deepcopy(path)
                copyPath.append(Board(newBoard))
                q.append(copyPath)
        depth += 1
        print(depth)


def heuristic(board):
    visit = set()
    path = []
    q = []
    collections.heapq.heappush(q, (0, path))

    while q:
        cost, path = collections.heapq.heappop()
        currentBoard = path[-1]

        # Check if you already have seen this board if so skip else add it to visit
        if currentBoard in visit:
            print("hi")
            continue
        visit.add(currentBoard)

        # When the game is solved return the winning path
        if currentBoard.isSolved():
            return path

        # Check all moves that could be made and add the new board to the PriorityQueue
        for newBoard in board.moves():
            copyPath = path[:]
            costNewBoard = costCalculator(newBoard, len(path))
            collections.heapq.heappush(q, (costNewBoard, copyPath + [newBoard]))


def costCalculator(board, movesMade):
    return movesMade


def runAlgorithm(board, algorithm=randomFind):
    start_time = time.time()
    path = algorithm(board)
    run_time = time.time() - start_time
    return path, run_time


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python rushhour.py [filename]")
        exit(1)
    gamename = f"gameboards/{argv[1]}.csv"
    game = RushHour(gamename)
    startBoard = Board(game.cars)
    
    path, run_time = runAlgorithm(startBoard, randomFind)
    if len(path) > 20:
        print(len(path))
    else:
        for i in path:
            time.sleep(1)
            print(i)
    print(f"The runtime was: {run_time} seconds")