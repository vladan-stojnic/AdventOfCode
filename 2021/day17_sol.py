from math import ceil, sqrt


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    return data


def parse_data(data):
    splitted = data.split(",")
    range_x = splitted[0].split("=")[1]
    range_y = splitted[1].split("=")[1]

    x_target = tuple(int(v) for v in range_x.split(".."))
    y_target = tuple(int(v) for v in range_y.split(".."))

    return x_target, y_target


def find_min_x_v(x_target):
    val = 2 * x_target[0]
    return ceil((-1 + sqrt(1 + 4 * val)) / 2)


def find_max_y_v(y_target):
    val = y_target[0]
    return -val - 1


def max_height(v_y):
    return (v_y * (v_y + 1)) // 2


def decreasing_generator(start):
    x = start

    while True:
        yield x
        x -= 1


def needed_steps_x(v, target):
    min_s, max_s = None, None

    s = 0

    for st, i in enumerate(range(v, 0, -1), start=1):
        s += i

        if target[0] <= s <= target[1]:
            if not min_s:
                min_s = st
        elif s > target[1]:
            if not max_s:
                max_s = st - 1
                break

    return min_s, max_s


def needed_steps_y(v, target):
    min_s, max_s = None, None

    s = 0

    for st, i in enumerate(decreasing_generator(v), start=1):
        s += i

        if target[0] <= s <= target[1]:
            if not min_s:
                min_s = st
        elif s < target[0]:
            if not max_s:
                max_s = st - 1
                break

    return min_s, max_s


def find_matching_speeds(steps, y_steps):
    out = []

    if not steps[0]:
        return out

    for y_speed, step_range in y_steps.items():
        if not step_range[0]:
            continue

        if not steps[1]:
            if (step_range[0] >= steps[0]) or (step_range[1] >= steps[0]):
                out.append(y_speed)
        else:
            if set(range(steps[0], steps[1] + 1)).intersection(
                set(range(step_range[0], step_range[1] + 1))
            ):
                out.append(y_speed)

    return out


data = read_input("day17")
x_target, y_target = parse_data(data)

# Part 1

v_y = find_max_y_v(y_target)

print(f"Maximal possible hight: {max_height(v_y)}")

# Part 2

x_steps = {}

for i in range(find_min_x_v(x_target), x_target[1] + 1):
    x_steps[i] = needed_steps_x(i, x_target)

y_steps = {}

for i in range(find_max_y_v(y_target), y_target[0] - 1, -1):
    y_steps[i] = needed_steps_y(i, y_target)

possible_speeds = set()

for x_speed, steps in x_steps.items():
    possible_y_speeds = find_matching_speeds(steps, y_steps)
    for y_speed in possible_y_speeds:
        possible_speeds.add((x_speed, y_speed))

print(f"Numer of possible initialy velocities: {len(possible_speeds)}")
