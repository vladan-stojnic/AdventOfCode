from textwrap import wrap


class CPU:
    def __init__(self, register_values=[20, 60, 100, 140, 180, 220]):
        self.x = 1
        self.cycle = 1
        self.register_values = set(register_values)
        self.register_values_sorted = list(register_values)
        self.register = []
        self.screen = ""

    def do_register(self):
        if (
            ((self.cycle % 40) == self.x)
            or ((self.cycle % 40) == self.x + 1)
            or ((self.cycle % 40) == self.x + 2)
        ):
            self.screen += "#"
        else:
            self.screen += "."
        if self.cycle in self.register_values:
            self.register.append(self.x)

    def noop(self):
        self.do_register()
        self.cycle += 1

    def addx(self, val, step):
        self.do_register()
        self.cycle += 1
        if step == 1:
            self.addx(val, 2)
        elif step == 2:
            self.x += val
        else:
            raise NotImplementedError("Not implemented step")

    def execute(self, instruction):
        op, val = instruction

        if op == "noop":
            self.noop()
        elif op == "addx":
            self.addx(val, 1)
        else:
            raise NotImplementedError("This operation is not implemented")

    def draw_screen(self):
        return "\n".join(wrap(self.screen, 40))


def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()

    return data


def parse_data(data):
    def split_cast(line):
        splitted = line.split(" ")

        if len(splitted) == 1:
            return splitted[0], 0
        else:
            return splitted[0], int(splitted[1])

    return [split_cast(l) for l in data]


data = read_input("day10")

data = parse_data(data)

cpu = CPU()

for instruction in data:
    cpu.execute(instruction)

# Part 1
print(
    f"Sum of signal strengths: {sum(val * cycle for val, cycle in zip(cpu.register, cpu.register_values_sorted))}"
)

# Part 2
print(cpu.draw_screen())
