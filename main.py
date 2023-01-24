from rushhourcode.classes import board, rushhour
from rushhourcode.algorithms import breadth_first as bf
from rushhourcode.algorithms import iterative_deepening as iter
from rushhourcode.algorithms import random_find as randomF
from rushhourcode.algorithms import heuristic as heur
from rushhourcode.algorithms import shortened_path_random as shortRandom
from rushhourcode.algorithms import beam

# from rushhourcode.visualization import visualize as vis
import time
import matplotlib.pyplot as plt
from sys import argv
from typing import Tuple, List


def checkArgs() -> Tuple[int, int, int]:
    """
    Checks if the arguments given are correct, returns them as integers if that is the case.
    """
    sizes = {0: 6, 1: 6, 2: 6, 3: 6, 4: 9, 5: 9, 6: 9, 7: 12}

    # Check number of arguments
    if len(argv) != 3:
        print("Usage: python main.py [board (0-7)] [algorithm number (-1-5)]")
        exit(1)

    # Check type of arguments
    try:
        board, algorithm = int(argv[1]), int(argv[2])
    except ValueError:
        print("board and algorithm should be integers in the range 0-7 and -1-5, respectively.")
        exit(2)

    # Check if the argument is a valid number
    if board not in range(8) or algorithm not in range(-1, 8):
        print("board and algorithm should be integers in the range 0-7 and -1-5, respectively.")
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
    Runs the desired algorithm on the desired board and returns a solution and the run time.
    """
    start_time = time.time()
    if algorithm == -1:
        number_of_steps = []
        for _ in range(100):
            path = randomF.random_find(startBoard)
            number_of_steps.append(len(path))
        plt.hist(number_of_steps)
        plt.xlabel("Number of steps")
        plt.ylabel("Frequency")
        plt.savefig("output/statistics.png")
    elif algorithm == 0:
        rand = randomF.RandomFind(startBoard)
        path = rand.runRandom()
    elif algorithm == 1:
        breadth = bf.BreadthFirst(startBoard)
        path = breadth.runBF()
    elif algorithm == 2:
        heuristic = heur.Heuristic1(startBoard)
        path = heuristic.run()
    elif algorithm == 3:
        iterativeDeep = iter.IterativeDeepening(startBoard, 0)
        path = iterativeDeep.run()
    elif algorithm == 4:
        beamSearch = beam.Beam(startBoard, 8)
        path = beamSearch.run()
    elif algorithm == 5:
        comprRand = shortRandom.ShortenedPathRandom(startBoard, 10, 3)
        path = comprRand.run()
    elif algorithm == 6:
        heuristic = heur.Heuristic2(startBoard)
        path = heuristic.run()
    elif algorithm == 7:
        heuristic = heur.Heuristic3(startBoard)
        path = heuristic.run()
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

    if algorithm == -1:
        algorithm_name = "Sample"
    elif algorithm == 0:
        algorithm_name = "Random Find"
    elif algorithm == 1:
        algorithm_name = "Breadth First Search"
    elif algorithm == 2:
        algorithm_name = "Heuristic 1"
    elif algorithm == 3:
        algorithm_name = "Iterative Deepening"
    elif algorithm == 4:
        algorithm_name = "Beam Search"
    elif algorithm == 5:
        algorithm_name = "Shortened Path Random"
    elif algorithm == 6:
        algorithm_name = "Heuristic 2"
    elif algorithm == 7:
        algorithm_name = "Heuristic 3"
    print(f"The board was solved with {algorithm_name} in {len(moves)} steps and {run_time} seconds.")


if __name__ == "__main__":
    board_number, algorithm, size = checkArgs()
    file_name = get_file_name(board_number)
    game = rushhour.RushHour(file_name)
    startBoard = board.Board(game.cars, size)
    path, run_time = runAlgorithm(startBoard, algorithm)  # Probably better to do this in rushhour class
    display_results(game, path, run_time, algorithm)  # Probably better to do this in rushhour class

    """
    SUMMARY RESULTS:
    File 1: (0.1s, 21 steps, bfs)
    File 2: (0.2s, 15 steps, bfs), (0.05s, 15s, beam4)
    File 3: (0.3, 33 steps, bfs)
    File 4: (22s, 27 steps, bfs), (1.5s, 30 steps, beam4)
    File 5: (2.4s, 9031), (0.56s, 3062 steps), random, (18s, 47, heuristic3), (45s, 41, beam4), (22 steps and 1385.6623094081879 seconds bfs), (22 steps and 791.6342825889587 seconds heuristic 2)
    File 6: (0.23s, 1600), (0.12s, 449 steps), random, (16s, 52, heuristic3), (202s, 46, beam5), (18 steps and 448.25743222236633 seconds heuristic 2)
    File 7, (17s, 31539), (8.5s, 16454), random  -> beam in combination with heuristic3 probably good
    """
