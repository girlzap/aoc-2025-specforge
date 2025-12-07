import sys

def main():
    grid = [list(line.rstrip("\n")) for line in sys.stdin.readlines()]
    if not grid:
        print(0)
        return

    rows = len(grid)
    cols = max(len(row) for row in grid)

    # Normalize width
    for r in range(rows):
        if len(grid[r]) < cols:
            grid[r] += ['.'] * (cols - len(grid[r]))

    # Find S
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                s_row, s_col = r, c
                break

    # Beam starts below S
    beams = []
    if s_row + 1 < rows:
        beams.append((s_row + 1, s_col))

    visited = set()      # <<< CRUCIAL FIX
    split_count = 0

    while beams:
        new_beams = []
        for (r, c) in beams:

            # Skip if we've seen this beam position before
            if (r, c) in visited:
                continue
            visited.add((r, c))

            nr = r + 1  # move DOWN

            if nr >= rows:
                continue  # off-grid

            cell = grid[nr][c]

            if cell == '.':
                new_beams.append((nr, c))

            elif cell == '^':
                split_count += 1

                # Left beam at SAME ROW as splitter entry
                if c - 1 >= 0:
                    new_beams.append((r, c - 1))

                # Right beam at SAME ROW as splitter entry
                if c + 1 < cols:
                    new_beams.append((r, c + 1))

            else:
                new_beams.append((nr, c))

        beams = new_beams

    print(split_count)


if __name__ == "__main__":
    main()
