# Question #2

from a2.a2_q1 import *


def check_teams(graph, csp_sol):
    NumberOfTeams = len(csp_sol)
    for i in range(NumberOfTeams):
        for j in range(1, NumberOfTeams):
            if csp_sol[i] == csp_sol[j]:
                if j in graph[i]:
                    return False
    return True


# Friendship_Graph = rand_graph(0.5, 4)
# Friendship_Graph = {0: [1, 2], 1: [0], 2: [0], 3: []}
# CspSln = {0: 0, 1: 1, 2: 1, 3: 0}
# print(Friendship_Graph)
# print("CSP Solutions", CspSln)
# print("Total # Teams is: ", len(CspSln))
# print(check_teams(Friendship_Graph, CspSln))


