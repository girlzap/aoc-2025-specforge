def count_zero_landings(instructions):
    pos = 50
    zero_count = 0

    for instr in instructions:
        direction = instr[0]
        amount = int(instr[1:])

        if direction == 'R':
            pos = (pos + amount) % 100
        else:  # direction == 'L'
            pos = (pos - amount) % 100

        if pos == 0:
            zero_count += 1

    return zero_count

with open("day1/day1-input.txt") as f:
    instructions = [line.strip() for line in f if line.strip()]

print(count_zero_landings(instructions)) 
