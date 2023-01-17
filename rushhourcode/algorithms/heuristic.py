from ..classes.board import Board
import heapq


def heuristic(board: Board) -> list[Board]:
    """
    Uses a Priority Queue to determine which boards to look at, returns a solution when found.
    """
    visit = set()
    pq: list[tuple[float, int, Board]] = []
    heapq.heappush(pq, (0, 0, board))
    while pq:
        cost, depth, currentBoard = heapq.heappop(pq)

        # When the game is solved return the winning path, THIS IS BAD SINCE IT IS THE SAME AS FOR BFS
        if currentBoard.isSolved():
            if currentBoard.isSolved():
                path = []
                path.append(currentBoard)
                # Create the path by traversing back in the graph
                while currentBoard.parentBoard:
                    currentBoard = currentBoard.parentBoard
                    path.append(currentBoard)
                return path[::-1][1:]  # Order reversed since traversing is started at leaf board

        # Check all moves that could be made and add the new board to the Priority Queue, ALSO THIS VERY MUCH THE SAME AS FOR BFS
        for newBoard in currentBoard.moves():
            # Check if you already have seen this board if so skip else add it to visit
            if newBoard in visit:
                continue
            visit.add(newBoard)
            costNewBoard = costCalculator(newBoard, depth)
            heapq.heappush(pq, (costNewBoard, depth, newBoard))
    return [board]

# def costCalculator(board: Board, movesMade: int) -> float:
#     return -board.moves_created()

def costCalculator(board: Board, movesMade: int) -> float:  #Board 4 6
    dist = board.exit_distance()
    blocks = board.number_blocking_cars()
    moves_created = board.moves_created()
    return 3*dist + 3*blocks + movesMade - 14*moves_created

# def costCalculator(board: Board, movesMade: int) -> float:
#     ## when these methods are used together, improvements in the methods is easy
#     dist = board.exit_distance()
#     blocks = board.number_blocking_cars()
#     blocked_blockers = board.number_blocking_cars_blocked()  ## so these are not able to move out of the way yet
#     moves_created = board.moves_created()
#     return 7*dist + 15*blocks + movesMade + 5*moves_created

# def costCalculator(board: Board, movesMade: int) -> float:
#     blocks = board.number_blocking_cars()
#     blockedBlockers = board.number_blocking_cars_blocked()
#     return blocks+blockedBlockers