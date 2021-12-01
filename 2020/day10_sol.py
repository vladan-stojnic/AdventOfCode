from collections import Counter
from functools import lru_cache

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    data = [int(d) for d in data]

    return data

@lru_cache
def weight(val, m):
    global data_sorted_set

    if val == m:
        return 1

    w = 0
    for i in range(1, 4):
        if (val + i) in data_sorted_set:
            w += weight(val+i, m)

    return w


data = read_input('day10')

# Part 1

data_sorted = sorted(data)

diffs = [data_sorted[i]-data_sorted[i-1] for i in range(1, len(data_sorted))]
diffs.insert(0, data_sorted[0])

counts = Counter(diffs)

print(counts[1]*(counts[3]+1))

# Part 2

data_sorted_set = set(data_sorted)

ww = 0

for ds in data_sorted[:3]:
    if ds <= 3:
        ww += weight(ds, data_sorted[-1])

print(ww)