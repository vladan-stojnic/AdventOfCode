from collections import defaultdict


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_line(line):
    splitted = line.split(" | ")
    signal_pattern = [s for s in splitted[0].split(" ")]
    output = [s for s in splitted[1].split(" ")]

    return signal_pattern, output


def is_simple_digit(digit):
    return len(digit) in {2, 3, 4, 7}


def parse_sequence(seq):
    mapping = defaultdict(set)

    for s in seq:
        if len(s) == 2:
            mapping[1].update(s)
        elif len(s) == 3:
            mapping[7].update(s)
        elif len(s) == 4:
            mapping[4].update(s)
        elif len(s) == 7:
            mapping[8].update(s)
        elif len(s) == 5:
            if len(mapping[235]) == 0:
                mapping[235] = set(s)
            else:
                mapping[235] = mapping[235].intersection(s)
        elif len(s) == 6:
            if len(mapping[690]) == 0:
                mapping[690] = set(s)
            else:
                mapping[690] = mapping[690].intersection(s)

    mapping[147] = mapping[1].union(mapping[4]).union(mapping[7])

    return mapping


def create_correct_mapping(mapping):
    correct_mapping = {}

    correct_mapping[mapping[7].difference(mapping[1]).pop()] = "a"
    correct_mapping[
        (mapping[4].difference(mapping[1])).intersection(mapping[690]).pop()
    ] = "b"
    correct_mapping[mapping[1].difference(mapping[690]).pop()] = "c"
    correct_mapping[
        (mapping[4].difference(mapping[1])).difference(mapping[690]).pop()
    ] = "d"
    correct_mapping[
        (mapping[8].difference(mapping[147])).difference(mapping[235]).pop()
    ] = "e"
    correct_mapping[
        (mapping[8].difference(mapping[147])).intersection(mapping[235]).pop()
    ] = "g"
    correct_mapping[
        set("abcdefg").difference(correct_mapping.keys()).pop()
    ] = "f"

    return correct_mapping


def map_values(digit, mapping):
    new_digit = ""

    for d in digit:
        new_digit += mapping[d]

    return "".join(sorted(new_digit))


def decode_digit(digit):
    mapping = {}

    mapping["abcefg"] = "0"
    mapping["cf"] = "1"
    mapping["acdeg"] = "2"
    mapping["acdfg"] = "3"
    mapping["bcdf"] = "4"
    mapping["abdfg"] = "5"
    mapping["abdefg"] = "6"
    mapping["acf"] = "7"
    mapping["abcdefg"] = "8"
    mapping["abcdfg"] = "9"

    return mapping[digit]


def decode(output, mapping):
    val = ""

    for digit in output:
        val += decode_digit(map_values(digit, mapping))

    return int(val)


data = read_input("day8")

data = [parse_line(line) for line in data]

# Part 1

simple_numbers = 0

for _, output in data:
    simple_numbers += sum(map(is_simple_digit, output))

print(f"Number of simple numbers in output: {simple_numbers}")

# Part 2

sum_of_values = 0

for signal, output in data:
    mapping = parse_sequence(signal)

    correct_mapping = create_correct_mapping(mapping)

    sum_of_values += decode(output, correct_mapping)

print(f"Sum of decoded numbers: {sum_of_values}")
