def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    data = [(d.split(" ")[0], int(d.split(" ")[1])) for d in data]

    return data


data = read_input("day2")

# Part 1

pos_x, pos_y = 0, 0

for command, value in data:
    if command == "forward":
        pos_x += value
    elif command == "down":
        pos_y += value
    elif command == "up":
        pos_y -= value
    else:
        raise ValueError("Wrong parsing of input")

print(f"x: {pos_x}, y: {pos_y}, multiplied: {pos_x * pos_y}")

# Part 2

pos_x, pos_y, aim = 0, 0, 0

for command, value in data:
    if command == "forward":
        pos_x += value
        pos_y += aim * value
    elif command == "down":
        aim += value
    elif command == "up":
        aim -= value
    else:
        raise ValueError("Wrong parsing of input")

print(f"x: {pos_x}, y: {pos_y}, multiplied: {pos_x * pos_y}")
