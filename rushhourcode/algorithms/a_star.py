# this is the a_star algorithm to solve a Rush hour puzzle
import heapq

class Node:
    """this is class with characteristics of a configuration of the puzzle board, represented as node."""

    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.red_car_row, self.red_car_col = self.calculate_coordinates_red_car()
        self.distance_from_begin = self.calculate_distance_from_begin()
        self.distance_to_goal = self.calculate_blocking_steps()

    def calculate_cost(self):
        cost = self.distance_from_begin + self.distance_to_goal
        return cost

    def calculate_coordinates_red_car(self):
        for row_idx, row in enumerate(self.board):
            for col_idx, col in enumerate(row):
                if col == 'X':
                    return row_idx, col_idx

    def calculate_distance_from_begin(self):
        if self.parent == None:
            return 0
        else:
            distance = self.parent.distance_from_begin + 1
            return distance

    def calculate_blocking_steps(self):
        length_position = self.red_car_row + 2
        blocked_steps = 0

        for col in self.board[self.red_car_row][length_position:]:
            if col != '.':
                blocked_steps = blocked_steps + 1

        return blocked_steps

    def __eq__(self, other):
        return self.calculate_cost() == other.calculate_cost()

    def __lt__(self, other):
        return self.calculate_cost() < other.calculate_cost()

    def __gt__(self, other):
        return self.calculate_cost() > other.calculate_cost()

class AStar:
    """comment"""

    def __init__(self, board):
        self.open = []
        heapq.heapify(self.open)
        self.closed = []
        self.start_board = board

    def a_star(self):
        pass



board = [['.','.','A','A','B','B'],
['C','C','.','D','D','H'],
['.','.','X','X','G','H'],
['E','E','F','F','G','H'],
['J','.','.','K','I','I'],
['J','.','.','K','L','L']]

star = AStar(board)
print(star.open)











