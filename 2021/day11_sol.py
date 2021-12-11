import numpy as np


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    output = []

    for line in data:
        output.append([int(i) for i in line])

    return np.array(output)


def simulate_step(state):
    new_state = state + 1

    flashed = new_state > 9

    old_flashed = np.zeros_like(flashed)

    while not np.all(old_flashed == flashed):
        flashed_indices = np.transpose(np.nonzero(flashed != old_flashed))

        for i, j in flashed_indices:
            new_state[
                max(0, i - 1) : min(new_state.shape[0], i + 2),
                max(0, j - 1) : min(new_state.shape[0], j + 2),
            ] += 1

        old_flashed = flashed
        flashed = new_state > 9

    new_state[flashed] = 0

    return new_state, np.sum(flashed)


state = parse_data(read_input("day11"))

# Part 1

num_flashes = 0
NUM_STEPS = 100

for i in range(NUM_STEPS):
    state, flashed = simulate_step(state)
    num_flashes += flashed

print(f"Number of flashes in {NUM_STEPS} steps: {num_flashes}")

# Part 2

current_step = NUM_STEPS

while not np.all(state == 0):
    state, _ = simulate_step(state)
    current_step += 1

print(f"First step when all octopuses flash: {current_step}")
