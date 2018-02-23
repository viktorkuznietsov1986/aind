import matplotlib as mpl
import matplotlib.pyplot as plt

from IPython.display import display
from sympy import *

from util import constraint

init_printing()

x = Symbol('x')
display(x)

i, j, k = symbols(['i', 'j', 'k'])  # use implicit unpacking to associate multiple symbols with variables
display((i, j, k))

X = symbols("X:3")
display(X)

x, y = symbols('x y')
or_relation = x | y

display(or_relation)

x, y = symbols("x y")
y = x   # now y references the same symbolic object as x
display(y)  # display(y) == x  ??!

x, z = symbols("x z")
display(Eq(z, x))

x, y, z = symbols("x y z")
display([x**2, x - y, Ne(x, y), (~x & y & z)])

x, y, z = symbols("x y z")
relation = Eq(x, y)
display(relation)

display(relation.subs(x, z))

a = symbols("a:5")
b = symbols("b:5")
display([relation.subs({x: _a, y: _b}) for _a, _b in zip(a, b)])

print(type(relation), type(relation.subs(x, z)))
print(type(relation) == type(relation.subs(x, z)))

print(type(relation), type(relation.subs({x: 0, y: 1})))
print(type(relation) != type(relation.subs({x: 0, y: 1})))

x, y = symbols(['x', 'y'])
sameAs = constraint("SameAs", Eq(x, y))
display(sameAs)

display(sameAs.subs(x, 0), type(sameAs.subs(x, 0)))

display(sameAs.subs({x: 0, y: 0}), type(sameAs.subs({x: 0, y: 0})))

A = symbols("A:3")

# test for completion
assert(len(A) == 3)
assert(all([type(v) == Symbol for v in A]))
print("All tests passed!")


x,y = symbols("x,y")
E = x^y

# test for completion
_vars = E.free_symbols
assert(len(_vars) == 2)
xor_table = {(0, 0): False, (0, 1): True, (1, 0): True, (1, 1): False}
assert(all(E.subs(zip(_vars, vals)) == truth for vals, truth in xor_table.items()))
print("All tests passed!")

a,b,c = symbols("a,b,c")
maxAbsDiff = constraint("maxAbsDiff", (abs(a-b) < c))
maxAbsDiff_copy = constraint("maxAbsDiff_copy", (abs(A[0] - A[1]) < A[2]))

# test for completion
assert(maxAbsDiff.free_symbols != maxAbsDiff_copy.free_symbols)
assert(len(maxAbsDiff_copy.free_symbols) == len(maxAbsDiff_copy.args))
inputs = {(0, 6, 7): True, (6, 0, 7): True, (7, 6, 0): False}
assert(all(maxAbsDiff_copy.subs(zip(A[:3], vals)) == truth for vals, truth in inputs.items()))
print("All tests passed!")

expr = ~Eq(A[0], A[1]) & ~Eq(A[1], A[2]) & ~Eq(A[0], A[2]) 
allDiff = constraint("allDiff", expr)

inputs = (([0, 1, 2], True), ([1, 1, 1], False), ([0, 1, 1], False))
assert(all(allDiff.subs(zip(A, vals)) == truth for vals, truth in inputs))
print("All tests passed!")