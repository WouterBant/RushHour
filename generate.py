from rushhourcode.board_generator.board_generator import generate_board
from sys import argv 
from rushhourcode.classes.board import Board

def hill_climb(board: Board):
    current_best = board
    score = board.number_of_blocking_and_blocking_blocking_cars()
    difference = -1
    while difference != 0:
        for move in current_best.moves():
            test_score = move.number_of_blocking_and_blocking_blocking_cars()
            difference = test_score - score
            if test_score > score:
                score = test_score 
                current_best = move
    print(current_best)



if __name__ == "__main__":
    if len(argv) != 4:
        print("Usage: generate.py [size] [tries] [shuffles]")
        exit(10)
    size, tries, shuffles = int(argv[1]), int(argv[2]), int(argv[3])
    board = generate_board(size=size, tries=tries, shuffles=shuffles)
    print(board)
    hill_climb(board)

