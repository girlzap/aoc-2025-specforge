import sys

TARGET = 12  # must pick exactly 12 digits

def best_12_digit_number(bank: str) -> int:
    bank = bank.strip()
    n = len(bank)
    result_digits = []
    start = 0

    for _ in range(TARGET):
        remaining_needed = TARGET - len(result_digits)
        # We may choose the next digit from start .. max_pick
        max_pick = n - remaining_needed

        best_digit = '0'
        best_pos = start

        # scan to find the maximum digit available
        for pos in range(start, max_pick + 1):
            d = bank[pos]
            if d > best_digit:
                best_digit = d
                best_pos = pos

                # optimization: '9' is the highest possible, stop early
                if best_digit == '9':
                    break

        result_digits.append(best_digit)
        start = best_pos + 1

    # Convert the 12-digit string to int
    return int("".join(result_digits))


def main():
    total = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        total += best_12_digit_number(line)
    print(total)


if __name__ == "__main__":
    main()
