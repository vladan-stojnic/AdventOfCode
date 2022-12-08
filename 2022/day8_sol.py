import numpy as np


def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()

    return data


def parse_data(data):
    return np.array([np.array([int(v) for v in l]) for l in data])


def print_matrix(data):
    for row in data:
        for col in row:
            print(col, end="")
        print()


def find_visible(data):
    visible = np.zeros(data.shape, dtype=bool)
    for i, row in enumerate(data[1:-1], start=1):
        for j, val in enumerate(row[1:-1], start=1):
            if (
                val > np.max(row[:j])
                or val > np.max(row[j + 1 :])
                or val > np.max(data[:i, j])
                or val > np.max(data[i + 1 :, j])
            ):
                visible[i, j] = True

    visible[0, :] = True
    visible[:, 0] = True
    visible[-1, :] = True
    visible[:, -1] = True

    return visible


def calculate_scenic_score(data):
    scenic_scores = np.zeros(data.shape, dtype=np.uint64)

    for i in range(1, data.shape[0] - 1):
        for j in range(1, data.shape[1] - 1):
            val = data[i, j]
            up = 0
            for dx in range(i - 1, -1, -1):
                up += 1
                if val <= data[dx, j]:
                    break
            down = 0
            for dx in range(i + 1, data.shape[0]):
                down += 1
                if val <= data[dx, j]:
                    break
            left = 0
            for dy in range(j - 1, -1, -1):
                left += 1
                if val <= data[i, dy]:
                    break
            right = 0
            for dy in range(j + 1, data.shape[1]):
                right += 1
                if val <= data[i, dy]:
                    break
            scenic_scores[i, j] = left * right * up * down

    return scenic_scores


data = read_input("day8")

data = parse_data(data)

# Part 1
visible = find_visible(data)

print(f"Number of visible trees: {np.sum(visible)}")

# Part 2
scenic_scores = calculate_scenic_score(data)

print(f"Maximum scenic score: {np.max(scenic_scores)}")
