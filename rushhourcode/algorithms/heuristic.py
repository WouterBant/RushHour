import heapq


def heuristic(board):
    visit = set()
    path = []
    q = []
    heapq.heappush(q, (0, path))

    while q:
        cost, path = heapq.heappop()
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
            heapq.heappush(q, (costNewBoard, copyPath + [newBoard]))


def costCalculator(board, movesMade):
    return movesMade
