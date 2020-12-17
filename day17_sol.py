import copy

def read_input(path, dimension=3):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    active = []

    for i, row in enumerate(data):
        for j, state in enumerate(row):
            if state == '#':
                if dimension == 3:
                    active.append((i, j, 0))
                elif dimension == 4:
                    active.append((i, j, 0, 0))

    return set(active)

def get_neighbors(location):
    neighbors = []

    if len(location) == 3:
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    neighbors.append((location[0]+i, location[1]+j, location[2]+k))

    elif len(location) == 4:
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        neighbors.append((location[0]+i, location[1]+j, location[2]+k, location[3]+l))

    return set(neighbors)

def get_num_active(location, state):
    return sum([1 for neighbor in get_neighbors(location) if neighbor in state])

def get_all_neighbors_to_check(state):
    neighbors = set()
    for active in state:
        neighbors |= get_neighbors(active)

    return neighbors

# Part 1

current_state = read_input('day17')

for play in range(6):

    neighbors_to_check = get_all_neighbors_to_check(current_state)
    new_state = set()

    for neighbor in neighbors_to_check:
        if neighbor in current_state:
            if 3 <= get_num_active(neighbor, current_state) <= 4:
                new_state.add(neighbor)
        else:
            if get_num_active(neighbor, current_state) == 3:
                new_state.add(neighbor)

    current_state = copy.deepcopy(new_state)

print(len(current_state))

# Part 2

current_state = read_input('day17', dimension=4)

for play in range(6):

    neighbors_to_check = get_all_neighbors_to_check(current_state)
    new_state = set()

    for neighbor in neighbors_to_check:
        if neighbor in current_state:
            if 3 <= get_num_active(neighbor, current_state) <= 4:
                new_state.add(neighbor)
        else:
            if get_num_active(neighbor, current_state) == 3:
                new_state.add(neighbor)

    current_state = copy.deepcopy(new_state)

print(len(current_state))