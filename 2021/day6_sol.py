from collections import Counter


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.split(",")

    data = [int(d) for d in data]

    return data


def simulate_day(state):
    new_state = {i: 0 for i in range(9)}

    for i in range(8):
        new_state[i] = state[i + 1]

    new_state[8] = state[0]
    new_state[6] += state[0]

    return new_state


data = read_input("day6")

current_state = Counter(data)

# Part 1

NUM_DAYS_1 = 80

for _ in range(NUM_DAYS_1):
    current_state = simulate_day(current_state)

print(
    f"Size of population after {NUM_DAYS_1} days: {sum(current_state.values())}"
)

# Part 2

NUM_DAYS_2 = 256

for _ in range(NUM_DAYS_1, NUM_DAYS_2):
    current_state = simulate_day(current_state)

print(
    f"Size of population after {NUM_DAYS_2} days: {sum(current_state.values())}"
)
