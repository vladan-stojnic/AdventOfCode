import itertools
from util import read_input, IntcodeComputer


def parse_input(data):
    return [int(val) for val in data.split(",")]


memory = parse_input(read_input("day2"))

# Part 1

intcode = IntcodeComputer(memory)

intcode.set_states([(1, 12), (2, 2)])

intcode.execute()

print(f"Value at index 0: {intcode.memory[0]}")

# Part 2

SECRET_CODE = 19690720

for noun, verb in itertools.product(range(100), range(100)):
    intcode.reset()
    intcode.set_states([(1, noun), (2, verb)])
    intcode.execute()

    if intcode.memory[0] == SECRET_CODE:
        print(f"Value 100 * noun + verb: {100*noun + verb}")
        break

