from rushhour import RushHour
from board import Board

import collections
import time
from sys import argv
import random
import copy


def randomFind(board):
    path = []
    count = 0
    while not board.isSolved():
        # print(board)
        board = Board(board.randomMove())
        # print(board)
        path.append(board)
        # if count % 100000 == 0:
        #     print(board)
        count += 1
        if count % 10000 == 0:
            print(board)
        # if len(path) == 4:
        #     # for i in path:
        #     #     print(i)
        #     return
        # time.sleep(1)
    return path


def breadth_first_search(board, max_depth=100):
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
                # q.append(path + [Board(newBoard)])
                copyPath = copy.deepcopy(path)
                copyPath.append(Board(newBoard))
                q.append(copyPath)
        depth += 1
        print(depth)
        # if depth == 4:
        #     for i in q[0]:
        #         print(i)
        #     return
        # print(len(q[0]))


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
    # print(startBoard)
    # random.seed(471)
    
    path, run_time = runAlgorithm(startBoard, breadth_first_search)
    # print(len(path))
    for i in path:
        print(i)
    # for i in path:
    #     time.sleep(1)
    #     print(i)
    # for board in path:
    #     print(board)