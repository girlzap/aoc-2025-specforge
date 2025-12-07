import sys

def count_fresh_ids(input_text: str) -> int:
    """
    Given full database input text, return the number of available
    ingredient IDs that fall within at least one fresh range.
    """

    lines = [line.strip() for line in input_text.splitlines()]

    ranges = []
    available = []
    blank_found = False

    for line in lines:
        if line == "":
            blank_found = True
            continue

        if not blank_found:
            start, end = line.split("-")
            ranges.append((int(start), int(end)))
        else:
            available.append(int(line))

    merged = merge_ranges(ranges)

    fresh_count = 0
    for ingredient_id in available:
        if is_in_any_range(ingredient_id, merged):
            fresh_count += 1

    return fresh_count


def merge_ranges(ranges):
    if not ranges:
        return []

    ranges.sort(key=lambda r: r[0])
    merged = [ranges[0]]

    for current in ranges[1:]:
        last_start, last_end = merged[-1]
        curr_start, curr_end = current

        if curr_start <= last_end:
            merged[-1] = (last_start, max(last_end, curr_end))
        else:
            merged.append(current)

    return merged


def is_in_any_range(value, ranges):
    for start, end in ranges:
        if start <= value <= end:
            return True
    return False


if __name__ == "__main__":
    input_text = sys.stdin.read()  # <-- read everything
    print(count_fresh_ids(input_text))
    
    # To run: python3 part1.py < day5-input.txt
