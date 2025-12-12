import sys

points = []

# Read red-tile coordinates from stdin
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    x, y = map(int, line.split(","))
    points.append((x, y))

n = len(points)
max_area = 0

# Check all unordered pairs of points
for i in range(n):
    x1, y1 = points[i]
    for j in range(i + 1, n):
        x2, y2 = points[j]

        width = abs(x1 - x2) + 1   # inclusive width in tiles
        height = abs(y1 - y2) + 1  # inclusive height in tiles

        area = width * height
        if area > max_area:
            max_area = area

print(max_area)
