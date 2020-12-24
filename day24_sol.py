import collections
import copy

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    return data

def parse_line(line):
    one_element = ['e', 'w']

    output = []

    i = 0

    while i < len(line):
        if line[i] in one_element:
            output.append(line[i])
            i += 1
        else:
            output.append(line[i:i+2])
            i += 2

    return output

def get_neighbors(tile):
    x, y = tile

    return set([(x+1, y), (x-1, y), (x+0.5, y+0.5), (x+0.5, y-0.5), (x-0.5, y+0.5), (x-0.5, y-0.5)])

def get_possible_white_tiles(black_tiles):
    possible_tiles = set()

    for tile in black_tiles:
        possible_tiles = possible_tiles.union(get_neighbors(tile).difference(black_tiles))

    return possible_tiles

def count_black_neighbors(tile, black_tiles):
    neighbors = get_neighbors(tile)
    black_neighbors = 0
    for neighbor in neighbors:
        if neighbor in black_tiles:
            black_neighbors += 1

    return black_neighbors

def play_exibit(black_tiles, num_days=100):
    for i in range(num_days):
        new_black = set()
        possible_white_tiles = get_possible_white_tiles(black_tiles)

        for tile in black_tiles:
            black_neighbors = count_black_neighbors(tile, black_tiles)

            if not((black_neighbors == 0) or (black_neighbors > 2)):
                new_black.add(tile)

        for tile in possible_white_tiles:
            black_neighbors = count_black_neighbors(tile, black_tiles)

            if black_neighbors == 2:
                new_black.add(tile)

        black_tiles = copy.deepcopy(new_black)

    return len(black_tiles)

data = read_input('day24')

flipping = collections.defaultdict(lambda: 0)

for line in data:
    movements = parse_line(line)
    x, y = 0, 0

    for move in movements:
        if move == 'e':
            x += 1
        elif move == 'w':
            x -= 1
        elif move == 'se':
            x += 0.5
            y -= 0.5
        elif move == 'sw':
            x -= 0.5
            y -= 0.5
        elif move == 'ne':
            x += 0.5
            y += 0.5
        else:
            x -= 0.5
            y += 0.5

    flipping[(x, y)] += 1

# Part 1

black_tiles = set()

for key, value in flipping.items():
    if value % 2 == 1:
        black_tiles.add(key)

print(len(black_tiles))

# Part 2

print(play_exibit(black_tiles))