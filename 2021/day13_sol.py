def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    paper = set()
    instructions = []

    for line in data:
        if "," in line:
            splitted = line.split(",")
            paper.add((int(splitted[0]), int(splitted[1])))
        elif "=" in line:
            splitted = line.split("=")
            instructions.append((splitted[0][-1], int(splitted[1])))

    return paper, instructions


def fold_horizontal(paper, pos):
    new_paper = set()

    for x, y in paper:
        if y < pos:
            new_paper.add((x, y))
        elif y > pos:
            new_y = (pos - (y % pos)) % pos
            new_paper.add((x, new_y))
        else:
            raise ValueError("Dot at folding line!")

    return new_paper


def fold_vertical(paper, pos):
    new_paper = set()

    for x, y in paper:
        if x < pos:
            new_paper.add((x, y))
        elif x > pos:
            new_x = (pos - (x % pos)) % pos
            new_paper.add((new_x, y))
        else:
            raise ValueError("Dot at folding line!")

    return new_paper


def print_paper(paper):
    max_x, _ = max(paper, key=lambda x: x[0])
    _, max_y = max(paper, key=lambda x: x[1])

    for j in range(max_y + 1):
        for i in range(max_x + 1):
            if (i, j) in paper:
                print("#", end="")
            else:
                print(".", end="")
        print()


data = read_input("day13")

paper, instructions = parse_data(data)

# Part 1

for axis, val in [instructions[0]]:
    if axis == "y":
        paper = fold_horizontal(paper, val)
    else:
        paper = fold_vertical(paper, val)

print(f"Number of dots after first fold: {len(paper)}")

# Part 2

for axis, val in instructions[1:]:
    if axis == "y":
        paper = fold_horizontal(paper, val)
    else:
        paper = fold_vertical(paper, val)

print_paper(paper)
