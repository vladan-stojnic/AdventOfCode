from itertools import compress
import numpy as np
import copy

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.split('\n\n')

    rules = {}
    my_ticket = None
    tickets = []

    for rule in data[0].splitlines():
        name, values = rule.split(':')
        values = values.strip()
        v1, v2 = values.split('or')
        v1, v2 = v1.strip(), v2.strip()
        v1_min = int(v1.split('-')[0])
        v1_max = int(v1.split('-')[1])
        v2_min = int(v2.split('-')[0])
        v2_max = int(v2.split('-')[1])

        rules[name] = [(v1_min, v1_max), (v2_min, v2_max)]

    my_ticket = [int(d) for d in data[1].splitlines()[1].split(',')]

    for ticket in data[2].splitlines()[1:]:
        tickets.append([int(t) for t in ticket.split(',')])


    return rules, my_ticket, tickets

def check_value_range(value, r):
    return r[0] <= value <= r[1]

def check_value(value, ranges):
    for r in ranges:
        if check_value_range(value, r):
            return True

    return False

def check_ticket(ticket, ranges):
    for value in ticket:
        if not check_value(value, ranges):
            return False

    return True

def check_all_values(values, ranges):
    for value in values:
        if not check_value(value, ranges):
            return False

    return True


def check_rules(values, rules):
    return [name for name, ranges in rules.items() if check_all_values(values, ranges)]

rules, my_ticket, tickets = read_input('day16')

# Part 1

rules_values = rules.values()

ranges = [item for rule in rules_values for item in rule]

tickets_values = [value for ticket in tickets for value in ticket]

not_valid = [not check_value(value, ranges) for value in tickets_values]

print(sum(compress(tickets_values, not_valid)))

# Part 2

valid = [check_ticket(t, ranges) for t in tickets]

valid_tickets = np.array(list(compress(tickets, valid)))

possible = [check_rules(valid_tickets[:, col], rules) for col in range(valid_tickets.shape[1])]

mapping = {}

possible = [(i, p) for i, p in enumerate(possible)]

possible = sorted(possible, key = lambda x: len(x[1]))

for i, p in possible:
    for f in p:
        if f not in mapping:
            mapping[f] = i

res = 1

for key, value in mapping.items():
    if key.startswith('departure'):
        res *= my_ticket[value]

print(res)