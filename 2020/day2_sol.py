def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()
    data = [d.split(' ') for d in data]
    output = []
    for d in data:
        row = []
        min_max = d[0].split('-')
        row.append((int(min_max[0]), int(min_max[1])))
        char = d[1][0]
        row.append(char)
        row.append(d[2])
        output.append(row)
    
    return output

data = read_input('day2')

# Part 1

valid = 0
for min_max, char, password in data:
    count = password.count(char)
    if min_max[0] <= count <= min_max[1]:
        valid += 1

print (valid)

# Part 2

valid = 0
for indices, char, password in data:
    if (password[indices[0]-1] == char) ^ (password[indices[1]-1] == char):
        valid += 1

print(valid)