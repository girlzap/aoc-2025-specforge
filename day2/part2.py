import sys
from math import isqrt

def is_invalid_id(n: int) -> bool:
    s = str(n)
    L = len(s)

    # Single-digit numbers cannot be invalid
    if L == 1:
        return False

    # Find divisors of L (pattern length)
    # Pattern length must be < L so that repeats >= 2
    for d in range(1, L):
        if L % d == 0:
            p = s[:d]
            if p * (L // d) == s:
                return True

    return False


def sum_invalid_ids(line: str) -> int:
    total = 0
    line = line.strip()

    for token in line.split(','):
        if not token:
            continue
        start_str, end_str = token.split('-')
        start = int(start_str)
        end = int(end_str)

        # Ensure order
        if start > end:
            start, end = end, start

        for n in range(start, end + 1):
            if is_invalid_id(n):
                total += n

    return total


def main():
    line = sys.stdin.readline()
    print(sum_invalid_ids(line))


if __name__ == "__main__":
    main()
