def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    right_cucumbers = set()
    down_cucumbers = set()

    height = len(data)
    width = None

    for i, line in enumerate(data):
        width = len(line)
        for j, value in enumerate(line):
            if value == ">":
                right_cucumbers.add((i, j))
            elif value == "v":
                down_cucumbers.add((i, j))

    return right_cucumbers, down_cucumbers, height, width


def get_next_position(cucumber_type, i, j, height, width):
    if cucumber_type == ">":
        return i, (j + 1) % width
    else:
        return (i + 1) % height, j


def make_step(right_cucumbers, down_cucumbers, height, width):
    new_right = set()

    for i, j in right_cucumbers:
        new_pos = get_next_position(">", i, j, height, width)

        if new_pos not in right_cucumbers and new_pos not in down_cucumbers:
            new_right.add(new_pos)
        else:
            new_right.add((i, j))

    right_cucumbers = new_right

    new_down = set()

    for i, j in down_cucumbers:
        new_pos = get_next_position("v", i, j, height, width)

        if new_pos not in right_cucumbers and new_pos not in down_cucumbers:
            new_down.add(new_pos)
        else:
            new_down.add((i, j))

    return right_cucumbers, new_down


def play(data):
    right_cucumbers, down_cucumbers, height, width = parse_data(data)

    old_right, old_down = None, None

    steps = 0

    while old_right != right_cucumbers or old_down != down_cucumbers:
        old_right = right_cucumbers
        old_down = down_cucumbers
        right_cucumbers, down_cucumbers = make_step(
            right_cucumbers, down_cucumbers, height, width
        )

        steps += 1

    return steps


data = read_input("day25")

print(f"Number of steps until cucumbers stop moving: {play(data)}")
