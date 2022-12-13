import numpy as np


def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    # data = data.splitlines()

    return data


def parse_data(data):
    def split_and_eval(pair):
        splitted = pair.splitlines()

        return eval(splitted[0]), eval(splitted[1])

    pairs = data.split("\n\n")

    return [split_and_eval(pair) for pair in pairs]


def parse_data_part2(data):
    packets = data.splitlines()

    return [eval(packet) for packet in packets if packet != ""]


def compare_two_numbers(val1, val2):
    if val1 < val2:
        return True
    elif val2 < val1:
        return False
    else:
        return None


def compare_two_lists(l1, l2):
    min_len = min(len(l1), len(l2))

    for idx in range(min_len):
        val1, val2 = l1[idx], l2[idx]
        if isinstance(val1, list):
            if isinstance(val2, list):
                result = compare_two_lists(val1, val2)
            else:
                result = compare_two_lists(val1, [val2])
        else:
            if isinstance(val2, list):
                result = compare_two_lists([val1], val2)
            else:
                result = compare_two_numbers(val1, val2)
        if result is not None:
            return result

    if min_len == len(l1) and min_len < len(l2):
        return True

    if min_len == len(l2) and min_len < len(l1):
        return False

    return None


data = read_input("day13")

# Part 1
parsed_data = parse_data(data)

sum_of_indices = 0

for idx, pair in enumerate(parsed_data, start=1):
    if compare_two_lists(*pair):
        sum_of_indices += idx

print(f"Sum of indices of correctly ordered packets: {sum_of_indices}")

# Part 2

parsed_data = parse_data_part2(data)

# add wanted packets
parsed_data.append([[2]])
parsed_data.append([[6]])

pairwise_comparisons = np.zeros(
    (len(parsed_data), len(parsed_data)), dtype=np.uint8
)

for idx_left in range(len(parsed_data) - 1):
    for idx_right in range(idx_left + 1, len(parsed_data)):
        out = compare_two_lists(parsed_data[idx_left], parsed_data[idx_right])

        pairwise_comparisons[idx_left, idx_right] = int(out)
        pairwise_comparisons[idx_right, idx_left] = int(not out)

print(
    f"Product of indices of new packets: {np.prod((np.sum(pairwise_comparisons, axis=0) + 1)[-2:])}"
)
