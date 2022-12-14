from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()

    return data


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def construct_line(loc1, loc2):
    x1, y1 = loc1
    x2, y2 = loc2

    dx = sign(x2 - x1)
    dy = sign(y2 - y1)

    line_points = set()

    current = loc1
    while current != loc2:
        line_points.add(current)
        current = Point(current.x + dx, current.y + dy)
    line_points.add(loc2)

    return line_points


def parse_data(data):
    occupied = set()
    for line in data:
        locations = line.split(" -> ")
        for loc1, loc2 in zip(locations, locations[1:]):
            loc1 = Point(*(int(l) for l in loc1.split(",")))
            loc2 = Point(*(int(l) for l in loc2.split(",")))

            occupied.update(construct_line(loc1, loc2))

    return occupied


def get_new_location(current, occupied, floor=None):
    move = Point(current.x, current.y + 1)
    if move not in occupied and move.y != floor:
        return move

    move = Point(current.x - 1, current.y + 1)
    if move not in occupied and move.y != floor:
        return move

    move = Point(current.x + 1, current.y + 1)
    if move not in occupied and move.y != floor:
        return move

    return None


def simulate_new_sand(current, occupied, lowest_point):
    while current != None:
        last = current
        current = get_new_location(current, occupied)

        if current is not None and current.y > lowest_point:
            return False

    occupied.add(last)
    return True


def simulate_new_sand_part2(current, occupied, lowest_point):
    while current != None:
        last = current
        current = get_new_location(current, occupied, lowest_point + 2)

    occupied.add(last)


data = read_input("day14")
sand_entrance = Point(500, 0)

# Part 1
occupied = parse_data(data)
start_size = len(occupied)
lowest_point = max(o.y for o in occupied)
running = True
while running:
    running = simulate_new_sand(sand_entrance, occupied, lowest_point)

print(f"Number of grains of sand that fell: {len(occupied) - start_size}")

# Part 2
occupied = parse_data(data)
start_size = len(occupied)
lowest_point = max(o.y for o in occupied)
while sand_entrance not in occupied:
    simulate_new_sand_part2(sand_entrance, occupied, lowest_point)

print(f"Number of grains of sand that fell: {len(occupied) - start_size}")
