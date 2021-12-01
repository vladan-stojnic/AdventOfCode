def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    data = [(d.split('=')[0].strip(), d.split('=')[1].strip()) for d in data]


    return data

def get_address(command):
    addr = command.split('[')[1]
    addr = int(addr[:-1])

    return addr

def mask_value(value, mask):
    bin_val = format(value, '036b')

    out = ''

    for v, m in zip(bin_val, mask):
        if m == 'X':
            out += v
        else:
            out += m

    out = int(out, base=2)

    return out

def get_masked_address(command, mask):
    addr = get_address(command)

    bin_addr = format(addr, '036b')

    out = ''

    x_loc = []

    for i, (v, m) in enumerate(zip(bin_addr, mask)):
        if m == '0':
            out += v
        elif m == '1':
            out += m
        else:
            x_loc.insert(0, 35-i)
            out += '0'

    outs = [int(out, base=2)]
    for loc in x_loc:
        off = 2**loc

        new_outs = []
        for o in outs:
            new_outs.append(o+off)
        
        outs += new_outs

    return outs

    

data = read_input('day14')

# Part 1

mask = 'X'*36

memory = {}

for command, value in data:
    if command == 'mask':
        mask = value
    else:
        addr = get_address(command)
        memory[addr] = mask_value(int(value), mask)

print(sum(memory.values()))

# Part 2

mask = 'X'*36

memory = {}

for command, value in data:
    if command == 'mask':
        mask = value
    else:
        addrs = get_masked_address(command, mask)
        for addr in addrs:
            memory[addr] = int(value)

print(sum(memory.values()))