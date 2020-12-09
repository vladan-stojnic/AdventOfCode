import copy
import itertools

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    data = [int(d) for d in data]

    return data

data = read_input('day9')

# Part 1

current25 = copy.deepcopy(data[:25])

for idx, new in enumerate(data[25:]):
    pairs = itertools.combinations(current25, 2)
    sums = [sum(p) for p in pairs]

    if new not in sums:
        loc, solution = idx+25, new
        break

    current25.pop(0)
    current25.append(new)

print(loc, solution)

# Part 2

for i in range(loc):
    for j in range(i, loc):
        s = sum(data[i:j+1])
        if solution == s:
            ss = sorted(data[i:j+1])
            print(ss[0] + ss[-1])
            break