import re


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    drawn = [int(num) for num in data[0].split(",")]

    boards = []
    markings = []

    board = []
    marking = []
    for line in data[2:]:
        if line == "":
            boards.append(board)
            markings.append(marking)
            board = []
            marking = []
            continue

        line = line.strip()
        line = re.sub(" +", " ", line)

        board.append([int(num) for num in line.split(" ")])
        marking.append([False for _ in range(5)])

    boards.append(board)
    markings.append(marking)

    return drawn, boards, markings


def column_sum(marking, col):
    return sum([row[col] for row in marking])


def mark_boards(num, boards, markings, used_boards):
    winner = []
    for idx, (board, marking) in enumerate(zip(boards, markings)):
        if idx in used_boards:
            continue

        for board_row, marking_row in zip(board, marking):
            try:
                col_idx = board_row.index(num)
                marking_row[col_idx] = True

                if sum(marking_row) == 5:
                    winner.append(idx)

                if column_sum(marking, col_idx) == 5:
                    winner.append(idx)
            except ValueError:
                continue

    return winner


def sum_remaining_fields(board, marking):
    return sum(
        [
            sum(
                [
                    num if not mar else 0
                    for num, mar in zip(board_row, marking_row)
                ]
            )
            for board_row, marking_row in zip(board, marking)
        ]
    )


def play_bingo(drawn, boards, markings):
    used_boards = set()
    for num in drawn:
        winner = mark_boards(num, boards, markings, used_boards)
        if winner:
            used_boards.update(winner)
            sum_of_remaining = sum(
                sum_remaining_fields(boards[w], markings[w]) for w in winner
            )
            yield winner, sum_of_remaining * num


data = read_input("day4")

# Part 1

drawn, boards, markings = parse_data(data)

winner, score = next(play_bingo(drawn, boards, markings))

print(f"First to win: {winner} Score: {score}")

# Part 2

for winner, score in play_bingo(drawn, boards, markings):
    continue

print(f"Last to win: {winner} Score: {score}")
