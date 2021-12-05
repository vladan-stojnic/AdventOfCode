from collections import Counter, namedtuple

Point = namedtuple("Point", ["x", "y"])
Line = namedtuple("Line", ["p1", "p2"])


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_line(line):
    splitted = line.split(" -> ")
    first = Point(*[int(x) for x in splitted[0].split(",")])
    second = Point(*[int(x) for x in splitted[1].split(",")])

    return Line(first, second)


def horizontal(line):
    return line.p1.y == line.p2.y


def vertical(line):
    return line.p1.x == line.p2.x


def line_points(line):
    mov_x, mov_y = 0, 0

    if line.p1.x > line.p2.x:
        mov_x = -1
    elif line.p1.x < line.p2.x:
        mov_x = 1

    if line.p1.y > line.p2.y:
        mov_y = -1
    elif line.p1.y < line.p2.y:
        mov_y = 1

    points = [line.p1]

    current_x, current_y = line.p1.x + mov_x, line.p1.y + mov_y

    while (current := Point(current_x, current_y)) != line.p2:
        points.append(current)
        current_x += mov_x
        current_y += mov_y

    points.append(line.p2)

    return points


data = read_input("day5")

lines = [parse_line(line) for line in data]

# Part 1

counter = Counter()

for line in lines:
    if horizontal(line) or vertical(line):
        counter.update(line_points(line))

dangerous = sum(val >= 2 for key, val in counter.items())

print(f"Number of dangerous spots: {dangerous}")

# Part 2

counter = Counter()

for line in lines:
    counter.update(line_points(line))

dangerous = sum(val >= 2 for key, val in counter.items())

print(f"Number of dangerous spots: {dangerous}")
