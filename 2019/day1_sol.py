from util import read_input


def parse_input(data):
    return [int(val) for val in data.splitlines()]


def get_fuel(mass):
    return mass // 3 - 2


def get_fuel_part2(mass):
    required = get_fuel(mass)

    if required <= 0:
        return 0

    return required + get_fuel_part2(required)


assert get_fuel(12) == 2
assert get_fuel(14) == 2
assert get_fuel(1969) == 654
assert get_fuel(100756) == 33583

assert get_fuel_part2(14) == 2
assert get_fuel_part2(1969) == 966
assert get_fuel_part2(100756) == 50346

data = parse_input(read_input("day1"))

# Part 1

print(f"Fuel required: {sum([get_fuel(mass) for mass in data])}")

# Part 2

print(f"Fuel required: {sum([get_fuel_part2(mass) for mass in data])}")
