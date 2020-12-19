import re

def read_input(path, dimension=3):
    with open(path, 'r') as f:
        data = f.read()
    data = data.split('\n\n')

    rules = {int(line.split(':')[0]): ' '+line.split(':')[1].strip()+' ' for line in data[0].splitlines()}

    completed = set()
    to_use = []

    digits = re.compile('[0-9]+')
    for key, value in rules.items():
        if not digits.search(value):
            completed.add(key)
            to_use.append(key)
            rules[key] = '('+value.replace('"', '')+')'

    while len(completed) != len(rules):
        use = to_use.pop(0)
        val = rules[use]

        exp_to_find = re.compile(r'\b'+str(use)+r'\b')
        for key, value in rules.items():
            if exp_to_find.search(value):
                rules[key] = exp_to_find.sub(val, rules[key])
                if not digits.search(rules[key]):
                    completed.add(key)
                    to_use.append(key)
                    rules[key] = ' ('+rules[key].replace('"', '')+') '

    for key, value in rules.items():
        rules[key] = value.replace(' ', '')

    return rules, data[1].splitlines()

def update_rules(rules):
    rules[8] = '('+rules[42]+'+'+')'

    # Hackey way to set same number of repetitions for rule 42 and 31 in rule 11 
    rules[11] = '('+rules[42]+rules[31]+')'
    for i in range(2, 11):
        rules[11] += '|('+rules[42]+'{'+str(i)+'}'+rules[31]+'{'+str(i)+'})'
    rules[11] = '('+rules[11]+')'

    rules[0] = '('+rules[8]+rules[11]+')'

    return rules

rules, data = read_input('day19')

# Part 1

rule_to_find = re.compile('^'+rules[0]+'$')

matched = 0

for line in data:
    if rule_to_find.match(line):
        matched += 1

print(matched)

# Part 2

rules = update_rules(rules)

rule_to_find = re.compile('^'+rules[0]+'$')

matched = 0

for line in data:
    if rule_to_find.match(line):
        matched += 1

print(matched)