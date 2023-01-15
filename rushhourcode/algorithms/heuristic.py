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
        for newBoard in board.moves():
            # Check if you already have seen this board if so skip else add it to visit
            if newBoard in visit:
                continue
            visit.add(newBoard)
            costNewBoard = costCalculator(newBoard, depth)
            heapq.heappush(pq, (costNewBoard, depth, newBoard))
    return [board]


def costCalculator(board: Board, movesMade: int) -> float:
    return movesMade*0.9
