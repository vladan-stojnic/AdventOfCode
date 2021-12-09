from collections import deque
from math import prod


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    output = []

    for line in data:
        output.append([int(v) for v in line])

    return output


def get_neighbors(data, i, j):
    neighbors = []

    if i - 1 >= 0:
        neighbors.append((data[i - 1][j], (i - 1, j)))

    if i + 1 < len(data):
        neighbors.append((data[i + 1][j], (i + 1, j)))

    if j - 1 >= 0:
        neighbors.append((data[i][j - 1], (i, j - 1)))

    if j + 1 < len(data[0]):
        neighbors.append((data[i][j + 1], (i, j + 1)))

    return neighbors


def get_for_basin(val, neighbors, selected):
    output = []

    for n in neighbors:
        if n[0] < 9 and n[0] > val and n[1] not in selected:
            output.append(n)
            selected.add(n[1])

    return output


data = read_input("day9")

data = parse_data(data)

# Part 1

sum_of_lows = 0

for i, row in enumerate(data):
    for j, val in enumerate(row):
        neighbors = get_neighbors(data, i, j)

        if all(map(lambda x: x[0] > val, neighbors)):
            sum_of_lows += val + 1

print(f"Sum of low points: {sum_of_lows}")

# Part 2

basins = []

for i, row in enumerate(data):
    for j, val in enumerate(row):
        neighbors = get_neighbors(data, i, j)

        if all(map(lambda x: x[0] > val, neighbors)):
            basin_size = 1
            selected = set([(i, j)])

            possible_to_select = deque(get_for_basin(val, neighbors, selected))

            while len(possible_to_select) > 0:
                basin_size += 1

                new_val, (new_i, new_j) = possible_to_select.popleft()

                new_neighbors = get_neighbors(data, new_i, new_j)

                new_basin_elems = get_for_basin(
                    new_val, new_neighbors, selected
                )

                possible_to_select.extend(new_basin_elems)

            basins.append(basin_size)

multiplied_sizes = prod(sorted(basins)[-3:])

print(f"Multiplied sizes of three biggest basins: {multiplied_sizes}")
