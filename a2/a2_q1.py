# Question #1 Create a function called rand_graph(p, n) that returns a new random graph with n nodes numbered 0 to
# n−1 such that every different pair of nodes is connected with probability p. Assume n>1, and 0≤p≤1 For example:

# >>> rand_graph(0.5, 5)
# {0: [2], 1: [2, 4], 2: [0, 1, 4], 3: [], 4: [1, 2]}

# >>> rand_graph(0.1, 10)
# {0: [4, 7], 1: [3, 6], 2: [9], 3: [1, 6], 4: [0, 5], 5: [4], 6: [1, 3], 7: [0], 8: [], 9: [2]}
# Notice that if a appears in the list for key b, then b also appears in the list for key a.

# The higher the value of p, the more edges the resulting graph will have.

# Put all your code for this into a file named a2_q1.py so that the marker can test it.

import random


def rand_graph(p, n):
    """where n is the number of people (vertices) in the graph, & p (probability) determines the number of edges
    between them """
    graph = {}  # empty dictionary
    for i in range(n):
        graph[i] = []  # Create dictionary of size n with nothing in it
    for j in range(n):
        for k in range(j + 1, n):
            if random.random() < p:
                # add to corresponding people (vertices) because friendship is symmetrical
                graph[j].append(k)
                graph[k].append(j)
    return graph


print(rand_graph(0.05, 31))
