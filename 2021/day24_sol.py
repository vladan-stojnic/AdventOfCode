"""Solved by hand so this one is only for checking if the result is correct"""


from collections import deque


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


memory = {
    "w": 0,
    "x": 0,
    "y": 0,
    "z": 0,
}


def get_value(x):
    if x in memory:
        return memory[x]

    return int(x)


def inp(register, input_tape):
    memory[register] = input_tape.popleft()


def add(register, value):
    memory[register] += get_value(value)


def mul(register, value):
    memory[register] *= get_value(value)


def div(register, value):
    memory[register] = memory[register] // get_value(value)


def mod(register, value):
    memory[register] %= get_value(value)


def eql(register, value):
    value = get_value(value)

    if memory[register] == value:
        memory[register] = 1
    else:
        memory[register] = 0


mapping = {
    "inp": inp,
    "add": add,
    "mul": mul,
    "div": div,
    "mod": mod,
    "eql": eql,
}


data = read_input("day24")

input_tape = deque([4, 8, 1, 1, 1, 5, 1, 4, 7, 1, 9, 1, 1, 1])

for line in data:
    splitted = line.split(" ")
    if len(splitted) == 3:
        mapping[splitted[0]](splitted[1], splitted[2])
    else:
        mapping[splitted[0]](splitted[1], input_tape)
        print(memory["z"])
        input("Enter....")

print(memory["z"])
