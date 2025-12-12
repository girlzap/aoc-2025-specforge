import sys

# ---------- Union-Find (Disjoint Set Union) ----------
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False  # no merge
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


# ---------- Read Input ----------
points = []
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    x, y, z = map(int, line.split(","))
    points.append((x, y, z))

N = len(points)

# ---------- Build pairwise distances ----------
pairs = []
for i in range(N):
    x1, y1, z1 = points[i]
    for j in range(i + 1, N):
        x2, y2, z2 = points[j]
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        dist2 = dx*dx + dy*dy + dz*dz
        pairs.append((dist2, i, j))

# ---------- Sort all pairs by distance ----------
pairs.sort(key=lambda x: x[0])

# ---------- Process pairs until all nodes connected ----------
dsu = DSU(N)
component_count = N
last_merge_pair = None

for dist2, i, j in pairs:
    if dsu.union(i, j):          # if this actually merges components
        component_count -= 1
        last_merge_pair = (i, j)
        if component_count == 1: # fully connected!
            break

# ---------- Final computation ----------
i, j = last_merge_pair
x1 = points[i][0]
x2 = points[j][0]
answer = x1 * x2

print(answer)
