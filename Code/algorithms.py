import collections
import time

def random(board):
    path = [] 
    while not board.isSolved():
        board = board.randomMove()
        path.append(board)
    return path

def breadth_first_search(board, max_depth=float("infinity")):
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
                continue
            visit.add(currentBoard)

            # When the game is solved return the winning path
            if currentBoard.isSolved():
                return path
            
            # Check all moves that could be made and add the new board to the queue
            for newBoard in board.moves():
                copyPath = path[:]
                q.append(copyPath + [newBoard])
        depth += 1

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

def runAlgorithm(board, algorithm=random):
    start_time = time.time()
    path = algorithm(board)
    run_time = time.time() - start_time
    return path, run_time