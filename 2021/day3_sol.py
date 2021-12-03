def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def find_most_common_bit(data, position):
    counter = [0, 0]

    for num in data:
        counter[int(num[position])] += 1

    if counter[0] > counter[1]:
        return "0"
    else:
        return "1"


def find_ratings(data, position=0, rating_type="oxygen"):
    if len(data) == 1:
        return int(data[0], base=2)

    new_data = []

    common = find_most_common_bit(data, position)

    for num in data:
        if rating_type == "oxygen":
            if num[position] == common:
                new_data.append(num)
        else:
            if num[position] != common:
                new_data.append(num)

    return find_ratings(new_data, position + 1, rating_type)


data = read_input("day3")

# Part 1

gamma = ""
epsilon = ""

for pos in range(len(data[0])):
    common = find_most_common_bit(data, pos)
    gamma += common
    epsilon += "1" if common == "0" else "0"


gamma = int(gamma, base=2)
epsilon = int(epsilon, base=2)

print(f"Power consumtion: {gamma * epsilon}")

# Part 2

oxygen_rating = find_ratings(data)
co2_rating = find_ratings(data, rating_type="co2")

print(f"Life support rating: {oxygen_rating * co2_rating}")

