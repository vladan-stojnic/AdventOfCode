def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()
    #data = [int(d) for d in data]
    
    return data

def check_byr(value):
    try:
        year = int(value)
        if 1920 <= year <= 2002:
            return True
        return False
    except:
        return False

def check_iyr(value):
    try:
        year = int(value)
        if 2010 <= year <= 2020:
            return True
        return False
    except:
        return False

def check_eyr(value):
    try:
        year = int(value)
        if 2020 <= year <= 2030:
            return True
        return False
    except:
        return False

def check_hgt(value):
    try:
        unit = value[-2:]
        value = int(value[:-2])

        if unit == 'cm' and 150 <= value <= 193:
            return True
        elif unit == 'in' and 59 <= value <= 76:
            return True
        else:
            return False
    except:
        return False

def check_hcl(value):
    try:
        if not value.startswith('#'):
            return False

        value = value[1:]
        value = int(value, 16)

        return True
    except:
        return False

def check_ecl(value):
    return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def check_pid(value):
    try:
        value_num = int(value)

        if len(value) == 9:
            return True
        else:
            return False
    except:
        return False

def check_field(field, value):
    if field == 'byr':
        return check_byr(value)
    elif field == 'iyr':
        return check_iyr(value)
    elif field == 'eyr':
        return check_eyr(value)
    elif field == 'hgt':
        return check_hgt(value)
    elif field == 'hcl':
        return check_hcl(value)
    elif field == 'ecl':
        return check_ecl(value)
    elif field == 'pid':
        return check_pid(value)
    return False

data = read_input('day4')

mapping = {'byr': 0, 'iyr': 1, 'eyr': 2, 'hgt': 3, 'hcl': 4, 'ecl': 5, 'pid': 6, 'cid': 7}

# Part 1

pass_valid = ['0']*8

num_valid = 0
num_pass = 0

for line in data:
    if line == '':
        if ''.join(pass_valid).startswith('1111111'):
            num_valid += 1
        pass_valid = ['0']*8
        continue

    for field_value in line.split(' '):
        field = field_value[:3]
        if field in mapping:
            pass_valid[mapping[field]] = '1'

if ''.join(pass_valid).startswith('1111111'):
    num_valid += 1

print(num_valid)

# Part 2

pass_valid = ['0']*8

num_valid = 0
num_pass = 0

for line in data:
    if line == '':
        if ''.join(pass_valid).startswith('1111111'):
            num_valid += 1
        pass_valid = ['0']*8
        continue

    for field_value in line.split(' '):
        field, value = field_value.split(':')
        if field in mapping and check_field(field, value):
            pass_valid[mapping[field]] = '1'

if ''.join(pass_valid).startswith('1111111'):
    num_valid += 1

print(num_valid)