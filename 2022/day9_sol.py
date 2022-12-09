from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()

    return data


def parse_data(data):
    def split_and_cast(line):
        splitted = line.split()
        return splitted[0], int(splitted[1])

    return [split_and_cast(l) for l in data]


def move_head(direction, head, tail, visited, step=1):
    x, y = head
    match direction:
        case "R":
            x += step
        case "L":
            x -= step
        case "U":
            y += step
        case "D":
            y -= step
    head = Point(x, y)
    head, tail = move_tail(head, tail, visited)

    return head, tail


def move_tail(head, tail, visited):
    x, y = tail
    if not touching(head, tail):
        x += 1 * sign(head.x - tail.x)
        y += 1 * sign(head.y - tail.y)
        tail = Point(x, y)

    visited.add(tail)

    return head, tail


def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


def touching(head, tail):
    dist = abs(head.x - tail.x) + abs(head.y - tail.y)

    return (dist == 1) or (dist == 2 and not in_same_row_col(head, tail))


def in_same_row_col(head, tail):
    return head.x == tail.x or head.y == tail.y


def execute_move(move, head, tail, visited):
    direction, steps = move

    for _ in range(steps):
        head, tail = move_head(direction, head, tail, visited)

    return head, tail


def execute_move_part2(move, knots, visited):
    direction, steps = move

    for _ in range(steps):
        head, tail = move_head(direction, knots[0], knots[1], visited[0])
        knots[0] = head
        knots[1] = tail

        for head_pos in range(1, len(knots) - 1):
            head, tail = move_head(
                direction,
                knots[head_pos],
                knots[head_pos + 1],
                visited[head_pos],
                step=0,
            )
            knots[head_pos] = head
            knots[head_pos + 1] = tail


data = read_input("day9")

data = parse_data(data)

# Part 1

head = Point(0, 0)
tail = Point(0, 0)
visited = set()

for move in data:
    head, tail = execute_move(move, head, tail, visited)

print(f"Number of positions visited by tail: {len(visited)}")

# Part 2

knots = [Point(0, 0) for _ in range(10)]
visited = [set() for _ in range(9)]

for move in data:
    execute_move_part2(move, knots, visited)

print(f"Number of positions visited by tail: {len(visited[-1])}")
