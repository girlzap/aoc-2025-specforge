import sys

def best_two_digit(bank: str) -> int:
    digits = [int(c) for c in bank.strip()]
    n = len(digits)

    best = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            value = digits[i] * 10 + digits[j]
            if value > best:
                best = value
    return best


def main():
    total = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        total += best_two_digit(line)
    print(total)


if __name__ == "__main__":
    main()

    # To run: python3 part1.py < day3-input.txt
