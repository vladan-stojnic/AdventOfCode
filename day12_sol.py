import math

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    data = [(d[0], int(d[1:])) for d in data]

    return data

data = read_input('day12')

# Part 1

x, y = 0, 0
direction = 0

for command, value in data:
    if command == 'N':
        y += value
    elif command == 'S':
        y -= value
    elif command == 'E':
        x += value
    elif command == 'W':
        x -= value
    elif command == 'L':
        direction -= value // 90
        direction %= 4
    elif command == 'R':
        direction += value // 90
        direction %= 4
    elif command == 'F':
        if direction == 0:
            x += value
        elif direction == 1:
            y -= value
        elif direction == 2:
            x -= value
        else:
            y += value

print(abs(x)+abs(y))

# Part 2
x, y = 0, 0
x_w, y_w = 10, 1

for command, value in data:
    if command == 'N':
        y_w += value
    elif command == 'S':
        y_w -= value
    elif command == 'E':
        x_w += value
    elif command == 'W':
        x_w -= value
    elif command == 'F':
        x += value * x_w
        y += value * y_w
    elif command == 'L':
        angle = value
        x_w, y_w = round(math.cos(math.radians(angle))*x_w-math.sin(math.radians(angle))*y_w), round(math.sin(math.radians(angle))*x_w+math.cos(math.radians(angle))*y_w)
    elif command == 'R':
        angle = -value
        x_w, y_w = round(math.cos(math.radians(angle))*x_w-math.sin(math.radians(angle))*y_w), round(math.sin(math.radians(angle))*x_w+math.cos(math.radians(angle))*y_w)

print(abs(x)+abs(y))