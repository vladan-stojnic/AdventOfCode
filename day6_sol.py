from collections import Counter

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.split('\n\n')

    data = [(''.join(d.splitlines()), len(d.splitlines())) for d in data]

    return data

data = read_input('day6')

# Part 1

result = 0
for group, _ in data:
    counts = Counter(group)
    result += len(counts.values())

print(result)

# Part 2

result = 0
for group, persons in data:
    counts = Counter(group)
    result += sum([c == persons for c in counts.values()])

print(result)