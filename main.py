from rushhourcode.classes import board, rushhour
from rushhourcode.algorithms import breadth_first_search as bfs
from rushhourcode.algorithms import iterative_deepening as iter
from rushhourcode.algorithms import random_find as randomF
from rushhourcode.algorithms import heuristic as heur

# from rushhourcode.visualization import visualize as vis
import time
import matplotlib.pyplot as plt
from sys import argv
from typing import Tuple, List


def checkArgs() -> Tuple[int, int, int]:
    """
    Checks if the arguments given are correct, returns them as integers if that is the case.
    """
    # Check number of arguments
    sizes = {0: 6, 1: 6, 2: 6, 3: 6, 4: 9, 5: 9, 6: 9, 7: 12}

    if len(argv) != 3:
        print("Usage: python main.py [board (0-7)] [algorithm number (0-1)]")
        exit(1)

    # Check type of arguments
    try:
        board, algorithm = int(argv[1]), int(argv[2])
    except ValueError:
        print(
            "board and algorithm should be integers in the range 0-7 and 0-1, respectively."
        )
        exit(2)

    # Check if the argument is a valid number
    if board not in range(8) or algorithm not in range(-1, 5):
        print("board and algorithm should be integers in the range 0-7 and 0-1, respectively.")
        exit(3)

    size = sizes[board]

    # When arguments valid return them
    return (board, algorithm, size)


def get_file_name(board_number: int) -> str:
    """Based on the number entered by the user returns the corresponding file."""
    if board_number in range(4):
        return f"gameboards/Rushhour6x6_{board_number}.csv"
    elif board_number in range(4, 7):
        return f"gameboards/Rushhour9x9_{board_number}.csv"
    else:
        return "gameboards/Rushhour12x12_7.csv"


def runAlgorithm(startBoard: board.Board, algorithm: int) -> Tuple[List[board.Board], float]:
    """
    Runs the desired algorithm on the desired board and returns a solution and  the run time.
    """
    start_time = time.time()
    if algorithm == -1:
        number_of_steps = []
        for _ in range(1000):
            path = randomF.random_find(startBoard)
            number_of_steps.append(len(path))
        plt.hist(number_of_steps)
        plt.xlabel("Number of steps")
        plt.ylabel("Frequency")
        plt.savefig("output/statistics.png")
    elif algorithm == 0:
        path = randomF.random_find(startBoard)
    elif algorithm == 1:
        path = bfs.breadth_first_search(startBoard)
    elif algorithm == 2:
        path = heur.heuristic(startBoard)
    elif algorithm == 3:
        path = iter.iterative_deepening(startBoard)
    elif algorithm == 4:
        path = iter.depth_first_search(startBoard)
    run_time = time.time() - start_time
    return (path, run_time)


def display_results(game: rushhour.RushHour, path: List[board.Board], run_time: float, algorithm: int) -> None:
    """Displays the solution and outputs the moves to the output file and shows run time and steps."""
    # if len(path) <= 25:
    #     for i in path:
    #         print(i)
    #         time.sleep(1)
    moves = [board.move for board in path]
    game.output_path(moves)
    game.output_boards(path)
    # match algorithm:
    #     case 0:
    #         algorithm_name = "Random Find"
    #     case 1:
    #         algorithm_name = "Breadth First Search"
    #     case 2:
    #         algorithm_name = "Heuristic"
    if algorithm == -1:
        algorithm_name = "Sample"
    elif algorithm == 0:
        algorithm_name = "Random Find"
    elif algorithm == 1:
        algorithm_name = "Breadth First Search"
    elif algorithm == 2:
        algorithm_name = "Heuristic"
    elif algorithm == 3:
        algorithm_name = "Iterative Deepening"
    elif algorithm == 4:
        algorithm_name = "Depth First Search"
    print(f"The board was solved with {algorithm_name} in {len(moves)} steps and {run_time} seconds.")


if __name__ == "__main__":
    board_number, algorithm, size = checkArgs()
    file_name = get_file_name(board_number)
    game = rushhour.RushHour(file_name)
    startBoard = board.Board(game.cars, size)
    path, run_time = runAlgorithm(
        startBoard, algorithm
    )  # Probably better to do this in rushhour class
    display_results(
        game, path, run_time, algorithm
    )  # Probably better to do this in rushhour class

    """
    SUMMARY RESULTS:
    File 1: 0.5s, 21 steps, bfs
    File 2: 1.2s, 15 steps, bfs
    File 3: 3.0s, 33 steps, bfs
    File 4: 220s, 27 steps, 2.2GB, bfs
    File 5: (24s, 9031), (5.6s, 3062 steps), random
    File 6: (100s, 10734), (1.2s, 449 steps), random
    File 7, (227s, 31539), random
    """
