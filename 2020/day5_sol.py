def read_data(path):
    with open(path, 'r') as f:
        data = f.read()
    
    data = data.splitlines()

    return data

def decode_pass(p):
    p = p.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')

    id = int(p[:7], 2)*8 + int(p[7:], 2)

    return id

data = read_data('day5')

passes = sorted([decode_pass(p) for p in data])

# Part 1
print(passes[-1])

# Part 2

diffs = [passes[i]-passes[i-1] for i in range(1, len(passes))]

print(passes[diffs.index(2)]+1)