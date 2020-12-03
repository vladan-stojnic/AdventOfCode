def read_file(path):
    grid = []
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()
    for line in data:
        row = []
        for elem in line:
            row.append(elem)
        grid.append(row)
    
    return grid

data = read_file('day3')

# Part 1

pos_x, pos_y = 0, 0

trees = 0

while(True):
    pos_x += 3
    pos_x %= len(data[0])
    pos_y += 1
    if pos_y == len(data):
        break
    elif data[pos_y][pos_x] == '#':
        trees += 1

print(trees)

# Part 2

res = 1

for slope_x, slope_y in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:

    pos_x, pos_y = 0, 0

    trees = 0

    while(True):
        pos_x += slope_x
        pos_x %= len(data[0])
        pos_y += slope_y
        if pos_y >= len(data):
            break
        elif data[pos_y][pos_x] == '#':
            trees += 1

    res *= trees

print(res)