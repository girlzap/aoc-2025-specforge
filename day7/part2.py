import sys

def main():
    grid = [list(line.rstrip("\n")) for line in sys.stdin.readlines()]
    if not grid:
        print(0)
        return

    rows = len(grid)
    cols = max(len(row) for row in grid)

    # Normalize row widths
    for r in range(rows):
        if len(grid[r]) < cols:
            grid[r] += ['.'] * (cols - len(grid[r]))

    # Locate S
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                s_row, s_col = r, c
                break
        else:
            continue
        break

    # dp[r][c] = number of timelines currently at (r, c)
    dp = [[0] * cols for _ in range(rows)]

    start_r = s_row + 1
    if start_r >= rows:
        print(1)
        return

    dp[start_r][s_col] = 1
    leaf_count = 0

    # Process each row top → bottom
    for r in range(start_r, rows):
        for c in range(cols):
            ways = dp[r][c]
            if ways == 0:
                continue

            nr = r + 1

            # Exiting bottom → leaf timelines
            if nr >= rows:
                leaf_count += ways
                continue

            cell_below = grid[nr][c]

            if cell_below == "^":
                # Split left
                if c - 1 >= 0:
                    dp[nr][c - 1] += ways
                else:
                    leaf_count += ways

                # Split right
                if c + 1 < cols:
                    dp[nr][c + 1] += ways
                else:
                    leaf_count += ways

            else:
                # Normal downward fall
                dp[nr][c] += ways

    print(leaf_count)


if __name__ == "__main__":
    main()
