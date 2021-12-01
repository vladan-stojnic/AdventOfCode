import math

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    earliest_departure = int(data[0])

    bus_ids = [(offset, int(d)) for offset, d in enumerate(data[1].split(',')) if d != 'x']


    return earliest_departure, bus_ids

earliest_departure, bus_ids = read_input('day13')

# Part 1

departures = [math.ceil(earliest_departure/bus)*bus for _, bus in bus_ids]

diffs = [abs(earliest_departure-d) for d in departures]

min_diff = min(diffs)

bus_to_take = bus_ids[diffs.index(min_diff)][1]

print(min_diff*bus_to_take)

# Part 2

# Implements a sieve-search for modular equations

m = 1
s = None

for i, (remeinder, mod) in enumerate(bus_ids[:-1]):
    if s == None:
        s = (mod-remeinder)%mod
    m *= mod
    k = 0
    while True:
        ps = s + k*m
        if (ps % bus_ids[i+1][1]) == ((bus_ids[i+1][1]-bus_ids[i+1][0])%bus_ids[i+1][1]):
            s = ps
            break
        k += 1
    
print(s)