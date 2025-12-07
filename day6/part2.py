import sys
from functools import reduce
import operator


def main():
    lines = [line.rstrip("\n") for line in sys.stdin.readlines()]
    if not lines:
        print(0)
        return

    # Pad all lines to the same width
    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]

    height = len(grid)
    last_row = height - 1

    def is_blank_col(c: int) -> bool:
        """Return True if column c is all spaces."""
        for r in range(height):
            if grid[r][c] != " ":
                return False
        return True

    total = 0
    c = width - 1  # start from rightmost column

    while c >= 0:
        # Skip blank separator columns
        if is_blank_col(c):
            c -= 1
            continue

        # We just hit the RIGHT edge of a problem.
        right = c
        left = c
        # Extend leftwards until we hit a blank column or the grid edge.
        while left - 1 >= 0 and not is_blank_col(left - 1):
            left -= 1

        # Columns [left .. right] (inclusive) are this problem.
        # We'll process them from right to left, since cephalopod math is RTL.
        problem_cols = list(range(right, left - 1, -1))

        # Find the operator column (exactly one column with + or * on the bottom row).
        op = None
        for col in problem_cols:
            ch = grid[last_row][col]
            if ch in "+*":
                if op is not None:
                    raise ValueError("Multiple operators found in a single problem.")
                op = ch

        if op is None:
            raise ValueError("No operator found in a problem block.")

        # Each column (including the operator column) contributes one number.
        numbers = []
        for col in problem_cols:
            digits = []
            for r in range(last_row):  # exclude bottom operator row
                ch = grid[r][col]
                if ch.isdigit():
                    digits.append(ch)
            if digits:
                num = int("".join(digits))
                numbers.append(num)
            else:
                # By puzzle spec, there should always be some digit; if not, treat as error.
                raise ValueError(f"No digits found in column {col} of a problem.")

        # Apply the operator over all numbers in this problem
        if op == "+":
            result = sum(numbers)
        else:  # op == "*"
            result = reduce(operator.mul, numbers, 1)

        total += result

        # Next problem lies further left, past this block
        c = left - 1

    print(total)


if __name__ == "__main__":
    main()
