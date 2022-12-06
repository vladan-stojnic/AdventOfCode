from collections import deque


def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()

    return data


def parse_data(data):
    is_moves = False

    moves = []
    stacks = []
    stack_lines = []
    for line in data:
        if line == "":
            is_moves = True
            continue

        if is_moves:
            splitted_line = line.split(" ")
            moves.append(
                (
                    int(splitted_line[1]),
                    int(splitted_line[3]) - 1,
                    int(splitted_line[5]) - 1,
                )
            )
        else:
            stack_lines.append(line)
    # 1, 5, 9
    for s in stack_lines[-1].split(" "):
        if s != "":
            stacks.append([])
    for line in stack_lines[::-1][1:]:
        for idx, crate in enumerate(line[1::4]):
            if crate != " ":
                stacks[idx].append(crate)

    return [deque(s) for s in stacks], moves


def execute_move(stacks, move, reverse_stacks=True):
    num_elem, origin, destination = move

    taken = []
    for _ in range(num_elem):
        taken.append(stacks[origin].pop())

    if reverse_stacks:
        step = 1
    else:
        step = -1

    stacks[destination].extend(taken[::step])

    return stacks


def read_message(stacks):
    message = ""

    for s in stacks:
        message += s[-1]

    return message


data = read_input("day5")

# Part 1
stacks, moves = parse_data(data)

for move in moves:
    execute_move(stacks, move)

print(f"Message is: {read_message(stacks)}")

# Part 2
stacks, moves = parse_data(data)

for move in moves:
    execute_move(stacks, move, False)

print(f"Message is: {read_message(stacks)}")
