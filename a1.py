# a1.py

from search import *
import time
import random


# ...
# ______________________________________________________________________________
# A* heuristics

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

    # allows printing of multiple puzzles
    def get_state(self):
        return self.initial


#  ____________________________End EightPuzzle__________________________________________________

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
    while frontier:
        node = frontier.pop()
        FledTheFrontier += 1  # Account for all fleeing nodes
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


SOLVED_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
NUM_RANDOM_MOVES = 40


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


# Helper function that displays the state of 8 puzzle (tuple) in 3x3 form
def display(state):
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

    def f():

        start_time = time.time()

        # ... do something ...

        elapsed_time = time.time() - start_time

        print(f'elapsed time (in seconds): {elapsed_time}s')


def eight_puzzle_analysis():
    print('generating 10 puzzles for stats')
    puzzles = make_n_puzzles(10)
    for puzz in puzzles:
        display(puzz.get_state())

        for puzz in puzzles:
            start_time = time.time_ns()
            finished_puzzle = astar_search(puzz)
            elapsed_time = (time.time_ns() - start_time)/1000000000
        print("data for A* search using misplaced tile Heuristic (default)")
        print('TIME:                    ', elapsed_time)
        print('LENGHT:                  ', finished_puzzle.path_cost)
        print('# of Frontier Fugitives: ', finished_puzzle)



eight_puzzle_analysis()
