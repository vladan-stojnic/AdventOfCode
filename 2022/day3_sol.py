from itertools import tee


def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()

    return data


def get_compartments(backpack):
    mid = len(backpack) // 2

    return set(backpack[:mid]), set(backpack[mid:])


def get_priority(val):
    if val.islower():
        return ord(val) - 97 + 1
    else:
        return ord(val) - 65 + 27


def intersection(first, *others):
    return set(first).intersection(*others)


data = read_input("day3")

# Part 1
data_per_compartment = [get_compartments(b) for b in data]

error_item = [b[0].intersection(b[1]) for b in data_per_compartment]

priorities = [get_priority(list(val)[0]) for val in error_item]

print(f"Sum of priorities: {sum(priorities)}")

# Part 2
groups = [data[i * 3 : (i + 1) * 3] for i in range(len(data) // 3)]
group_items = [intersection(g[0], *g[1:]) for g in groups]

priorities = [get_priority(list(val)[0]) for val in group_items]

print(f"Sum of priorities: {sum(priorities)}")
