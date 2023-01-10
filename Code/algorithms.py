import collections

def bfs(board):
    visit = set()
    path = [board]
    q = collections.deque()
    q.append(path)

    # As long as you have not found and there are unvisited configurations
    while q:
        path = q.popleft()
        currentBoard = path[-1]

        # Check if you already have seen this board if so skip else add it to visit
        if currentBoard in visit:
            continue
        visit.add(board)

        # When the game is solved return the winning path
        if currentBoard.isSolved():
            return path
        
        # Check all moves that could be made and add the new board to the queue
        for newBoard in board.moves():
            copyPath = path[:]
            q.append(copyPath + [newBoard])

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

def costCalculator(board, steps_taken):
    return steps_taken
