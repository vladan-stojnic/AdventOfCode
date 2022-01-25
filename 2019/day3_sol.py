import itertools
from util import read_input


def parse_data(data):
    splitted = data.splitlines()

    return splitted[0], splitted[1]


def is_horizontal(line):
    p1, p2 = line

    return p1[1] == p2[1]


def is_vertical(line):
    p1, p2 = line

    return p1[0] == p2[0]


def line_cross(l1, l2):
    p11, p12 = l1
    p21, p22 = l2

    if is_horizontal(l1) == is_horizontal(l2) and p11[1] == p21[1]:
        p11x, p12x = min(p11[0], p12[0]), max(p11[0], p12[0])
        p21x, p22x = min(p21[0], p22[0]), max(p21[0], p22[0])

        if max(p11x, p21x) <= min(p12x, p22x):
            return max(p11x, p21x), p11[1]
    elif is_vertical(l1) and is_vertical(l2) and p11[0] == p21[0]:
        p11y, p12y = min(p11[1], p12[1]), max(p11[1], p12[1])
        p21y, p22y = min(p21[1], p22[1]), max(p21[1], p22[1])

        if max(p11y, p21y) <= min(p12y, p22y):
            return max(p11y, p21y), p11[1]
    elif is_horizontal(l1) and is_vertical(l2):
        y1 = p11[1]
        x2 = p21[0]

        if (min(p21[1], p22[1]) <= y1 <= max(p21[1], p22[1])) and (
            min(p11[0], p12[0]) <= x2 <= max(p11[0], p12[0])
        ):
            return x2, y1
    else:
        y2 = p21[1]
        x1 = p11[0]

        if (min(p11[1], p12[1]) <= y2 <= max(p11[1], p12[1])) and (
            min(p21[0], p22[0]) <= x1 <= max(p21[0], p22[0])
        ):
            return x1, y2


def create_line(s):
    x, y = 0, 0
    output = []

    for val in s.split(","):
        current = ((x, y),)
        direction = val[0]
        move = int(val[1:])

        if direction == "R":
            current += ((x + move, y),)
            x += move
        elif direction == "D":
            current += ((x, y - move),)
            y -= move
        elif direction == "U":
            current += ((x, y + move),)
            y += move
        else:
            current += ((x - move, y),)
            x -= move

        output.append(current)

    return output


def find_crossings(l1, l2):
    crossings = []

    for ll1, ll2 in itertools.product(l1, l2):
        lc = line_cross(ll1, ll2)

        if lc and not (lc[0] == 0 and lc[1] == 0):
            crossings.append(lc)

    return crossings


def find_min_dist_cross(l1, l2):
    crossings = find_crossings(l1, l2)

    return min([abs(x[0]) + abs(x[1]) for x in crossings])


def point_in_segment(p, l):
    if is_horizontal(l):
        if (min(l[0][0], l[1][0]) <= p[0] <= max(l[0][0], l[1][0])) and p[
            1
        ] == l[0][1]:
            return True, abs(l[0][0] - p[0])
        else:
            return False, abs(l[0][0] - l[1][0])
    else:
        if (min(l[0][1], l[1][1]) <= p[1] <= max(l[0][1], l[1][1])) and p[
            0
        ] == l[0][0]:
            return True, abs(l[0][1] - p[1])
        else:
            return False, abs(l[0][1] - l[1][1])


def find_min_delay_cross(l1, l2):
    crossings = find_crossings(l1, l2)

    distances = []

    for cross in crossings:
        delay1 = 0
        for l11 in l1:
            crossed, delay = point_in_segment(cross, l11)
            delay1 += delay
            if crossed:
                break

        delay2 = 0
        for l22 in l2:
            crossed, delay = point_in_segment(cross, l22)
            delay2 += delay
            if crossed:
                break

        distances.append(delay1 + delay2)

    return min(distances)


assert (
    find_min_dist_cross(create_line("R8,U5,L5,D3"), create_line("U7,R6,D4,L4"))
    == 6
)
assert (
    find_min_dist_cross(
        create_line("R75,D30,R83,U83,L12,D49,R71,U7,L72"),
        create_line("U62,R66,U55,R34,D71,R55,D58,R83"),
    )
    == 159
)
assert (
    find_min_dist_cross(
        create_line("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"),
        create_line("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"),
    )
    == 135
)

assert (
    find_min_delay_cross(
        create_line("R8,U5,L5,D3"), create_line("U7,R6,D4,L4")
    )
    == 30
)
assert (
    find_min_delay_cross(
        create_line("R75,D30,R83,U83,L12,D49,R71,U7,L72"),
        create_line("U62,R66,U55,R34,D71,R55,D58,R83"),
    )
    == 610
)
assert (
    find_min_delay_cross(
        create_line("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"),
        create_line("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"),
    )
    == 410
)


l1, l2 = parse_data(read_input("day3"))

# Part 1

print(
    f"Minimal distant crossing: {find_min_dist_cross(create_line(l1), create_line(l2))}"
)

# Part 2

print(
    f"Minimal delayed crossing: {find_min_delay_cross(create_line(l1), create_line(l2))}"
)
