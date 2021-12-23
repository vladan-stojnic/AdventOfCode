import itertools
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Cuboid:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    def volume(self) -> int:
        return (
            (self.x_max - self.x_min + 1)
            * (self.y_max - self.y_min + 1)
            * (self.z_max - self.z_min + 1)
        )


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    output = []

    for line in data:
        operation = line.split(" ")[0]
        splitted = line.split(",")
        x = splitted[0].split("=")[-1]
        y = splitted[1].split("=")[-1]
        z = splitted[2].split("=")[-1]
        x = tuple(int(val) for val in x.split(".."))
        y = tuple(int(val) for val in y.split(".."))
        z = tuple(int(val) for val in z.split(".."))
        cuboid = Cuboid(x[0], x[1], y[0], y[1], z[0], z[1])
        output.append((operation, cuboid))

    return output


def find_intersection_of_two(cuboid1, cuboid2):
    intersection = Cuboid(
        max(cuboid1.x_min, cuboid2.x_min),
        min(cuboid1.x_max, cuboid2.x_max),
        max(cuboid1.y_min, cuboid2.y_min),
        min(cuboid1.y_max, cuboid2.y_max),
        max(cuboid1.z_min, cuboid2.z_min),
        min(cuboid1.z_max, cuboid2.z_max),
    )

    if (
        intersection.x_max < intersection.x_min
        or intersection.y_max < intersection.y_min
        or intersection.z_max < intersection.z_min
    ):
        return None

    return intersection


def find_on_cubes(data):
    num_cubes = 0
    cuboids = []
    for operation, cuboid in data:
        intersections = []

        for sign, cub in cuboids:
            intersection = find_intersection_of_two(cuboid, cub)
            if not intersection:
                continue
            intersections.append((-1 * sign, intersection))

        if operation == "on":
            cuboids.append((1, cuboid))
        for intersection in intersections:
            cuboids.append(intersection)

    for sign, cuboid in cuboids:
        num_cubes += sign * cuboid.volume()

    return num_cubes


def filter_cubes_part1(data):
    output = []
    for operation, cuboid in data:
        if (
            cuboid.x_min < -50
            or cuboid.x_max > 50
            or cuboid.y_min < -50
            or cuboid.y_max > 50
            or cuboid.z_min < -50
            or cuboid.z_max > 50
        ):
            continue

        output.append((operation, cuboid))

    return output


data = read_input("day22")
data = parse_data(data)

# Part 1

data1 = filter_cubes_part1(data)

print(f"Number of on cubes: {find_on_cubes(data1)}")

# Part 2

print(f"Number of on cubes: {find_on_cubes(data)}")
