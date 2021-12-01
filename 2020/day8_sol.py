import copy

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    return data

def parse_row(row):
    op, value = row.split(' ')
    value = int(value)

    return op, value

def find_idx(data, pos):
    for i in range(pos, len(data)):
        if data[i].startswith('nop') or data[i].startswith('jmp'):
            return i

data = read_input('day8')

# Part 1

i = 0
visited = [False]*len(data)
accumulator = 0

while(not visited[i]):
    op, value = parse_row(data[i])
    visited[i] = True
    if op == 'acc':
        accumulator += value
        i += 1
    elif op == 'nop':
        i += 1
    else:
        i += value

print(accumulator)

# Part 2

pos = 0

while pos < len(data):
    idx = find_idx(data, pos)
    new_data = copy.deepcopy(data)
    if data[idx].startswith('nop'):
        new_data[idx] = 'jmp' + data[idx][3:]
    else:
        new_data[idx] = 'nop' + data[idx][3:]

    pos = idx + 1

    i = 0
    visited = [False]*len(new_data)
    accumulator = 0

    while(i<len(new_data) and (not visited[i])):
        op, value = parse_row(new_data[i])
        visited[i] = True
        if op == 'acc':
            accumulator += value
            i += 1
        elif op == 'nop':
            i += 1
        else:
            i += value
    
    if i>=len(new_data):
        print(accumulator)
        break