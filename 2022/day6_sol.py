def read_input(path):
    with open(path, "r") as f:
        data = f.read()
    # data = data.splitlines()

    return data


def find_start(data, num_distinct=4):
    for idx in range(num_distinct, len(data) + 1):
        if len(set(data[idx - num_distinct : idx])) == num_distinct:
            return idx


data = read_input("day6")

# Part 1

assert find_start("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
assert find_start("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
assert find_start("nppdvjthqldpwncqszvftbrmjlhg") == 6
assert find_start("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
assert find_start("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

print(f"Start of packet marker found at: {find_start(data)}")

# Part 2

assert find_start("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
assert find_start("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
assert find_start("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
assert find_start("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
assert find_start("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26

print(f"Start of message marker found at: {find_start(data, 14)}")
