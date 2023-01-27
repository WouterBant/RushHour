# this is the a_star algorithm to solve a Rush hour puzzle

# two heuristics were tested: where cost were determined by the sum distance of the begin board as well as the end board
# and where the cost is determined by the cars that are blocking the red car
# because of duplication goals only the lastly mentioned heuristic is used in this file. Nonetheless, can the firstly
# mentioned heuristic still be called in the cost method

import heapq

class Node:
    """this is class with characteristics of a configuration of the puzzle board, represented as node."""

    def __init__(self, board, parent):
        """This method initializes a node with a given board configuration and parent node. Furthermore, it initializes
        a node with the coordinates of the red car, distance from the begin board, distance to the goal, cars that
        are blocking the blocked cars and a calculation of the cost"""
        self.board = board
        self.parent = parent
        self.red_car_row, self.red_car_col = self.calculate_coordinates_red_car()
        self.distance_from_begin = self.calculate_distance_from_begin()
        # self.distance_to_goal = 2 * self.calculate_blocking_steps()
        self.blocking_blocked_cars = self.blocked_cars_blocking_red_car()
        self.calculate_cost()

    def calculate_cost(self):
        """This method calculates and returns the cost, depending on the used heuristics"""
        # cost = self.distance_from_begin + self.distance_to_goal
        cost = self.blocking_blocked_cars + self.distance_from_begin
        self.cost = cost
        return cost

    def calculate_coordinates_red_car(self):
        """This method calculates the coordinates of the red car"""
        for row_idx, row in enumerate(self.board.board):
            for col_idx, col in enumerate(row):
                if col == 'X':
                    return row_idx, col_idx

    def calculate_distance_from_begin(self):
        """This method calculates and returns the distance from the begin board"""
        if self.parent is None:
            return 0
        else:
            distance = self.parent.distance_from_begin + 1
            return distance

    def calculate_blocking_steps(self):
        """This method calculates and returns the blocking steps from the coordinates of the cars till the goal board
        configuration"""
        length_position = self.red_car_col + 2
        blocked_steps = 0

        for col in self.board.board[self.red_car_row][length_position:]:
            if col != '.':
                blocked_steps = blocked_steps + 1

        return blocked_steps

    def calculate_steps_to_end(self):
        """This method calculates and returns the total amount of steps till the end"""
        length_position = self.red_car_col + 2
        steps = 0

        for col in self.board.board[self.red_car_row][length_position:]:
            if col == '.':
                steps = steps + 1

        return steps

    def blocked_cars_blocking_red_car(self):
        """This method calculates and returns the blocking cars of the cars that are blocking the red car"""
        length_position = self.red_car_col + 2
        visited = set()
        visited.add('X')
        blocked = 0

        for idx, col in enumerate(self.board.board[self.red_car_row][length_position:]):
            if col != '.':
                blocked += 1 + self.cars_blocking_blocking_cars_entire_row(self.red_car_row, idx, col, visited)
        return blocked

    def cars_blocking_blocking_cars_entire_row(self, row, col, char, visited):
        """This method will calculate and return the cars that are blocking the passed car"""
        current_board = self.board.board
        orientation = ''
        blocks = 0
        visited.add(char)

        # check orientation
        if row - 1 >= 0:
            if current_board[row - 1][col] == char:
                orientation = 'V'
        if row + 1 < len(current_board):
            if current_board[row + 1][col] == char:
                orientation = 'V'
        if col - 1 >= 0:
            if current_board[row][col - 1] == char:
                orientation = 'H'
        if col + 1 < len(current_board):
            if current_board[row][col + 1] == char:
                orientation = 'H'
        # check the blocking neighbours
        for i in range(0, len(current_board)):
            if orientation == 'H':
                if current_board[row][i] != '.' and current_board[row][i] != char:
                    if current_board[row][i] not in visited:
                        blocks += 1 + self.cars_blocking_blocking_cars_entire_row(row, i, current_board[row][i], visited)
                    else:
                        blocks += 1
            else:
                if current_board[i][col] != '.' and current_board[i][col] != char:
                    if current_board[i][col] not in visited:
                        blocks += 1 + self.cars_blocking_blocking_cars_entire_row(i, col, current_board[i][col], visited)
                    else:
                        blocks += 1

        return blocks

    def check_node_end(self):
        """This method will check if the coordinates of the red car are at the end goal board configuration"""
        check_step = len(self.board.board[0]) - 2
        if self.red_car_col == check_step:
            return True
        return False

    def __eq__(self, other):
        """This configuration will check if self and other have the same board configuration. And, will return True if
        this is the case"""
        return self.board.board == other.board.board

    def __lt__(self, other):
        """This method will check if self.cost is less than other.cost. And, will return True if this is the case"""
        return self.calculate_cost() < other.calculate_cost()

    def __gt__(self, other):
        """This method will check if self.cost is greater than other.cost. And, will return True if this is the case"""
        return self.calculate_cost() > other.calculate_cost()

class AStar:
    """This is a class for the A* algorithm"""

    def __init__(self, board):
        """This method initializes an A* algorithm with an open list, a closed list and a start board which
        is passed"""
        self.open = []
        heapq.heapify(self.open)
        self.closed = []
        self.start_board = board

    def return_found_path(self, node):
        """This method will return the path of the node that is given by tracing back each parent until there is no more
        node"""
        path = []
        current_node = node

        # loop until current node is nothing
        while current_node is not None:
            # add current node's board to the path list
            path.append(current_node.board.board)
            # set the current node to its parent
            current_node = current_node.parent
        # return the path list as reversed
        print("Path found of length: " + str(len(path)))
        return path[::-1]


    def a_star(self):
        """This method will perform the A* algorithm"""
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
                return self.return_found_path(current_node)

            # initialize empty list for the children of that current node
            children = []
            # check all moves that can be made and create nodes
            moves = current_node.board.moves()
            for move in moves:
                children.append(Node(move, current_node))

            # loop through children
            for child in children:
                if child in self.closed:
                    continue
                if child in self.open:
                    for open_node in self.open:
                        if child == open_node and child.distance_from_begin > open_node.distance_from_begin:
                            continue
                heapq.heappush(self.open, child)
        print("No solution found")
        return None
