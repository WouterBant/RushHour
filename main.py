from rushhourcode.classes import board, rushhour
from rushhourcode.algorithms import breadth_first as bf
from rushhourcode.algorithms import iterative_deepening as iter
from rushhourcode.algorithms import random_find as randomF
from rushhourcode.algorithms import astar_v_wouter as astar
from rushhourcode.algorithms import shortened_path_random as shortRandom
from rushhourcode.algorithms import beam
# from rushhourcode.visualization import visualize as vis

import argparse
import time
from sys import argv
from typing import Tuple, List
import os
import sys


def checkArgs() -> argparse.Namespace:
    """
    Checks if the arguments given are correct, returns them if it is the case.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", type=int, help="The algorithm number, always required.")
    parser.add_argument("board_number", type=int, help="The board number, only required when -r is not given.")
    parser.add_argument("-r", "--random", help="Generate and solve a random board.", action='store_true')
    parser.add_argument("-d", "--display", help="Generate and solve a random board.", action='store_true')
    parser.add_argument("-v", "--visualize", help="Visualize the solution.", action='store_true')

    # Parse the arguments
    args = parser.parse_args()

    # Check if an algorithm is given
    if not args.algorithm:
        print("Indicate the desired algorithm.")
        print("Example usage: python main.py (0-8) (0-7) [-v]")
        sys.exit(1)

    # Check if both the board number and the random board flag are given
    if args.board_number and args.random:
        print("Do not use -r flag in combination with board number.")
        print("Usage with board number: python main.py (0-8) (0-7) [-v]")
        print("Usage with -r flag: python main.py (0-8) -r [-v]")
        sys.exit(2)
    
    # Check if algorithm is valid
    if args.algorithm not in range(-1, 8):
        print("Algorithm should be between 0 and 8.")
        print("Example usage: python main.py (0-8) (0-7) [-v]")
        sys.exit(3)

    # Check when board number is given if it is valid
    if args.board_number and args.board_number not in range(8):
        print("Board number should be between 0 and 8.")
        print("Example usage: python main.py (0-8) (0-7) [-v]")
        print("Or use a random board: python main.py (0-8) -r [-v]")
        sys.exit(4)

    return args


def get_file_name_and_size(board_number: int) -> str:
    """Based on the number entered by the user returns the corresponding file."""
    if board_number in range(4):
        return (f"gameboards/Rushhour6x6_{board_number}.csv", 6)
    elif board_number in range(4, 7):
        return (f"gameboards/Rushhour9x9_{board_number}.csv", 9)
    else:
        return ("gameboards/Rushhour12x12_7.csv", 12)


def runAlgorithm(startBoard: board.Board, algorithm: int, display: bool) -> Tuple[List[board.Board], float, str]:
    """
    Runs the desired algorithm on the desired board and returns a solution and the run time.
    """
    start_time = time.time()

    if algorithm == 0:
        algo = randomF.RandomFind(startBoard)
        algorithm_name = "Random Find"
        path = algo.runRandom()
    elif algorithm == 1:
        algo = bf.BreadthFirst(startBoard, display=display)
        algorithm_name = "Breadth First Search"
        path = algo.runBF()
    elif algorithm == 2:
        algo = astar.AStar1(startBoard, display=display)
        algorithm_name = "AStar 1"
        path = algo.run()
    elif algorithm == 3:
        algo = iter.IterativeDeepening(startBoard, start_max_depth=0, display=display)
        algorithm_name = "Iterative Deepening"
        path = algo.run()
    elif algorithm == 4:
        algo = beam.Beam(startBoard, nodes_to_expand=8)
        algorithm_name = "Beam Search"
        path = algo.run()
    elif algorithm == 5:
        algo = shortRandom.ShortenedPathRandom(startBoard, batch_size=10, number_batches=3)
        algorithm_name = "Shortened Path Random"
        path = algo.run()
    elif algorithm == 6:
        algo = astar.AStar2(startBoard)
        algorithm_name = "AStar 2"
        path = algo.run()
    elif algorithm == 7:
        algo = astar.AStar3(startBoard)
        algorithm_name = "Moves Freed Heuristic"
        path = algo.run()

    run_time = time.time() - start_time

    return (path, run_time, algorithm_name)

def output_results(game: rushhour.RushHour, path: List[board.Board]):
    """Stores the solution moves in output/output.csv and the boards in output/boards_output.csv"""
    moves = [board.move for board in path]
    game.output_path(moves)
    game.output_boards(path)

if __name__ == "__main__":
    args = checkArgs()
    if args.board_number:
        file_name, size = get_file_name_and_size(args.board_number)
        game = rushhour.RushHour(file_name)
        startBoard = board.Board(game.cars, size)
        path, run_time, algorithm_name = runAlgorithm(startBoard, args.algorithm, args.display)
        output_results(game, path)
        print(f"Board {args.board_number} was solved with {algorithm_name} in {len(path)} steps and {run_time} seconds.")
    if args.visualize:
        os.system("python rushhourcode/visualization/visualize.py")

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
