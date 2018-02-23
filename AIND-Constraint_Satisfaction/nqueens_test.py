# Test diffRow and diffDiag
from IPython.core.display import display
from sympy import symbols

from nqueens import diffRow, diffDiag, NQueensCSP, X, Y, backtracking_search

_x = symbols("x:3")

# generate a diffRow instance for testing
diffRow_test = diffRow.subs({X[0] : _x[0], X[1] : _x[1]})

assert(len(diffRow_test.free_symbols) == 2)
assert(diffRow_test.subs({_x[0]: 0, _x[1]: 1}) == True)
assert(diffRow_test.subs({_x[0]: 0, _x[1]: 0}) == False)
assert(diffRow_test.subs({_x[0]: 0}) != False)  # partial assignment is not false
print("Passed all diffRow tests.")

# generate a diffDiag instance for testing
diffDiag_test = diffDiag.subs({Y[0] : 2, Y[1] : _x[2], X[0] : _x[0], X[1] : 0})

assert(len(diffDiag_test.free_symbols) == 2)
assert(diffDiag_test.subs({_x[0]: 0, _x[2]: 2}) == False)
assert(diffDiag_test.subs({_x[0]: 0, _x[2]: 0}) == True)
assert(diffDiag_test.subs({_x[0]: 0}) != False)  # partial assignment is not false
print("Passed all diffDiag tests.")

num_queens = 12
csp = NQueensCSP(num_queens)
var = csp.variables[0]
print("CSP problems have variables, each variable has a domain, and the problem has a list of constraints.")
print("Showing the variables for the N-Queens CSP:")
display(csp.variables)
print("Showing domain for {}:".format(var))
display(csp.domains[var])
print("And showing the constraints for {}:".format(var))
display(csp._constraints[var])

print("Solving N-Queens CSP...")
assn = backtracking_search(csp)
if assn is not None:
    #csp.show(assn)
    print("Solution found:\n{!s}".format(assn))
else:
    print("No solution found.")
