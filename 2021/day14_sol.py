from collections import defaultdict
from typing import Counter


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    rules = {}
    template = data[0]

    for line in data[2:]:
        splitted = line.split(" -> ")
        rules[splitted[0]] = splitted[1]

    return template, rules


def insertion(state, rules):
    new_state = defaultdict(lambda: 0)

    for pair, value in state.items():
        to_insert = rules[pair]
        new_state[pair[0] + to_insert] += value
        new_state[to_insert + pair[1]] += value

    return new_state


def template_to_state(template):
    state = defaultdict(lambda: 0)

    for x1, x2 in zip(template[:-1], template[1:]):
        state[x1 + x2] += 1

    return state


def state_to_counts(state, template):
    counter = defaultdict(lambda: 0)

    for key, val in state.items():
        counter[key[0]] += val

    counter[template[-1]] += 1

    return counter


data = read_input("day14")

template, rules = parse_data(data)

# Part 1

NUM_STEPS = 10

state = template_to_state(template)

for _ in range(NUM_STEPS):
    state = insertion(state, rules)

counter = state_to_counts(state, template)

print(
    f"Difference between maximum and minmum occurence: {max(counter.values()) - min(counter.values())}"
)

# Part 2

NUM_STEPS_2 = 40

for _ in range(NUM_STEPS, NUM_STEPS_2):
    state = insertion(state, rules)

counter = state_to_counts(state, template)

print(
    f"Difference between maximum and minmum occurence: {max(counter.values()) - min(counter.values())}"
)
