
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

def diagonal(A, B):
    """Diagonal of elements in A and elements in B """
    result = []
    for i in range(0, len(A)):
        result.append(A[i]+B[i])

    return result

diagonal_units = [diagonal(rows, cols), diagonal(rows, cols[::-1]) ]
unitlist = unitlist + diagonal_units # Update the unit list to add the new diagonal units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def is_solved(values):
    """
    Checks if the sudoku is solved.
    :param values(dict):
        a dictionary of the form {'box_name': '123456789', ...}

    :return:
        True if the dictionary corresponds to solved sudoku, False otherwise
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    if len(solved_values) == 81:
        return True

    return False

def process_with_naked_twins(units, values):
    """
    Apply a single iteration of naked twins algorithm to a sudoku grid.
    :param units: The list of units.
    :param values: The dictionary of sudoku grid values.
    :return: True if any grid cell has been modified, False otherwise.
    """

    values_updated = False

    for unit in units:

        # find naked twins within a single unit
        naked_twins_dictionary = {}
        naked_twins = []
        for element in unit:
            val = values[element]
            if len(val) == 2:
                if val in naked_twins_dictionary:
                    naked_twins.append(val)
                else:
                    naked_twins_dictionary[val] = element

        # process naked twins found
        for n in naked_twins:
            for element in unit:
                val = values[element]

                if len(val) > 1 and val != n:
                    for number in n:
                        val = val.replace(number, '')

                    if values[element] != val:
                        values[element] = val
                        values_updated = True

    return values_updated


def get_key_with_fewest_possibilities(values):
    """
    Gets key with the fewest choice of possible values. There should be at least 2 values in the box.
    :param values: dictionary of grid values.
    :return: the key with the fewest choice of possible values.
    """
    min_number_of_possibilities = 0
    key = ''

    for k in values:
        number_of_possibilities = len(values[k])
        if number_of_possibilities > 1:
            if min_number_of_possibilities == 0 or min_number_of_possibilities > number_of_possibilities:
                min_number_of_possibilities = number_of_possibilities
                key = k

    return key


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    stalled = False

    while not stalled:
        stalled = not process_with_naked_twins(unitlist, values)

    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    keys = values.keys()

    for k in keys:
        val = values[k]
        if len(val) == 1:
            for p in peers[k]:
                if p != k and isinstance(values[p], str):
                    values[p] = values[p].replace(val, '')

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for su in unitlist:
        units_dict_common = {}
        units_dict_unique = {}

        for u in su:
            val = values[u]

            if len(val) == 1:
                pass

            for s in val:
                if s in units_dict_common.keys():
                    if s in units_dict_unique.keys():
                        del units_dict_unique[s]
                else:
                    units_dict_common[s] = u
                    units_dict_unique[s] = u

        for uval in units_dict_unique:
            value_to_set = uval
            key_to_set = units_dict_unique[uval]
            values[key_to_set] = value_to_set


    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)
        # Your code here: Use the Only Choice Strategy
        only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    values_to_process = dict(values)

    values_to_process = reduce_puzzle(values_to_process)

    if values_to_process == False:
        return False

    # apply naked twins technique
    values_to_process = naked_twins(values_to_process)

    if is_solved(values_to_process):
        values = values_to_process
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    key = get_key_with_fewest_possibilities(values_to_process)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    val = values_to_process[key]
    for v in val:
        values_to_process[key] = v

        result_to_process = dict(values_to_process)
        retval = search(result_to_process)

        if retval == False:
            continue

        return retval

    return False


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
