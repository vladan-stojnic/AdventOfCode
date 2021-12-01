import re

def read_input(path, dimension=3):
    with open(path, 'r') as f:
        data = f.read()
    data = data.splitlines()

    return data

def create_rpn(expression, symbols):
    digit = re.compile('[0-9]')

    output = []
    stack = []


    num_str = ''
    for char in expression:
        if digit.match(char):
            num_str += char
        elif char in symbols:
            if num_str != '':
                num = int(num_str)
                output.append(num)
                num_str = ''

            if stack:
                if char != '(':
                    if symbols[char] <= symbols[stack[-1]]:
                        output.append(stack.pop())
                    
            stack.append(char)
        elif char == ')':
            if num_str != '':
                num = int(num_str)
                output.append(num)
                num_str = ''

            while True:
                s = stack.pop()

                if s == '(':
                    break
                else:
                    output.append(s)

    if len(num_str) != 0:
        output.append(int(num_str))

    if stack:
        while stack:
            output.append(stack.pop())

    return output

def evaluate_rpn(rpn):
    ops = {'+': lambda x, y: x+y, '*': lambda x, y: x*y}


    stack = []
    for elem in rpn:
        if elem in ops:
            y = stack.pop()
            x = stack.pop()
            stack.append(ops[elem](x, y))
        else:
            stack.append(elem)

    return stack[0]

def solve_expression(expression, symbols = {'+': 1, '*': 1, '(': 0}):
    rpn = create_rpn(expression, symbols)

    return evaluate_rpn(rpn)

data = read_input('day18')

# Part 1

assert solve_expression('1 + 2 * 3 + 4 * 5 + 6') == 71
assert solve_expression('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert solve_expression('2 * 3 + (4 * 5)') == 26
assert solve_expression('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert solve_expression('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert solve_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

res = [int(solve_expression(d)) for d in data]

print(sum(res))

# Part 2

assert solve_expression('1 + 2 * 3 + 4 * 5 + 6', {'+': 2, '*': 1, '(': 0}) == 231
assert solve_expression('1 + (2 * 3) + (4 * (5 + 6))', {'+': 2, '*': 1, '(': 0}) == 51
assert solve_expression('2 * 3 + (4 * 5)', {'+': 2, '*': 1, '(': 0}) == 46
assert solve_expression('5 + (8 * 3 + 9 + 3 * 4 * 3)', {'+': 2, '*': 1, '(': 0}) == 1445
assert solve_expression('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', {'+': 2, '*': 1, '(': 0}) == 669060
assert solve_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', {'+': 2, '*': 1, '(': 0}) == 23340

res = [int(solve_expression(d, {'+': 2, '*': 1, '(': 0})) for d in data]

print(sum(res))