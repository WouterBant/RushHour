import collections

def bfs(board):
    visit = set()
    path = []
    q = collections.deque()
    q.append((board, path))

    while q:
        board, path = q.popleft()
        if board.isSolved:
            for b in path:
                print(b)
            print(len(path))
            return path
        if board in visit:
            continue
        visit.add(board)
        for move in board.moves():
            path.append(move)
            q.append((move, path))
            path.remove(move)

def heuristic(board):
    visit = set()
    path = []
    q = []
    collections.heapq.heappush(q, (board, path))

    while q:
        board, path = collections.heapq.heappop()
        if board.isSolved:
            for b in path:
                print(b)
            return path
        if path in visit:
            continue
        visit.add(path)
        for move in board.moves():
            if move > board:  ## or make function that calculates
                path.append(move)
                collections.heapq.heappush(q, (move, path))
                path.remove(move)
