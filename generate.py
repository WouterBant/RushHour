from rushhourcode.board_generator.board_generator import generate_board
from sys import argv 
from rushhourcode.classes.board import Board

def hill_climb(board: Board):
    change_board = board
    score = board.number_of_blocking_and_blocking_blocking_cars()
    print(score)
    for _ in range(100):
        change_board = change_board.randomMove()
        print(change_board)
        score = change_board.number_of_blocking_and_blocking_blocking_cars()
        print(score)



if __name__ == "__main__":
    if len(argv) != 4:
        print("Usage: generate.py [size] [tries] [shuffles]")
        exit(10)
    size, tries, shuffles = int(argv[1]), int(argv[2]), int(argv[3])
    board = generate_board(size=size, tries=tries, shuffles=shuffles)
    print(board)
    hill_climb(board)

