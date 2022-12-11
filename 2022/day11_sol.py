from collections import deque
from math import prod


def reduce_level(val):
    return val // 3


class Monkey:
    def __init__(
        self,
        items,
        operation,
        test,
        if_true,
        if_false,
        reduce_function=reduce_level,
    ):
        self.items = deque(items)
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.num_inspected = 0
        self.reduce_function = reduce_function
        self.lcm = None

    def inspect(self, monkeys):
        if self.lcm is None:
            self.lcm = prod(m.test for m in monkeys)

        while self.items:
            self.num_inspected += 1
            item = self.items.popleft()
            new = eval(self.operation.replace("old", str(item)))
            new = self.reduce_function(new)
            new %= self.lcm

            if (new % self.test) == 0:
                monkeys[self.if_true].items.append(new)
            else:
                monkeys[self.if_false].items.append(new)


def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    # data = data.splitlines()

    return data


def parse_data(data, reduce_function):
    monkeys_data = data.split("\n\n")

    return [
        parse_monkey(monkey_data, reduce_function)
        for monkey_data in monkeys_data
    ]


def parse_monkey(
    data,
    reduce_function,
):
    lines = data.splitlines()

    items = (int(it) for it in lines[1].split(": ")[1].split(", "))

    test = int(lines[3].split(" by ")[-1])

    if_true = int(lines[4].split(" monkey ")[-1])

    if_false = int(lines[5].split(" monkey ")[-1])

    operation = lines[2].split(" = ")[-1]

    return Monkey(items, operation, test, if_true, if_false, reduce_function)


data = read_input("day11")

# Part 1
NUM_ROUNDS = 20
monkeys = parse_data(data, reduce_level)

for ro in range(NUM_ROUNDS):
    for monkey in monkeys:
        monkey.inspect(monkeys)

print(
    f"Level of monkey business: {prod(sorted((monkey.num_inspected for monkey in monkeys), reverse=True)[:2])}"
)

# Part 2
NUM_ROUNDS = 10000
monkeys = parse_data(data, lambda x: x)

for ro in range(NUM_ROUNDS):
    for monkey in monkeys:
        monkey.inspect(monkeys)

print(
    f"Level of monkey business: {prod(sorted((monkey.num_inspected for monkey in monkeys), reverse=True)[:2])}"
)
