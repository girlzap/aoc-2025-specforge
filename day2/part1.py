import sys

def sum_invalid_ids(line: str) -> int:
    line = line.strip()
    if not line:
        return 0

    total_sum = 0

    # Parse ranges: "start-end,start-end,..."
    for part in line.split(','):
        part = part.strip()
        if not part:
            continue

        start_str, end_str = part.split('-')
        start = int(start_str)
        end = int(end_str)

        # Ensure start <= end (just in case)
        if start > end:
            start, end = end, start

        # Explore by digit length to avoid brute-forcing every integer
        min_len = len(str(start))
        max_len = len(str(end))

        for L in range(min_len, max_len + 1):
            # Only even-length numbers can be "XX" style
            if L % 2 != 0:
                continue

            # Restrict to numbers with this digit length within the range
            length_low = max(start, 10 ** (L - 1))
            length_high = min(end, 10 ** L - 1)

            if length_low > length_high:
                continue  # no numbers of this length in this range

            half_len = L // 2

            # The number has the form: n = base * 10^half_len + base
            # base has half_len digits and no leading zero.
            factor = 10 ** half_len + 1

            # Solve:
            #   length_low <= base * factor <= length_high
            base_min = (length_low + factor - 1) // factor  # ceil division
            base_max = length_high // factor                # floor division

            # Constrain base to have correct digit length (no leading zero)
            base_min = max(base_min, 10 ** (half_len - 1))
            base_max = min(base_max, 10 ** half_len - 1)

            if base_min > base_max:
                continue

            # Now generate all invalid IDs in this length/range
            pow10_half = 10 ** half_len
            for base in range(base_min, base_max + 1):
                n = base * pow10_half + base
                total_sum += n

    return total_sum


def main():
    line = sys.stdin.readline()
    result = sum_invalid_ids(line)
    print(result)


if __name__ == "__main__":
    main()

# To run: python3 part1.py < day2-input.txt