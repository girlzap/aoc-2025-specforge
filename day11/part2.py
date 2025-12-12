import sys
from collections import defaultdict

def main():
    graph = defaultdict(list)

    # ----- Parse input -----
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

        # Ensure all nodes exist in graph structure
        if src not in graph:
            graph[src] = graph[src]  # force creation
        for d in dests:
            if d not in graph:
                graph[d] = []

    # If svr doesn't exist at all
    if "svr" not in graph:
        print(0)
        return

    memo = {}        # (node, seen_dac, seen_fft) -> number of valid paths
    visiting = set() # for cycle detection on same state

    def count_paths(node, seen_dac, seen_fft):
        state = (node, seen_dac, seen_fft)

        # memoized?
        if state in memo:
            return memo[state]

        # base case: reached out
        if node == "out":
            # must satisfy both-visited requirement
            return 1 if (seen_dac and seen_fft) else 0

        # no outgoing edges => dead end
        if not graph[node]:
            return 0

        # cycle detection in this specific flag-state
        if state in visiting:
            # AoC won't require infinite path counting,
            # so treat a cycle as contributing 0 valid paths.
            return 0

        visiting.add(state)

        # update visitation flags
        next_seen_dac = seen_dac or (node == "dac")
        next_seen_fft = seen_fft or (node == "fft")

        total = 0
        for child in graph[node]:
            total += count_paths(child, next_seen_dac, next_seen_fft)

        visiting.remove(state)
        memo[state] = total
        return total

    # compute total qualifying paths
    result = count_paths("svr", False, False)
    print(result)

if __name__ == "__main__":
    main()
