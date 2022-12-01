def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()

    return data


def parse_data(data):
    out = []
    elf = []
    for d in data:
        if d == "":
            out.append(elf)
            elf = []
        else:
            elf.append(int(d))

    return out


data = read_input("day1")

data = parse_data(data)

calories_per_elf = [sum(elf) for elf in data]

# Part 1
print(f"Max calories per elf: {max(calories_per_elf)}")

# Part 2
calories_per_elf_sorted = sorted(calories_per_elf)

print(f"Calories carried by top 3 elves: {sum(calories_per_elf_sorted[-3:])}")
