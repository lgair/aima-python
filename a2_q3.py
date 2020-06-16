# Question 3

from csp import *
from a2.a2_q1 import *
from a2.a2_q2 import *
import time


# --------------------CSP code - edited--------------------


class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b

    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases (for example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(n^4) for the
    explicit representation). In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP. Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        # super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
        self.unassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
            self.unassigns += 1

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print("Assignment: ", assignment, "From CSP: ", self)

    # These methods are for the tree and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: non conflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    def obtain_assigned(self):
        """Retrieve number of assigned CSP variables"""
        return self.nassigns

    def obtain_unassigned(self):
        """Retrieve number of unassigned CSP variables"""
        return self.unassigns

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]


# ---------------------------------------------------------


def MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint)


# ---------------------------------------------------------

def Chromatic_Number(csp_sol):
    """
    Return the total number of teams needed to minimally colour the friendship graph
    IE: The Chromatic number of the graph.
    """
    NumTeams = []
    for i in range(len(csp_sol)):
        if csp_sol[i] not in NumTeams:  # Convert csp_sol from object into array
            NumTeams.append(csp_sol[i])
    return len(NumTeams)


def Highest_Degree(Graph):
    """Return the degree of the vertex (person) with the maximum number of edges (friends)"""
    Max_Degree = [0, 0]  # store the Vertex's key from the dictionary and the vertex's degree
    for i in Graph:
        Vertices_Left = len(Graph) - (i + 1)
        if Vertices_Left == 0:
            return Max_Degree
        Current_Vertices_Degree = len(Graph[i])
        Next_Vertices_Degree = len(Graph[i + 1])
        if Current_Vertices_Degree >= Max_Degree[1]:
            Max_Degree[0] = i + 1
            Max_Degree[1] = Current_Vertices_Degree
        if Next_Vertices_Degree >= Max_Degree[1]:
            Max_Degree[0] = i + 1
            Max_Degree[0] = Next_Vertices_Degree
    return Max_Degree


# ---------------------------------------------------------


# Part three Exact Values

# List of teams for the friendship graph containing 31 people (list of colours for 31 vertices)


def Create_Team_Domain(Domain_Size, Max_Team_Num):
    """
    Domain_Size =  total size of Domain
    Max_Team_Num = total number of teams allowed
    List of teams (colours) for the friendship graph containing 31 people (vertices).
    """
    END = False
    Domain = []  # Empty array
    for i in range(Max_Team_Num):
        if not END:
            Domain.append(i)
        if i + 1 == Domain_Size:
            END = True
    return Domain


def Generate(Num_Graphs):
    """
    Generate n graphs with set probability and size, return an array of dictionaries
    """
    graphs = [0, 0, 0, 0, 0, 0]
    for i in range(Num_Graphs):
        if i + 1 > 6:  # probability not to exceed 60%
            return graphs
        graphs[i] = rand_graph((i + 1) * 0.1, 31)  # change back to 31
    return graphs


def run_q3():
    """
    Generate 6 friendship graph problems with 31 vertices with any two nodes having p
    probability of being connected by an edge (they're friends)
    """
    Num_Graphs = 6  # number of graphs to generate
    Friendship_Graphs = Generate(Num_Graphs)
    for i in range(Num_Graphs):
        Degree = [0,0]
        stop_condition = False
        start_time = time.time()

        for j in range(31):
            if not stop_condition:
                domain = Create_Team_Domain(j + 1, 31)
                Constraints = MapColoringCSP(domain, Friendship_Graphs[i])
                AC3(Constraints)
                csp_sol = (backtracking_search(Constraints, inference=forward_checking))
                # if not check_teams(Friendship_Graphs[i], csp_sol):
                #    exit("unsolvable graph")

                # print out data for solved graph
                if csp_sol is not None:
                    solved_time = time.time()
                    #print("Solution: ", csp_sol)
                    # print()
                    print(solved_time - start_time, end='')
                    print(", ", Chromatic_Number(csp_sol), end='')
                    print(", ", Constraints.nassigns, end='')
                    print(", ", Constraints.obtain_unassigned(), end='')
                    Degree = Highest_Degree(Friendship_Graphs[i])
                    print(", ", Degree[0], end='')
                    print(", ", Degree[1], end='')
                    print("\n")
                    stop_condition = True

    return True


def Collect_q3_data(n):
    print("Creating CSV")
    print("Columns follow: Solve Time, Chromatic Number, #Assigned CSP, #Unassigned CSP, Vertex of "
          "Highest Degree, Max Degree in graph")
    for i in range(n):  # Run run_q3 5x
        print("Batch: ", i)
        print()
        run_q3()
    return 0


Collect_q3_data(1)
