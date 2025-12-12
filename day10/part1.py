import sys
import re
from collections import deque

pattern_re = re.compile(r'\[([.#]+)\]')
buttons_re = re.compile(r'\(([^)]*)\)')

def parse_machine(line):
    """
    Parse a single machine line into:
      - target_mask: int bitmask of desired lights (1 = on)
      - buttons: list of int bitmasks, each representing a button toggle pattern
    """
    line = line.strip()
    if not line:
        return None

    m = pattern_re.search(line)
    if not m:
        return None
    pattern = m.group(1)
    L = len(pattern)

    # Build target mask
    target_mask = 0
    for i, ch in enumerate(pattern):
        if ch == '#':
            target_mask |= (1 << i)

    # Parse all button groups
    buttons = []
    groups = buttons_re.findall(line)
    for g in groups:
        g = g.strip()
        if not g:
            continue
        mask = 0
        # Allow optional spaces in the list, so strip each piece
        for part in g.split(','):
            part = part.strip()
            if not part:
                continue
            idx = int(part)
            if idx < 0 or idx >= L:
                # Index out of range, but puzzle shouldn't do this
                continue
            mask |= (1 << idx)
        buttons.append(mask)

    return target_mask, buttons, L

def min_presses_for_machine(target_mask, buttons, L):
    """
    Find minimal number of button presses to reach target_mask
    starting from 0, given a list of button bitmasks and number
    of lights L.

    Uses whichever of:
      - subset DP over buttons (complexity ~ 2^B)
      - BFS over states (complexity ~ 2^L)
    is cheaper.
    """
    B = len(buttons)

    # Trivial case: already all off
    if target_mask == 0:
        return 0

    if B == 0:
        # No buttons; if target is not zero, it's unsolvable in theory.
        # Puzzle likely doesn't include this case; return a large number.
        return float('inf')

    # Decide strategy based on which space is smaller: subsets (2^B) vs states (2^L)
    if B <= L:
        # Strategy 1: enumerate all subsets of buttons using DP
        # dp[mask] = resulting state from pressing subset 'mask'
        # We only care when dp[mask] == target_mask, and track minimal popcount(mask)
        full = 1 << B
        dp = [0] * full
        best = float('inf')

        for mask in range(1, full):
            lsb = mask & -mask
            idx = (lsb.bit_length() - 1)  # which button was added
            prev = mask ^ lsb
            dp[mask] = dp[prev] ^ buttons[idx]

            if dp[mask] == target_mask:
                presses = mask.bit_count()
                if presses < best:
                    best = presses

        return best
    else:
        # Strategy 2: BFS over states in {0..2^L-1}
        start = 0
        target = target_mask
        visited = set([start])
        q = deque()
        q.append((start, 0))

        while q:
            state, dist = q.popleft()
            for btn in buttons:
                ns = state ^ btn
                if ns == target:
                    return dist + 1
                if ns not in visited:
                    visited.add(ns)
                    q.append((ns, dist + 1))

        # If unreachable (shouldn't happen in puzzle input)
        return float('inf')

def main():
    total_presses = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parsed = parse_machine(line)
        if parsed is None:
            continue

        target_mask, buttons, L = parsed
        presses = min_presses_for_machine(target_mask, buttons, L)
        if presses == float('inf'):
            # If unsolvable, you might want to handle differently,
            # but AoC puzzles should avoid this.
            # For safety, we can just skip or treat as 0; here we skip.
            continue

        total_presses += presses

    print(total_presses)

if __name__ == "__main__":
    main()
