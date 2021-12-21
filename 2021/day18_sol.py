from collections import deque
from itertools import product
import string
from math import floor, ceil


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def find_left_regular(s_number, start):
    pos_start, pos_stop = None, None
    for idx, c in enumerate(s_number[start - 1 :: -1]):
        if c in string.digits:
            if not pos_stop:
                pos_stop = start - idx
                pos_start = start - 1 - idx
            else:
                pos_start = start - 1 - idx
        else:
            if pos_start:
                break

    return pos_start, pos_stop


def find_right_regular(s_number, start):
    pos_start, pos_stop = None, None
    for idx, c in enumerate(s_number[start + 1 :]):
        if c in string.digits:
            if not pos_start:
                pos_start = start + 1 + idx
                pos_stop = start + 2 + idx
            else:
                pos_stop = start + 2 + idx
        else:
            if pos_start:
                break

    return pos_start, pos_stop


def explode(s_number):
    open_stack = deque()
    close_idx = None
    for idx, c in enumerate(s_number):
        if c == "[":
            open_stack.append(idx)
        elif c == "]":
            if len(open_stack) > 4:
                close_idx = idx
                break
            else:
                open_stack.pop()
    try:
        open_idx = open_stack.pop()
    except:
        return -1, s_number

    current_pair = tuple(
        int(v) for v in s_number[open_idx + 1 : close_idx].split(",")
    )

    left = find_left_regular(s_number, open_idx)
    right = find_right_regular(s_number, close_idx)

    if left[0]:
        out = s_number[: left[0]]
        left_num = int(s_number[left[0] : left[1]]) + current_pair[0]
        out += str(left_num)
        out += s_number[left[1] : open_idx] + "0"
    else:
        out = s_number[:open_idx] + "0"

    if right[0]:
        out += s_number[close_idx + 1 : right[0]]
        right_num = int(s_number[right[0] : right[1]]) + current_pair[1]
        out += str(right_num)
        out += s_number[right[1] :]
    else:
        out += s_number[close_idx + 1 :]

    return open_idx, out


def split(s_number):
    start_idx = None
    end_idx = None
    for idx, c in enumerate(s_number):
        if c in string.digits:
            if start_idx == None:
                start_idx = idx
                end_idx = idx + 1
            else:
                end_idx = idx + 1
        else:
            if start_idx != None:
                val = int(s_number[start_idx:end_idx])
                if val > 9:
                    out = s_number[:start_idx]
                    left = str(floor(val / 2))
                    right = str(ceil(val / 2))
                    out += "[" + left + "," + right + "]"
                    out += s_number[end_idx:]
                    return start_idx, out
                else:
                    start_idx = None
                    end_idx = None

    if start_idx != None:
        val = int(s_number[start_idx:end_idx])
        if val > 9:
            out = s_number[:start_idx]
            left = str(floor(val / 2))
            right = str(ceil(val / 2))
            out += "[" + left + "," + right + "]"
            out += s_number[end_idx:]
            return start_idx, out

    return -1, s_number


def addition(s1, s2):
    return "[" + s1 + "," + s2 + "]"


def reduction_step(s):
    exp_idx, exp_out = explode(s)
    split_idx, split_out = split(s)

    if exp_idx == -1 and split_idx == -1:
        return s
    elif exp_idx != -1:
        return exp_out
    else:
        return split_out


def reduction(s):
    old_out = s
    out = reduction_step(s)

    while out != old_out:
        old_out = out
        out = reduction_step(old_out)

    return out


def magnitude_step(s_number):
    open_stack = deque()
    for idx, c in enumerate(s_number):
        if c == "[":
            open_stack.append(idx)
        elif c == "]":
            open_idx = open_stack.pop()
            close_idx = idx
            if not (
                ("[" in s_number[open_idx + 1 : close_idx])
                or ("]" in s_number[open_idx + 1 : close_idx])
            ):
                current_pair = tuple(
                    int(v)
                    for v in s_number[open_idx + 1 : close_idx].split(",")
                )
                val = 3 * current_pair[0] + 2 * current_pair[1]
                return (
                    True,
                    s_number[:open_idx] + str(val) + s_number[close_idx + 1 :],
                )

    return False, s_number


def magnitude(s_number):
    not_done, out = magnitude_step(s_number)

    while not_done:
        not_done, out = magnitude_step(out)

    return out


assert explode("[[[[[9,8],1],2],3],4]")[1] == "[[[[0,9],2],3],4]"
assert explode("[7,[6,[5,[4,[3,2]]]]]")[1] == "[7,[6,[5,[7,0]]]]"
assert explode("[[6,[5,[4,[3,2]]]],1]")[1] == "[[6,[5,[7,0]]],3]"
assert (
    explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")[1]
    == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
)
assert (
    explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")[1]
    == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
)

data = read_input("day18")

# Part 1

out = data[0]

for line in data[1:]:
    out = addition(out, line)
    out = reduction(out)

print(f"Magnitude of complete sum: {magnitude(out)}")

# Part 2

combs = [
    (x, y) for x, y in product(range(len(data)), range(len(data))) if x != y
]

magnitudes = []

for comb in combs:
    out = addition(data[comb[0]], data[comb[1]])
    out = reduction(out)
    magnitudes.append(int(magnitude(out)))

print(f"Maximal possible magnitude by adding two numbers: {max(magnitudes)}")
