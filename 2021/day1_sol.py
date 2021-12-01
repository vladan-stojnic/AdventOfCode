def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()
    data = [int(d) for d in data]

    return data


def count_increases(data):
    increases = 0

    for x1, x2 in zip(data[:-1], data[1:]):
        if x2 > x1:
            increases += 1

    return increases


data = read_input("day1")

# Part 1

inc_depth = count_increases(data)

print("Depth increases", inc_depth, "times")

# Part 2

filtered_data = [sum(data[i : i + 3]) for i in range(len(data) - 2)]

inc_depth = count_increases(filtered_data)

print("Depth increases", inc_depth, "times")
