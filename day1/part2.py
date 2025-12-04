def count_zero_hits(instructions):
    N = 100          # dial size
    pos = 50         # starting position
    zero_hits = 0

    for inst in instructions:
        direction = inst[0]
        steps = int(inst[1:])

        if direction == 'R':
            # First time (in steps) we would land on 0
            if pos == 0:
                t1 = N
            else:
                t1 = N - pos

            if steps >= t1:
                zero_hits += 1 + (steps - t1) // N

            # Update final position
            pos = (pos + steps) % N

        elif direction == 'L':
            # First time (in steps) we would land on 0
            if pos == 0:
                t1 = N
            else:
                t1 = pos

            if steps >= t1:
                zero_hits += 1 + (steps - t1) // N

            # Update final position
            pos = (pos - steps) % N

        else:
            raise ValueError(f"Invalid direction: {direction}")

    return zero_hits



with open("day1/day1-input.txt") as f:
    instructions = [line.strip() for line in f if line.strip()]

print(count_zero_hits(instructions)) 
