import sys
from collections import defaultdict

def main():
    graph = defaultdict(list)

    # Parse input
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if ':' not in line:
            continue

        src, rest = line.split(':', 1)
        src = src.strip()
        dests = rest.strip().split()
        for d in dests:
            graph[src].append(d)

        # Make sure every mentioned node exists in the graph
        if src not in graph:
            graph[src] = graph[src]  # touching ensures existence
        for d in dests:
            if d not in graph:
                graph[d] = []

    memo = {}       # node -> number of paths to 'out'
    visiting = set()  # for cycle detection

    def count_paths(node):
        # Memoized result
        if node in memo:
            return memo[node]

        # Base case: found 'out'
        if node == "out":
            return 1

        # Dead end
        if not graph[node]:
            return 0

        # Detect cycles
        if node in visiting:
            # If a cycle is reachable, AoC guarantees it's not an infinite-path case.
            # Treat as producing 0 paths to avoid infinite recursion.
            return 0

        visiting.add(node)
        total = 0
        for nxt in graph[node]:
            total += count_paths(nxt)
        visiting.remove(node)

        memo[node] = total
        return total

    # If 'you' isn't present, answer is 0
    if "you" not in graph:
        print(0)
        return

    print(count_paths("you"))

if __name__ == "__main__":
    main()
