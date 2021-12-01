import itertools
import math

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()
    data = [int(d) for d in data]
    
    return data

data = read_input('day1')

# Part 1

for c in itertools.combinations(data, 2):
    if sum(c) == 2020:
        print(math.prod(c))

# Part 2

for c in itertools.combinations(data, 3):
    if sum(c) == 2020:
        print(math.prod(c))