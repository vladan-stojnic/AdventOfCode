import numpy as np

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    data = [[c for c in line] for line in data]

    return data

def get_neighbor(state, x, y):
    neighbor = state[max(0, x-1):min(state.shape[0], x+2), max(0, y-1):min(state.shape[1], y+2)]
    return list(neighbor.flatten())

def get_num_occupied(state, x, y):
    occupied = 0
    # Look UP
    for i in range(x-1, -1, -1):
        if state[i, y] == '#':
            occupied += 1
            break
        elif state[i, y] == 'L':
            break

    # Look DOWN
    for i in range(x+1, state.shape[0]):
        if state[i, y] == '#':
            occupied += 1
            break
        elif state[i, y] == 'L':
            break

    # Look LEFT
    for i in range(y-1, -1, -1):
        if state[x, i] == '#':
            occupied += 1
            break
        elif state[x, i] == 'L':
            break

    # Look RIGHT
    for i in range(y+1, state.shape[1]):
        if state[x, i] == '#':
            occupied += 1
            break
        elif state[x, i] == 'L':
            break

    # Look UP-LEFT
    for i in range(1, min(x+1, y+1)):
        if state[x-i, y-i] == '#':
            occupied += 1
            break
        elif state[x-i, y-i] == 'L':
            break

    # Look UP-RIGHT
    for i in range(1, min(x+1, state.shape[1]-y)):
        if state[x-i, y+i] == '#':
            occupied += 1
            break
        elif state[x-i, y+i] == 'L':
            break

    # Look DOWN-LEFT
    for i in range(1, min(state.shape[0]-x, y+1)):
        if state[x+i, y-i] == '#':
            occupied += 1
            break
        elif state[x+i, y-i] == 'L':
            break

    # Look DOWN-RIGHT
    for i in range(1, min(state.shape[0]-x, state.shape[1]-y)):
        if state[x+i, y+i] == '#':
            occupied += 1
            break
        elif state[x+i, y+i] == 'L':
            break

    return occupied

# Part 1

state = np.array(read_input('day11'))

while True:
    #print(state)
    new_state = state.copy()
    for ir in range(state.shape[0]):
        for ic in range(state.shape[1]):
            if state[ir, ic] == 'L':
                neighbor = get_neighbor(state, ir, ic)
                if (neighbor.count('L') + neighbor.count('.')) == len(neighbor):
                    new_state[ir, ic] = '#'
            elif state[ir, ic] == '#':
                neighbor = get_neighbor(state, ir, ic)
                if neighbor.count('#') >= 5:
                    new_state[ir, ic] = 'L'
    
    if np.all(new_state == state):
        break

    state = new_state.copy()

print(list(state.flatten()).count('#'))

# Part 2

state = np.array(read_input('day11'))

while True:
    #print(state)
    new_state = state.copy()
    for ir in range(state.shape[0]):
        for ic in range(state.shape[1]):
            occupied = get_num_occupied(state, ir, ic)
            if state[ir, ic] == 'L' and occupied == 0:
                new_state[ir, ic] = '#'
            elif state[ir, ic] == '#' and occupied >= 5:
                new_state[ir, ic] = 'L'
    
    if np.all(new_state == state):
        break

    state = new_state.copy()

print(list(state.flatten()).count('#'))