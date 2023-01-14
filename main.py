from rushhourcode.classes import board, car, rushhour
from rushhourcode.algorithms import breadth_first_search as bfs
from rushhourcode.algorithms import random_find as randomF
from rushhourcode.visualization import visualize as vis

import time
from sys import argv

def runAlgorithm(startBoard, algo=1):
    start_time = time.time()
    if algo == 1:
        path = randomF.random_find(startBoard)
    elif algo == 2:
        path = bfs.breadth_first_search(startBoard)
    run_time = time.time() - start_time
    return path, run_time

if __name__ == "__main__":
    if len(argv) < 2:  # Fix this and check if range good
        print("Usage: python main.py [filename] [algorithm number]")
        exit(1)
    gamename = f"gameboards/{argv[1]}.csv"  # Fix this such that a single number is enough
    game = rushhour.RushHour(gamename)
    startBoard = board.Board(game.cars)
    
    path, run_time = runAlgorithm(startBoard, int(argv[2]))
    if len(path) > 25:
        print(len(path))
    else:
        for i in path:
            time.sleep(1)
            print(i)
    moves = [board.move for board in path]
    game.output(moves)
    print(f"The board was solved in {len(moves)} steps and {run_time} seconds.")
    
    ### SUMMARY RESULTS:
    # File 1: 0.5s, 21 steps, bfs
    # File 2: 1.2s, 15 steps, bfs
    # File 3: 3.0s, 33 steps, bfs
    # File 4: 220s, 27 steps, 2.2GB, bfs
    # File 5: (24s, 9031), (5.6s, 3062 steps), random
    # File 6: (100s, 10734), (1.2s, 449 steps), random
    # File 7, (227s, 31539), random
