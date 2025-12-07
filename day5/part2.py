import sys

def merge_ranges(ranges):
    """Merge overlapping or adjacent integer ranges."""
    if not ranges:
        return []

    # Sort by starting value
    ranges.sort(key=lambda r: r[0])
    merged = [ranges[0]]

    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]

        # Overlap or adjacency
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def main():
    lines = [line.strip() for line in sys.stdin.readlines()]

    ranges = []
    for line in lines:
        if line == "":
            break  # Ignore everything after the blank line
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    merged = merge_ranges(ranges)

    total = sum((end - start + 1) for start, end in merged)

    print(total)


if __name__ == "__main__":
    main()
