# a1.py advice for manhattan distance taken from
# https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
# https://www.geeksforgeeks.org/sum-manhattan-distances-pairs-points/


from search import *
import time
import random

# ...
SOLVED_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
NUM_RANDOM_MOVES = 100
#PYCHARM_DEBUG = True


# ______________________________________________________________________________
# A* heuristics
# Duck Puzzle


class DuckPuzzle(Problem):
    """ almost the same as eightpuzzle but now the board looks like a duck facing to the left
     1 2
     3 4 5 6   goal state
       7 8 *
    Tiles slide into the blank (the *) as in the regular 8-puzzle, but now the board has a different shape which changes
    the possible moves.
    """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        unable_to_move_up = (0, 1, 4, 5)
        unable_to_move_down = (2, 6, 7, 8)
        unable_to_move_left = (0, 2, 6)
        unable_to_move_right = (1, 5, 8)
        # check which tuples the blank square is in and remove corresponding move option
        if index_blank_square in unable_to_move_left:
            possible_actions.remove('LEFT')
        if index_blank_square in unable_to_move_up:
            possible_actions.remove('UP')
        if index_blank_square in unable_to_move_right:
            possible_actions.remove('RIGHT')
        if index_blank_square in unable_to_move_down:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state
        duckPuzzle Shape should induce some special cases here.
            1 2
            3 4 5 6
              7 8 *
        the numbers at index's 0, 1, and 2 will forever be trapped in that corner of the house. Therefore index
        tile 3 is a special case. Tile index 0, 1, & 2 are also their own special cases.
        """
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}  # for most numbers in normal places
        delta_case1 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}  # specifically for tile at index #3
        delta_case2 = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}  # Special case for tiles at index 0, 1, & 2
        blank_case2 = (0, 1, 2)
        if blank is 3:
            neighbor = blank + delta_case1[action]
        elif blank in blank_case2:
            neighbor = blank + delta_case2[action]
        else:
            neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1
        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        # Goal state is puzzle = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        # for my simplicity index has been shortened to `i`
        # adapted from the manhattan function in test_search.py
        currentstate = node.state  # Grab the current state of the EightPuzzle object passed via the node
        i_target = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        i_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        for i in range(len(currentstate)):
            i_state[currentstate[i]] = index[i]  # initialize i_state dictionary
        manhattan_distance_x = 0
        manhattan_distance_y = 0
        for i in range(9):
            manhattan_distance_x += abs(i_target[i][0] - i_state[i][0])  # two indices because index was 2d array
            manhattan_distance_y += abs(i_target[i][1] - i_state[i][1])
        return manhattan_distance_y + manhattan_distance_x

    def a_max(self, node):
        """ Return the biggest heuristic value from either manhattan or h
        Always grantee most efficient result and larger euristic dominates
        the smaller one"""

        h = self.h(node)
        manhattan = self.manhattan(node)
        return max(h, manhattan)

    def get_state(self):
        """Obtain Current state of EightPuzzle Object, could be useful for display"""
        return self.initial
# END duck_puzzle class


def display_Dpuzz(state):
    """ Helper function that displays duck_puzzle formatted properly (like a duck)"""
    # I am going to call the state the "board". Since the state is a tuple, all the object values are stored in an
    # array so that they may be printed. The blank square or 0 will be notated by a *
    # logically the same as display(state) above but for duckpuzzle()
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # Initialize the array with zeroes
    for i in range(9):
        board[i] = state[i]
        if board[i] == 0:
            board[i] = '*'
        # logic below for printing a duck array QUACK
        if i <= 1:
            print(board[i], ' ', end='')
            if i == 1:
                print()
        elif 5 >= i > 1:
            print(board[i], ' ', end='')
            if i == 5:
                print()
                print('   ', end='')
        else:
            print(board[i], ' ', end='')
    print()
    print()


def make_rand_duckPuzz():
    state = SOLVED_STATE
    puzz = DuckPuzzle(state)

    for _ in range(NUM_RANDOM_MOVES):
        possible_actions = puzz.actions(state=state)  # All currently valid moves for 0
        action = random.choice(possible_actions)  # Pick a valid move at random
        state = puzz.result(state=state, action=action)  # Apply it to random state, set state to new state
    return DuckPuzzle(state)  # Will always be a solvable puzzle as valid moves have been applied to a solved state


def make_n_Dpuzz(n):  # Create an Array of n Random puzzles
    puzzles = []
    for _ in range(n):
        puzzles.append(make_rand_duckPuzz())
    return puzzles
#-----------------End Duck Puzzle functions-----------------------


class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):
        # Goal state is puzzle = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        # for my simplicity index has been shortened to `i`
        # adapted from the manhattan function in test_search.py
        currentstate = node.state  # Grab the current state of the EightPuzzle object passed via the node
        i_target = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        i_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        # x = 0
        # y = 0

        for i in range(len(currentstate)):
            i_state[currentstate[i]] = index[i]  # initialize i_state dictionary

        manhattan_distance_x = 0
        manhattan_distance_y = 0

        for i in range(9):
            manhattan_distance_x += abs(i_target[i][0] - i_state[i][0])  # two indices because index was 2d array
            manhattan_distance_y += abs(i_target[i][1] - i_state[i][1])

        return manhattan_distance_y + manhattan_distance_x

    def a_max(self, node):
        """ Return the biggest heuristic value from either manhattan or h
        Always grantee most efficient result and larger euristic dominates
        the smaller one"""

        h = self.h(node)
        manhattan = self.manhattan(node)
        return max(h, manhattan)

    def get_state(self):
        """Obtain Current state of EightPuzzle Object, could be useful for display"""
        return self.initial


def display(state):
    """ Helper function that displays the state of 8 puzzle (tuple) in 3x3 form"""
    # I am going to call the state the "board". Since the state is a tuple, all the object values are stored in an
    # array so that they may be printed. The blank square or 0 will be notated by a *
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # Initialize the array with zeroes

    for i in range(9):
        board[i] = state[i]
        if board[i] == 0:
            board[i] = '*'
        # logic below for printing a 3x3 array
        if i <= 2:
            print(board[i], ' ', end='')
            if i == 2:
                print()
        elif 5 >= i > 2:
            print(board[i], ' ', end='')
            if i == 5:
                print()
        else:
            print(board[i], ' ', end='')
    print()
    print()


def make_rand_8puzzle():
    state = SOLVED_STATE
    puzz = EightPuzzle(state)
    for _ in range(NUM_RANDOM_MOVES):
        possible_actions = puzz.actions(state=state)  # All currently valid moves for 0
        action = random.choice(possible_actions)  # Pick a valid move at random
        state = puzz.result(state=state, action=action)  # Apply it to random state, set state to new state
    return EightPuzzle(state)  # Will always be a solvable puzzle as valid moves have been applied to a solved state


def make_n_puzzles(n):  # Create an Array of n Random puzzles
    puzzles = []
    for _ in range(n):
        puzzles.append(make_rand_8puzzle())
    return puzzles
# -------------------------------------End EightPuzzle Functions--------------------------------


# ----------------------------- A* Search variations!-------------------------------------------
def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# Modify astar_search to use Manhattan Distance Heuristic
def astar_manhattan(problem, h=None):
    """Modification on A* search to use Manhattan Distance as Heuristic"""
    h = memoize(h or problem.manhattan, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


# modified astar_search to use maximum of misplaced tile heuristic
def astar_max(problem, h=None):
    h = memoize(h or problem.a_max, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


# ---------------------------------END A* Search Variations-------------------------------------


def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    FledTheFrontier = 0  # Tracks how many nodes have fled the frontier (were removed from it) yeeehaw
    test = 0
    while frontier:
        test += 1
        node = frontier.pop()
        FledTheFrontier += 1  # Account for all fleeing nodes
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, FledTheFrontier]  # Return FledFromFrontier here so that we may access it outside the func
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None
# ----------Small Functions to generate 10 (or n) puzzles for some statistical analysis----------


def eight_puzzle_analysis():
    # print("data for 10 puzzles using A* search using misplaced tile Heuristic (default)")
    puzzles = make_n_puzzles(10)

    for puzz in puzzles:
        display(puzz.get_state())
        start_time = time.time_ns()
        finished_puzzle = astar_search(puzz)
        elapsed_time = (time.time_ns() - start_time) / 1000000000
        # Output data in CSV Format where first column is TIME (s), Second is LENGTH, and Third is FRONTIER-
        print(elapsed_time, end='')
        print(',', finished_puzzle[0].path_cost, end='')
        print(',', finished_puzzle[1])
    print()

    # print("data for 10 puzzles using modified A* with manhattan distance heuristic")
    for puzz in puzzles:
        start_time = time.time_ns()
        finished_puzzle = astar_manhattan(puzz)
        elapsed_time = (time.time_ns() - start_time) / 1000000000
        # Output data in CSV Format where first column is TIME (s), Second is LENGTH, and Third is FRONTIER-
        print(elapsed_time, end='')
        print(',', finished_puzzle[0].path_cost, end='')
        print(',', finished_puzzle[1])
    print()

    # print("data for 10 puzzles using modified A* with max misplaced distance heuristic")
    for puzz in puzzles:
        start_time = time.time_ns()
        finished_puzzle = astar_max(puzz)
        elapsed_time = (time.time_ns() - start_time) / 1000000000
        # Output data in CSV Format where first column is TIME (s), Second is LENGTH, and Third is FRONTIER-
        print(elapsed_time, end='')
        print(',', finished_puzzle[0].path_cost, end='')
        print(',', finished_puzzle[1])


def duck_puzzle_analysis():
    puzzles = make_n_Dpuzz(10)

    for puzz in puzzles:
        #display_Dpuzz(puzz.get_state())
        start_time = time.time_ns()
        finished_puzzle = astar_search(puzz)
        elapsed_time = (time.time_ns() - start_time) / 1000000000
        # Output data in CSV Format where first column is TIME (s), Second is LENGTH, and Third is FRONTIER-
        print(elapsed_time, end='')
        print(',', finished_puzzle[0].path_cost, end='')
        print(',', finished_puzzle[1])
    print()
    # print("data for 10 puzzles using modified A* with manhattan distance heuristic")
    for puzz in puzzles:
        start_time = time.time_ns()
        finished_puzzle = astar_manhattan(puzz)
        elapsed_time = (time.time_ns() - start_time) / 1000000000
        # Output data in CSV Format where first column is TIME (s), Second is LENGTH, and Third is FRONTIER-
        print(elapsed_time, end='')
        print(',', finished_puzzle[0].path_cost, end='')
        print(',', finished_puzzle[1])
    print()
    # print("data for 10 puzzles using modified A* with max misplaced distance heuristic")
    for puzz in puzzles:
        start_time = time.time_ns()
        finished_puzzle = astar_max(puzz)
        elapsed_time = (time.time_ns() - start_time) / 1000000000
        # Output data in CSV Format where first column is TIME (s), Second is LENGTH, and Third is FRONTIER-
        print(elapsed_time, end='')
        print(',', finished_puzzle[0].path_cost, end='')
        print(',', finished_puzzle[1])
    return 0


def single_duck_puzzle():
    #debugging to find where misplaced action
    puzzle = make_rand_duckPuzz()
    #display_Dpuzz(puzzle.get_state())


#single_duck_puzzle()
# eight_puzzle_analysis()
duck_puzzle_analysis()
