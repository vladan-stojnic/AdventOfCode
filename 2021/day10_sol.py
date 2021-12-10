from collections import deque
from statistics import median


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def matched(opened, closed):
    pairs = {"()", "[]", "{}", "<>"}

    return (opened + closed) in pairs


data = read_input("day10")

syntax_error_score = 0

syntax_error_values = {")": 3, "]": 57, "}": 1197, ">": 25137}
autocomplete_values = {"(": 1, "[": 2, "{": 3, "<": 4}

autocomplete_scores = []

for line in data:
    stack = deque()
    error = False
    for c in line:
        if c in {"(", "[", "{", "<"}:
            stack.append(c)
        else:
            opened = stack.pop()
            if not matched(opened, c):
                syntax_error_score += syntax_error_values[c]
                error = True
                break
    if not error:
        score = 0
        while len(stack) != 0:
            c = stack.pop()
            score = 5 * score + autocomplete_values[c]
        autocomplete_scores.append(score)


print(f"Syntax error score: {syntax_error_score}")
print(f"Autocomplete score: {median(autocomplete_scores)}")
