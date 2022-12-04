def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()

    return data


def parse_data(data):
    out = []

    for d in data:
        pairs = d.split(",")
        pair_left = pairs[0].split("-")
        pair_right = pairs[1].split("-")
        out.append(
            (
                (int(pair_left[0]), int(pair_left[1])),
                (int(pair_right[0]), int(pair_right[1])),
            )
        )

    return out


def interval_contained_first(first, second):
    return first[0] >= second[0] and first[1] <= second[1]


def interval_contained(first, second):
    return interval_contained_first(first, second) or interval_contained_first(
        second, first
    )


def interval_overlaps_first(first, second):
    return second[0] >= first[0] and second[0] <= first[1]


def interval_overlaps(first, second):
    return interval_overlaps_first(first, second) or interval_overlaps_first(
        second, first
    )


data = read_input("day4")

data = parse_data(data)

# Part 1
num_contained_intervals = sum(
    interval_contained(line[0], line[1]) for line in data
)

print(
    f"Number of intervals that fully contain each other: {num_contained_intervals}"
)

# Part 2
num_overlapping_intervals = sum(
    interval_overlaps(line[0], line[1]) for line in data
)

print(
    f"Number of intervals that overlap with each other: {num_overlapping_intervals}"
)
