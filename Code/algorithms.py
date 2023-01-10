import collections

def bfs(board):
    visit = set()
    path = []
    q = collections.deque()
    q.append(board)

    while q:
        board, path = q.popleft()
        if board.isSolved:
            for b in path:
                print(b)
            print(len(path))
            return path
        if path in visit:
            continue
        visit.add(path)
        for move in board.moves():
            path.append(move)
            q.append((move, path))
            path.remove(move)

def heuristic(board):
    visit = set()
    path = []
    q = collections.deque()  ## []
    q.append(board)  ## heapq.heappush(q, board)

    while q:
        board, path = q.popleft()  ## heapq.heappop(q)
        if board.isSolved:
            for b in path:
                print(b)
            return path
        if path in visit:
            continue
        visit.add(path)
        for move in board.moves():
            if move > board:  ## or make function that calculates or priorityQ
                path.append(move)
                q.append((move, path))  ## heapq.heappush(q, move)
                path.remove(move)
