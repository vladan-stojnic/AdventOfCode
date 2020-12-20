import numpy as np
import itertools
import collections

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.split('\n\n')

    nums = []

    tiles = []

    for tile in data:
        tile_data = tile.splitlines()
        tile_num = tile_data[0].split(' ')
        tile_num = int(tile_num[1][:-1])

        nums.append(tile_num)

        grid = []
        for row in tile_data[1:]:
            grid.append(list(row))
        
        tiles.append(grid)

    return nums, np.array(tiles).transpose((1, 2, 0))

def top(tile):
    return tile[0, :]

def bottom(tile):
    return tile[-1, :]

def left(tile):
    return tile[:, 0]

def right(tile):
    return tile[:, -1]

def generate_transforms(tile):
    r1 = np.rot90(tile, 1)
    r2 = np.rot90(tile, 2)
    r3 = np.rot90(tile, 3)

    f1 = np.flipud(tile)
    
    f1r1 = np.rot90(f1, 1)
    f1r2 = np.rot90(f1, 2)
    f1r3 = np.rot90(f1, 3)

    return [tile, r1, r2, r3, f1, f1r1, f1r2, f1r3]

def get_neighbors(grid, i, j):
    neighbors = []
    if i-1>=0:
        if grid[i-1, j] != -1:
            neighbors.append(grid[i-1, j])
    if i+1<grid.shape[0]:
        if grid[i+1, j] != -1:
            neighbors.append(grid[i+1, j])
    if j-1>=0:
        if grid[i, j-1] != -1:
            neighbors.append(grid[i, j-1])
    if j+1<grid.shape[1]:
        if grid[i, j+1] != -1:
            neighbors.append(grid[i, j+1])

    return neighbors

def compare_with_monster(patch, monster):
    return np.all(patch[monster=='#']=='#')

def match_monster(sea, monster, out):
    for i in range(sea.shape[0]-monster.shape[0]):
        for j in range(sea.shape[1]-monster.shape[1]):
            ss = sea[i:i+monster.shape[0], j:j+monster.shape[1]]

            if compare_with_monster(ss, monster):
                patch = np.copy(ss)
                patch[monster=='#'] = 'O'
                out[i:i+monster.shape[0], j:j+monster.shape[1]] = patch

    return out


nums, tiles = read_input('day20')

# Part 1

nums = np.array(nums)

matched = np.array([0] * len(nums))

matches = collections.defaultdict(lambda: set())

# Find number of matches for every tile (corners = 2, border = 3, other = 4)

for (i, j) in itertools.combinations(range(len(nums)), 2):
    tile1 = tiles[:, :, i]
    tile2 = tiles[:, :, j]

    for t1, t2 in itertools.product(generate_transforms(tile1), generate_transforms(tile2)):
        if np.all(top(t1) == bottom(t2)):
            matches[i] |= set([j])
            matches[j] |= set([i])
        elif np.all(bottom(t1) == top(t2)):
            matches[i] |= set([j])
            matches[j] |= set([i])
        elif np.all(left(t1) == right(t2)):
            matches[i] |= set([j])
            matches[j] |= set([i])
        elif np.all(right(t1) == left(t2)):
            matches[i] |= set([j])
            matches[j] |= set([i])

for i in range(len(matched)):
    matched[i] = len(matches[i])

print(np.prod(nums[matched==2]))

# Part 2

# Arangement of tiles
output = -1*np.ones((int(np.sqrt(len(matched))), int(np.sqrt(len(matched)))), dtype=int)

used = set()

# Find correct arangement of tiles
for i in range(output.shape[0]):
    for j in range(output.shape[1]):
        neighbors = get_neighbors(output, i, j)

        if not neighbors:
            use = list(matched).index(2)
            output[i, j] = use
        else:
            possible = matches[neighbors[0]]
            for n in neighbors[1:]:
                possible &= matches[n]

            possible = possible.difference(used)

            possible = list(possible)
            possible = sorted(possible, key=lambda x: matched[x])
            use = possible[0]
            output[i, j] = use
        
        used.add(use)

# Output image with borders
image = np.zeros((int(np.sqrt(len(matched)))*10, int(np.sqrt(len(matched)))*10), dtype=str)

# Create image using formed arrangement
for i in range(output.shape[0]):
    for j in range(output.shape[1]):
        if i == 0 and j == 0:
            # Find matching orientations of corner tiles
            tile1 = tiles[:, :, output[0, 0]]
            tile2 = tiles[:, :, output[0, 1]]
            tile3 = tiles[:, :, output[1, 0]]

            for t1, t2, t3 in itertools.product(generate_transforms(tile1), generate_transforms(tile2), generate_transforms(tile3)):
                if np.all(right(t1) == left(t2)) and np.all(bottom(t1) == top(t3)):
                    image[0*10:(0+1)*10, 0*10:(0+1)*10] = t1
                    image[0*10:(0+1)*10, 1*10:(1+1)*10] = t2
                    image[1*10:(1+1)*10, 0*10:(0+1)*10] = t3
                    break
        elif i == 0 and j == 1:
            continue
        elif i == 1 and j == 0:
            continue
        elif i == 0:
            # Find matching orientations for border (top) tiles
            x, y = i, j-1
            old = image[x*10:(x+1)*10, y*10:(y+1)*10]
            tile = tiles[:, :, output[i, j]]

            for t1, t2 in itertools.product([old], generate_transforms(tile)):
                if np.all(right(t1) == left(t2)):
                    image[i*10:(i+1)*10, j*10:(j+1)*10] = t2
                    break
        elif j == 0:
            # Find matching orientations for border (left) tiles
            x, y = i-1, j
            old = image[x*10:(x+1)*10, y*10:(y+1)*10]
            tile = tiles[:, :, output[i, j]]

            for t1, t2 in itertools.product([old], generate_transforms(tile)):
                if np.all(bottom(t1) == top(t2)):
                    image[i*10:(i+1)*10, j*10:(j+1)*10] = t2
                    break
        else:
            # Find matching orientations for non-border tiles
            x, y = i, j-1
            old_left = image[x*10:(x+1)*10, y*10:(y+1)*10]

            x, y = i-1, j
            old_top = image[x*10:(x+1)*10, y*10:(y+1)*10]

            tile = tiles[:, :, output[i, j]]

            for t1, t2 in itertools.product([old_left], generate_transforms(tile)):
                if np.all(right(t1) == left(t2)) and np.all(bottom(old_top) == top(t2)):
                    image[i*10:(i+1)*10, j*10:(j+1)*10] = t2
                    break

# Sea image without borders
sea = np.zeros((int(np.sqrt(len(matched)))*8, int(np.sqrt(len(matched)))*8), dtype=str)

# Create sea image
for i in range(output.shape[0]):
    for j in range(output.shape[1]):
        patch = image[i*10:(i+1)*10, j*10:(j+1)*10]
        sea[i*8:(i+1)*8, j*8:(j+1)*8] = patch[1:-1, 1:-1]


# Monster shape
monster = []
monster.append(list('                  # '))
monster.append(list('#    ##    ##    ###'))
monster.append(list(' #  #  #  #  #  #   '))

monster = np.array(monster)

out = np.copy(sea)

# Rotate monster to match it and find if any is present
for m in generate_transforms(monster):
    out = match_monster(sea, m, out)

print(np.sum(out=='#'))