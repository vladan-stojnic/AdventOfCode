from math import ceil, floor
from statistics import mean, median


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.split(",")

    data = [int(d) for d in data]

    return data


data = read_input("day7")

max_pos = max(data)

# Part 1

target_position = int(median(data))
fuel_used = sum(map(lambda x: abs(x - target_position), data))

print(f"Target position: {target_position} Fuel used: {fuel_used}")

# Part 2

target_position_floor = floor(mean(data))
target_position_ceil = ceil(mean(data))

fuel_used_floor = sum(
    map(
        lambda x: (x * (x + 1)) // 2,
        map(lambda x: abs(x - target_position_floor), data),
    )
)
fuel_used_ceil = sum(
    map(
        lambda x: (x * (x + 1)) // 2,
        map(lambda x: abs(x - target_position_ceil), data),
    )
)

possible = [
    (target_position_floor, fuel_used_floor),
    (target_position_ceil, fuel_used_ceil),
]

target_position, fuel_used = min(possible, key=lambda x: x[1])

print(f"Target position: {target_position} Fuel used: {fuel_used}")
