from functools import lru_cache

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    return data

@lru_cache
def weight(color):
    global rules
    for r in rules:
        if r[0] == color:
            rule = r
            break
    if len(rule) == 1:
        return 1
    w = 1
    for num, color in rule[1:]:
        w += num * weight(color)

    return w

data = read_input('day7')

rules = []

for d in data:
    parts = [s.strip() for s in d.split('contain')]

    original = ' '.join(parts[0].split(' ')[:2])

    rule = (original, )

    contents = [p.strip() for p in parts[1].split(',')]

    if not contents[0].startswith('no other'):
        for c in contents:
            bags = c.split(' ')
            r = (int(bags[0]), ' '.join(bags[1:3]))
            rule = rule + (r, )
    
    rules.append(rule)

# Part 1

find = ['shiny gold']

res = 0

new_rules = rules

while(len(find) != 0):
    old_rules = new_rules
    new_rules = []
    current = find.pop()
    for rule in old_rules:
        outer = rule[0]
        used = False
        for _, color in rule[1:]:
            if color == current:
                res += 1
                find.append(outer)
                used = True
                break
        if not used:
            new_rules.append(rule)

print(res)

# Part 2

res = 0

print(weight('shiny gold')-1)