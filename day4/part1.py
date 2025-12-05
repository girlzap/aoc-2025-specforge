import sys

def count_accessible_rolls(grid_text: str) -> int:
    # Parse grid into a 2D list of characters
    grid = [list(line) for line in grid_text.strip().splitlines()]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # 8 possible neighbor directions
    directions = [
        (-1,  0), (-1,  1), (0, 1), (1, 1),
        (1,   0), (1, -1), (0, -1), (-1, -1)
    ]

    accessible_count = 0

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
                accessible_count += 1

    return accessible_count


if __name__ == "__main__":
    # Read ALL input from stdin — works for AoC multi-line puzzles
    grid_text = sys.stdin.read()
    print(count_accessible_rolls(grid_text))

# To run: python3 part1.py < day4-input.txt