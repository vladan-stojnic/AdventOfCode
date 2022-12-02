def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    data = data.splitlines()
    data = [d.split(" ") for d in data]

    return data


def game_score(opponent, me):
    if opponent == "R":
        if me == "R":
            return 3 + 1
        elif me == "P":
            return 6 + 2
        elif me == "S":
            return 0 + 3
    elif opponent == "P":
        if me == "R":
            return 0 + 1
        elif me == "P":
            return 3 + 2
        elif me == "S":
            return 6 + 3
    elif opponent == "S":
        if me == "R":
            return 6 + 1
        elif me == "P":
            return 0 + 2
        elif me == "S":
            return 3 + 3


def mapping_part2(opponent, me):
    if opponent == "R":
        if me == "X":
            return "S"
        elif me == "Y":
            return "R"
        elif me == "Z":
            return "P"
    elif opponent == "P":
        if me == "X":
            return "R"
        elif me == "Y":
            return "P"
        elif me == "Z":
            return "S"
    elif opponent == "S":
        if me == "X":
            return "P"
        elif me == "Y":
            return "S"
        elif me == "Z":
            return "R"


data = read_input("day2")

# Part 1

mapping = {"A": "R", "B": "P", "C": "S", "X": "R", "Y": "P", "Z": "S"}

data_part1 = [
    (mapping[game_round[0]], mapping[game_round[1]]) for game_round in data
]

scores_per_game = [game_score(*game) for game in data_part1]

print(f"Total score: {sum(scores_per_game)}")

# Part 2

data_part2 = [
    (
        mapping[game_round[0]],
        mapping_part2(mapping[game_round[0]], game_round[1]),
    )
    for game_round in data
]

scores_per_game = [game_score(*game) for game in data_part2]

print(f"Total score: {sum(scores_per_game)}")
