import sys
import math

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
            return False  # already connected
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

# ---------- Process first 1000 pairs ----------
K = 1000
dsu = DSU(N)

limit = min(K, len(pairs))
for k in range(limit):
    _, i, j = pairs[k]
    dsu.union(i, j)

# ---------- Compute component sizes ----------
comp_sizes = {}
for i in range(N):
    root = dsu.find(i)
    comp_sizes[root] = comp_sizes.get(root, 0) + 1

sizes = sorted(comp_sizes.values(), reverse=True)

# If fewer than 3 components exist, pad with 1s (AoC input will not need this)
while len(sizes) < 3:
    sizes.append(1)

# ---------- Final answer ----------
answer = sizes[0] * sizes[1] * sizes[2]
print(answer)
