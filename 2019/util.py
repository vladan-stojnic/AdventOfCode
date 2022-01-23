from copy import deepcopy


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    return data


class IntcodeComputer:
    def __init__(self, memory):
        self._start_memory = memory
        self._pos = 0
        self.reset()
        self._ops = {
            1: self._add,
            2: self._mul,
        }

    def _add(self):
        self.memory[self.memory[self._pos + 3]] = (
            self.memory[self.memory[self._pos + 1]]
            + self.memory[self.memory[self._pos + 2]]
        )

        return 4

    def _mul(self):
        self.memory[self.memory[self._pos + 3]] = (
            self.memory[self.memory[self._pos + 1]]
            * self.memory[self.memory[self._pos + 2]]
        )

        return 4

    def execute(self):
        while self._pos < len(self.memory):
            opcode = self.memory[self._pos]

            if opcode == 99:
                break
            elif opcode in self._ops:
                mov = self._ops[opcode]()
            else:
                raise ValueError("Not implemented operation")

            self._pos += mov

    def set_states(self, states):
        for pos, val in states:
            self.memory[pos] = val

    def reset(self):
        self._pos = 0
        self.memory = deepcopy(self._start_memory)


if __name__ == "__main__":
    intcode = IntcodeComputer([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    intcode.execute()
    assert intcode.memory == [
        3500,
        9,
        10,
        70,
        2,
        3,
        11,
        0,
        99,
        30,
        40,
        50,
    ]

    intcode = IntcodeComputer([1, 0, 0, 0, 99])
    intcode.execute()
    assert intcode.memory == [2, 0, 0, 0, 99]

    intcode = IntcodeComputer([2, 3, 0, 3, 99])
    intcode.execute()
    assert intcode.memory == [2, 3, 0, 6, 99]

    intcode = IntcodeComputer([2, 4, 4, 5, 99, 0])
    intcode.execute()
    assert intcode.memory == [2, 4, 4, 5, 99, 9801]

    intcode = IntcodeComputer([1, 1, 1, 4, 99, 5, 6, 0, 99])
    intcode.execute()
    assert intcode.memory == [
        30,
        1,
        1,
        4,
        2,
        5,
        6,
        0,
        99,
    ]

    print("All tests passed!!!")
