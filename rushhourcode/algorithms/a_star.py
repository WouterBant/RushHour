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
        self.calculate_cost()

    def calculate_cost(self):
        cost = self.distance_from_begin + self.distance_to_goal
        self.cost = cost
        return cost

    def calculate_coordinates_red_car(self):
        for row_idx, row in enumerate(self.board.board):
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

        for col in self.board.board[self.red_car_row][length_position:]:
            if col != '.':
                blocked_steps = blocked_steps + 1

        return blocked_steps

    def check_node_end(self):
        check_step = len(self.board.board[0]) - 2
        if self.red_car_col == check_step:
            return True
        return False

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

    def return_found_path(self, node):
        path = []
        # current node is the node passed in the function
        current_node = node
        # loop until current node is nothing
        while current_node is not None:
            # add current node's board to the path list
            path.append(current_node.board.board)
            # set the current node to its parent
            current_node = current_node.parent
        # return the path list as reversed
        return path[::-1]


    def a_star(self):
        first_node = Node(self.start_board, None)
        first_node.cost = 0
        # push the beginning node to the open list, because we start there
        heapq.heappush(self.open, first_node)

        # loop until we find the end node
        while len(self.open) > 0:
            # check current node by popping the node with the lowest self.cost
            current_node = heapq.heappop(self.open)
            self.closed.append(current_node)
            # check if the current node is our goal
            if current_node.check_node_end() == True:
                return self.return_found_path()

            # initialize empty list for the children of that current node
            children = []
            # check all moves that can be made and create nodes
            moves = current_node.board.moves()
            for move in moves:
                children.append(Node(move, current_node))

            

# board = [['.','.','A','A','B','B'],
# ['C','C','.','D','D','H'],
# ['.','.','X','X','G','H'],
# ['E','E','F','F','G','H'],
# ['J','.','.','K','I','I'],
# ['J','.','.','K','L','L']]
#
# star = AStar(board)
# star.a_star()














