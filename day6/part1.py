import sys
import re
from functools import reduce
from operator import add, mul

def main():
    lines = [line.rstrip("\n") for line in sys.stdin.readlines()]
    if not lines:
        print(0)
        return

    # Normalize row lengths by padding with spaces
    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]

    height = len(grid)
    last_row = height - 1  # operator row

    problem_columns = []
    col = 0

    # Identify contiguous column blocks (problems)
    while col < width:
        if all(grid[r][col] == " " for r in range(height)):
            col += 1
            continue

        # Start of a block
        start = col
        while col < width and not all(grid[r][col] == " " for r in range(height)):
            col += 1
        end = col  # one past the last column of the block
        problem_columns.append((start, end))

    total = 0

    for start, end in problem_columns:
        # Extract operator (exactly one non-space expected)
        op_chars = [grid[last_row][c] for c in range(start, end) if grid[last_row][c] in "+*"]
        if len(op_chars) != 1:
            raise ValueError(f"Invalid operator block in columns {start}-{end}")
        op = op_chars[0]

        # Extract numbers
        numbers = []
        for r in range(height - 1):  # everything except operator row
            segment = grid[r][start:end]
            digits = re.findall(r"\d+", segment)
            if digits:
                num = int("".join(digits))
                numbers.append(num)

        if not numbers:
            raise ValueError(f"No numbers found in block {start}-{end}")

        # Compute result for this problem
        if op == "+":
            result = sum(numbers)
        else:  # op == "*"
            result = reduce(mul, numbers, 1)

        total += result

    print(total)

if __name__ == "__main__":
    main()
