# Declare any required symbolic variables
from sympy import symbols, Eq, Ne

from util import constraint, displayBoard

X = symbols("X:2")
Y = symbols("Y:2")

# Define diffRow and diffDiag constraints
diffRow = constraint("diffRow", Ne(X[0], X[1]))
diffDiag = constraint("diffDiag", Ne(abs(X[0] - X[1]), abs(Y[0] - Y[1])))


class NQueensCSP:
    """CSP representation of the N-queens problem

    Parameters
    ----------
    N : Integer
        The side length of a square chess board to use for the problem, and
        the number of queens that must be placed on the board
    """

    def __init__(self, N):
        _vars = symbols('x:%d'%N)
        _domain = set(range(N))
        self.size = N
        self.variables = _vars
        self.domains = {v: _domain for v in _vars}
        self._constraints = {x: set() for x in _vars}

        print(self.variables)

        # add constraints - for each pair of variables xi and xj, create
        # a diffRow(xi, xj) and a diffDiag(xi, xj) instance, and add them
        # to the self._constraints dictionary keyed to both xi and xj;
        # (i.e., add them to both self._constraints[xi] and self._constraints[xj])
        for i in range(0, len(self.variables)-1):
            for j in range (i+1, len(self.variables)):
                xi = self.variables[i]
                xj = self.variables[j]

                diffrow = diffRow.subs({X[0] : xi, X[1] : xj})
                self._constraints[xi].add(diffrow)
                self._constraints[xj].add(diffrow)

                diffdiag = diffDiag.subs({Y[0] : i, Y[1] : j, X[0] : xi, X[1] : xj})
                self._constraints[xi].add(diffdiag)
                self._constraints[xj].add(diffdiag)



    @property
    def constraints(self):
        """Read-only list of constraints -- cannot be used for evaluation """
        constraints = set()
        for _cons in self._constraints.values():
            constraints |= _cons
        return list(constraints)

    def is_complete(self, assignment):
        """An assignment is complete if it is consistent, and all constraints
        are satisfied.

        Hint: Backtracking search checks consistency of each assignment, so checking
        for completeness can be done very efficiently

        Parameters
        ----------
        assignment : dict(sympy.Symbol: Integer)
            An assignment of values to variables that have previously been checked
            for consistency with the CSP constraints
        """
        if len(assignment) != self.size:
            return False

        for var in assignment:
            value = assignment[var]
            if not self.is_consistent(var, value, assignment):
                return False

        return True

    def is_consistent(self, var, value, assignment):
        """Check consistency of a proposed variable assignment

        self._constraints[x] returns a set of constraints that involve variable `x`.
        An assignment is consistent unless the assignment it causes a constraint to
        return False (partial assignments are always consistent).

        Parameters
        ----------
        var : sympy.Symbol
            One of the symbolic variables in the CSP

        value : Numeric
            A valid value (i.e., in the domain of) the variable `var` for assignment

        assignment : dict(sympy.Symbol: Integer)
            A dictionary mapping CSP variables to row assignment of each queen

        """
        constraints = self._constraints[var]

        for c in constraints:
            constr = c.subs({var : value})
            vars = constr.free_symbols
            variable = next(iter(vars))
            if variable in assignment.keys():
                if not constr.subs({variable: assignment[variable]}):
                    return False

        return True

    def inference(self, var, value):
        """Perform logical inference based on proposed variable assignment

        Returns an empty dictionary by default; function can be overridden to
        check arc-, path-, or k-consistency; returning None signals "failure".

        Parameters
        ----------
        var : sympy.Symbol
            One of the symbolic variables in the CSP

        value : Integer
            A valid value (i.e., in the domain of) the variable `var` for assignment

        Returns
        -------
        dict(sympy.Symbol: Integer) or None
            A partial set of values mapped to variables in the CSP based on inferred
            constraints from previous mappings, or None to indicate failure
        """
        # TODO (Optional): Implement this function based on AIMA discussion
        return {}

    def show(self, assignment):
        """Display a chessboard with queens drawn in the locations specified by an
        assignment

        Parameters
        ----------
        assignment : dict(sympy.Symbol: Integer)
            A dictionary mapping CSP variables to row assignment of each queen

        """
        locations = [(i, assignment[j]) for i, j in enumerate(self.variables)
                     if assignment.get(j, None) is not None]
        displayBoard(locations, self.size)


def select(csp, assignment):
    """Choose an unassigned variable in a constraint satisfaction problem """
    # TODO (Optional): Implement a more sophisticated selection routine from AIMA
    mindomain = float("inf")
    variable = None
    for var in csp.variables:
        if var not in assignment:
            remainingvalues = len(csp.domains[var])
            if remainingvalues < mindomain:
                variable = var
                mindomain = remainingvalues
            #return var
    #return None
    return variable


def order_values(var, assignment, csp):
    """Select the order of the values in the domain of a variable for checking during search;
    the default is lexicographically.
    """
    # TODO (Optional): Implement a more sophisticated search ordering routine from AIMA
    return csp.domains[var]


def backtracking_search(csp):
    """Helper function used to initiate backtracking search """
    return backtrack({}, csp)


def backtrack(assignment, csp):
    """Perform backtracking search for a valid assignment to a CSP

    Parameters
    ----------
    assignment : dict(sympy.Symbol: Integer)
        An partial set of values mapped to variables in the CSP

    csp : CSP
        A problem encoded as a CSP. Interface should include csp.variables, csp.domains,
        csp.inference(), csp.is_consistent(), and csp.is_complete().

    Returns
    -------
    dict(sympy.Symbol: Integer) or None
        A partial set of values mapped to variables in the CSP, or None to indicate failure
    """
    if csp.is_complete(assignment):
        return assignment

    var = select(csp, assignment)

    for value in order_values(var, assignment, csp):
        if csp.is_consistent(var, value, assignment):
            assignment[var] = value

            inferences = csp.inference(var, value)

            if inferences is not None:
                if len(inferences) > 0:
                    assignment.update(inferences)

                result = backtrack(assignment, csp)

                if result is not None:
                    return result

                # todo check!
                for i in inferences:
                    assignment.pop(i)

        if var in assignment.keys():
            assignment.pop(var)

    return None