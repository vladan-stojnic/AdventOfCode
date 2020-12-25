def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    data = [int(d) for d in data]

    return data

keys = read_input('day25')

card_key, door_key = keys

subject = 7

value = 1

card_loop_size = 0

while value != card_key:
    value *= subject
    value %= 20201227

    card_loop_size += 1

encryption_key = 1
for i in range(card_loop_size):
    encryption_key *= door_key
    encryption_key %= 20201227

print(encryption_key)