import sys
from fractions import Fraction
import itertools

def parse_line(line: str):
    """
    Parse one machine line into:
      - target: list[int] (joltage requirements)
      - buttons: list[list[int]] (indices of counters each button increments)
    Indicator pattern in [...] is ignored for part 2.
    """
    line = line.strip()
    if not line:
        return None

    tokens = line.split()
    if len(tokens) < 2:
        return None

    # Find the token with { ... } for target
    target_tok = None
    for tok in reversed(tokens):
        if tok.startswith("{") and tok.endswith("}"):
            target_tok = tok
            break
    if target_tok is None:
        return None

    inner = target_tok[1:-1].strip()
    if not inner:
        target = []
    else:
        target = [int(x) for x in inner.split(",")]

    # Buttons: tokens that look like "(...)"
    buttons = []
    for tok in tokens:
        tok = tok.strip()
        if tok.startswith("(") and tok.endswith(")"):
            inner_b = tok[1:-1].strip()
            if inner_b:
                idxs = [int(x) for x in inner_b.split(",") if x]
            else:
                idxs = []
            buttons.append(idxs)

    return target, buttons


def rref_solve_system(target, buttons):
    """
    Build A x = target and put [A|b] into RREF over rationals.
    Return:
      - matrix: RREF augmented matrix (m x (k+1))
      - pivot_cols: list of pivot column index per row (or -1 if none)
      - free_cols: list of variable indices that are free
    """
    m = len(target)
    k = len(buttons)

    # Build A (m x k) with 0/1 entries
    A = [[0] * k for _ in range(m)]
    for j, idxs in enumerate(buttons):
        for i in idxs:
            if 0 <= i < m:
                A[i][j] = 1

    # Build augmented matrix with Fractions: m rows, k+1 columns
    mat = [[Fraction(A[r][c], 1) for c in range(k)] + [Fraction(target[r], 1)]
           for r in range(m)]

    pivot_cols = [-1] * m
    row = 0

    # Gauss-Jordan elimination to RREF
    for col in range(k):
        # Find pivot row with non-zero entry in this column
        pivot_row = None
        for r in range(row, m):
            if mat[r][col] != 0:
                pivot_row = r
                break
        if pivot_row is None:
            # no pivot in this column -> free variable
            continue

        # Swap pivot row into position
        if pivot_row != row:
            mat[row], mat[pivot_row] = mat[pivot_row], mat[row]

        # Normalize pivot row so pivot = 1
        pivot_val = mat[row][col]
        if pivot_val != 1:
            for c in range(col, k + 1):
                mat[row][c] /= pivot_val

        # Eliminate this column from all other rows
        for r in range(m):
            if r == row:
                continue
            factor = mat[r][col]
            if factor != 0:
                for c in range(col, k + 1):
                    mat[r][c] -= factor * mat[row][c]

        pivot_cols[row] = col
        row += 1
        if row == m:
            break

    # Check for inconsistency: row of all zeros in A but nonzero RHS
    for r in range(m):
        all_zero = True
        for c in range(k):
            if mat[r][c] != 0:
                all_zero = False
                break
        if all_zero and mat[r][k] != 0:
            # 0 = nonzero -> no solution
            return None, None, None

    # Collect pivot and free columns
    pivot_col_set = set(c for c in pivot_cols if c != -1)
    free_cols = [c for c in range(k) if c not in pivot_col_set]

    return mat, pivot_cols, free_cols


def solve_machine(target, buttons):
    """
    Find minimal sum of button presses for one machine.
    Returns an integer.
    """
    m = len(target)
    k = len(buttons)

    if m == 0:
        return 0
    if all(t == 0 for t in target):
        return 0
    if k == 0:
        # no buttons and nonzero target -> impossible, but puzzle guarantees solvable
        return float('inf')

    mat, pivot_cols, free_cols = rref_solve_system(target, buttons)
    if mat is None:
        # No solution (shouldn't happen in valid input)
        return float('inf')

    # Map pivot_col -> row index
    pivot_row_for_col = {}
    for r, pc in enumerate(pivot_cols):
        if pc != -1:
            pivot_row_for_col[pc] = r

    k = len(buttons)  # number of variables
    max_target = max(target) if target else 0

    # Simple per-variable upper bounds:
    # For variable j, x_j <= min target[i] where A[i][j] = 1
    # If a button affects no counters (shouldn't happen), bound = 0.
    A = [[0] * k for _ in range(m)]
    for j, idxs in enumerate(buttons):
        for i in idxs:
            if 0 <= i < m:
                A[i][j] = 1

    var_upper = [0] * k
    for j in range(k):
        affected_targets = [target[i] for i in range(m) if A[i][j] == 1]
        if affected_targets:
            var_upper[j] = min(affected_targets)
        else:
            var_upper[j] = 0  # button that affects no counters is useless

    # If there are no free variables, the solution is unique
    if not free_cols:
        x = [0] * k
        # Each pivot column corresponds directly to x[col] = mat[row][k]
        for col, row in pivot_row_for_col.items():
            val = mat[row][k]
            # must be integer and >= 0
            if val.denominator != 1:
                return float('inf')
            iv = val.numerator
            if iv < 0:
                return float('inf')
            x[col] = iv
        # Check solution satisfies A x = target and var bounds
        for i in range(m):
            s = sum(A[i][j] * x[j] for j in range(k))
            if s != target[i]:
                return float('inf')
        for j in range(k):
            if x[j] > var_upper[j]:
                # we could still allow this, but in a correct system it shouldn't happen
                return float('inf')
        return sum(x)

    # Otherwise enumerate free variable assignments within bounds
    free_ranges = []
    for col in free_cols:
        free_ranges.append(range(var_upper[col] + 1))

    best = None

    for free_values in itertools.product(*free_ranges):
        x = [None] * k
        # Assign free variables
        for idx, col in enumerate(free_cols):
            x[col] = free_values[idx]

        # Solve for pivot variables using RREF rows
        valid = True
        for col, row in pivot_row_for_col.items():
            # Row expresses:
            # x[col] + sum_{j in free_cols} mat[row][j] * x[j] = mat[row][k]
            rhs = mat[row][k]
            for fc in free_cols:
                coeff = mat[row][fc]
                if coeff != 0:
                    rhs -= coeff * x[fc]
            # Now rhs should be the value of x[col]
            if rhs.denominator != 1:
                valid = False
                break
            iv = rhs.numerator
            if iv < 0:
                valid = False
                break
            if iv > var_upper[col]:
                # Can't exceed safe bound
                valid = False
                break
            x[col] = iv

        if not valid:
            continue

        # Sanity: ensure all variables assigned and within bounds
        for j in range(k):
            if x[j] is None or x[j] < 0:
                valid = False
                break
            if x[j] > var_upper[j]:
                valid = False
                break
        if not valid:
            continue

        # Final sanity: check A x == target
        for i in range(m):
            s = sum(A[i][j] * x[j] for j in range(k))
            if s != target[i]:
                valid = False
                break
        if not valid:
            continue

        total_presses = sum(x)
        if best is None or total_presses < best:
            best = total_presses

    # In valid AoC input, best should never be None
    return best if best is not None else float('inf')


def main():
    total = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parsed = parse_line(line)
        if not parsed:
            continue
        target, buttons = parsed
        presses = solve_machine(target, buttons)
        total += presses
    print(total)

if __name__ == "__main__":
    main()
