def check_password(password):
    last_val = None
    has_double = False
    for c in str(password):
        if c == last_val:
            has_double = True
        elif last_val != None and int(c) < int(last_val):
            return False

        last_val = c

    return has_double


def check_password_part2(password):
    if check_password(password):
        lengths = set()
        last_val = str(password)[0]
        length = 1
        for c in str(password)[1:]:
            if c == last_val:
                length += 1
            else:
                last_val = c
                lengths.add(length)
                length = 1

        lengths.add(length)

        return 2 in lengths

    return False


assert check_password(111111) == True
assert check_password(223450) == False
assert check_password(123789) == False


assert check_password_part2(112233) == True
assert check_password_part2(123444) == False
assert check_password_part2(111122) == True


# Part 1

START_VAL = 240298
END_VAL = 784956

valid_passwords = 0

for password in range(START_VAL, END_VAL + 1):
    if check_password(password):
        valid_passwords += 1

print(f"Number of valid passwords: {valid_passwords}")

# Part 2

valid_passwords = 0

for password in range(START_VAL, END_VAL + 1):
    if check_password_part2(password):
        valid_passwords += 1

print(f"Number of valid passwords: {valid_passwords}")
