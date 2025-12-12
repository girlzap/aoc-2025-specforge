import sys

# Read red-tile coordinates from stdin
points = []
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    x, y = map(int, line.split(","))
    points.append((x, y))

n = len(points)
if n < 2:
    print(0)
    sys.exit(0)

# Pre-split x and y for speed
xs = [p[0] for p in points]
ys = [p[1] for p in points]

# Build polygon edges from consecutive red tiles (wrap around)
edges = []
for i in range(n):
    x1, y1 = points[i]
    x2, y2 = points[(i + 1) % n]
    edges.append((x1, y1, x2, y2))


def rectangle_valid(i, j):
    """
    Check if the axis-aligned rectangle with opposite red corners
    points[i] and points[j] is valid: i.e., no polygon edge crosses
    the *interior* of the rectangle.
    """
    x1, y1 = xs[i], ys[i]
    x2, y2 = xs[j], ys[j]

    if x1 <= x2:
        rx_min, rx_max = x1, x2
    else:
        rx_min, rx_max = x2, x1

    if y1 <= y2:
        ry_min, ry_max = y1, y2
    else:
        ry_min, ry_max = y2, y1

    # If rectangle is actually a point, it's trivially valid but area=1.
    # The crossing test below naturally handles all cases anyway.
    for ex1, ey1, ex2, ey2 in edges:
        if ex1 == ex2:
            # Vertical edge
            x = ex1
            # Must be strictly between left and right sides to cross interior
            if not (rx_min < x < rx_max):
                continue
            # Check open interval overlap in y
            if ey1 <= ey2:
                ey_min, ey_max = ey1, ey2
            else:
                ey_min, ey_max = ey2, ey1

            # Open interval intersection: (ey_min, ey_max) ∩ (ry_min, ry_max) ≠ ∅
            if max(ey_min, ry_min) < min(ey_max, ry_max):
                return False
        else:
            # Horizontal edge
            y = ey1
            # Must be strictly between bottom and top to cross interior
            if not (ry_min < y < ry_max):
                continue
            if ex1 <= ex2:
                ex_min, ex_max = ex1, ex2
            else:
                ex_min, ex_max = ex2, ex1

            # Open interval intersection: (ex_min, ex_max) ∩ (rx_min, rx_max) ≠ ∅
            if max(ex_min, rx_min) < min(ex_max, rx_max):
                return False

    return True


# Build all unordered pairs of red tiles with their rectangle areas
pairs = []
for i in range(n):
    x1, y1 = xs[i], ys[i]
    for j in range(i + 1, n):
        x2, y2 = xs[j], ys[j]
        width = abs(x1 - x2) + 1
        height = abs(y1 - y2) + 1
        area = width * height
        pairs.append((area, i, j))

# Sort by area descending so we can early-exit on the first valid rectangle
pairs.sort(reverse=True, key=lambda t: t[0])

max_area = 0

for area, i, j in pairs:
    # If we already found a rectangle with this area or larger, we can stop
    if area <= max_area:
        break
    if rectangle_valid(i, j):
        max_area = area
        break

print(max_area)
