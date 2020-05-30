# a1.py

from search import *
import time

# ...
# Return a random and solvable puzzle from EightPuzzle class using problem function
print('in a1 file')
SimpleBoard = (1, 2, 3, 4, 0, 6, 7, 8, 5)


def make_rand_8puzzle():
    print("called make_rand_8puzzle")
    numbers = []
    numbers = [1, 2, 3, 4, 5]
    print(numbers)
    return 0


make_rand_8puzzle()


# Helper function that displays the state of 8 puzzle (tuple) in 3x3 form
def display(state):
    # I am going to call the state the "board" since the state is a tuple, I will store all the object values in an
    # array so that they may be printed. The blank square or 0 will be notated by a *
    print('In Display Function')

    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # Initialize the array with zeroes

    for i in range(len(state)):

        board[i] = state[i]
        if board[i] == 0:
            board[i] = '*'
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


print('test printing of simple board')
display(SimpleBoard)


def f():
    start_time = time.time()

    # ... do something ...

    elapsed_time = time.time() - start_time

    print(f'elapsed time (in seconds): {elapsed_time}s')
