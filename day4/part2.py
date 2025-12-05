import sys

def count_removed_rolls(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    # 8-direction adjacency
    directions = [
        (-1,  0), (-1,  1), ( 0, 1), ( 1, 1),
        ( 1,  0), ( 1, -1), ( 0, -1), (-1, -1)
    ]

    total_removed = 0

    # Convert grid to a mutable structure
    grid = [list(row) for row in grid]

    while True:
        to_remove = []

        # Step 1: Compute adjacency for all rolls
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '@':
                    continue

                neighbor_count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == '@':
                            neighbor_count += 1

                if neighbor_count < 4:
                    to_remove.append((r, c))

        # Step 2: Stop if nothing to remove
        if not to_remove:
            break

        # Step 3: Remove all accessible rolls simultaneously
        for r, c in to_remove:
            grid[r][c] = '.'

        total_removed += len(to_remove)

    return total_removed


def main():
    grid = [line.rstrip("\n") for line in sys.stdin if line.strip()]
    print(count_removed_rolls(grid))


if __name__ == "__main__":
    main()
