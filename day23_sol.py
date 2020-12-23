import math

class Node:
    def __init__(self, value=None, next_node=None):
        self.value = value
        self.next_node = next_node

class CircularList:
    def __init__(self, values=None):
        self.head = None
        self.length = 0
        self.min = None
        self.max = None
        self.elements = {}
        if values:
            node = None
            last = None
            self.length = len(values)
            for val in values[::-1]:
                node = Node(val, node)
                self.elements[val] = node
                if not last:
                    last = node
                if not self.min:
                    self.min = val
                else:
                    if val < self.min:
                        self.min = val
                
                if not self.max:
                    self.max = val
                else:
                    if val > self.max:
                        self.max = val

            self.head = node
            last.next_node = self.head

    def __str__(self):
        nxt = self.head
        out = []
        for i in range(self.length):
            out.append(str(nxt.value))
            nxt = nxt.next_node

        return ','.join(out)

    def get_element(self, value):
        if value in self.elements:
            return self.elements[value]

        return None

def play_game(cups, num_turns=100):
    current = cups.head
    min_value = cups.min
    max_value = cups.max

    for i in range(num_turns):
        removed_start = current.next_node
        tmp = current
        removed_values = []
        for i in range(3):
            tmp = tmp.next_node
            removed_values.append(tmp.value)

        removed_end = tmp

        destination = current.value
        while True:
            destination -= 1
            if destination < min_value:
                destination = max_value

            destination_node = cups.get_element(destination)

            if destination_node and destination_node.value not in removed_values:
                old_nxt = destination_node.next_node

                old_removed = removed_end.next_node

                destination_node.next_node = removed_start

                removed_end.next_node = old_nxt

                current.next_node = old_removed

                current = current.next_node

                break
    
    return cups

def part1(start_order, num_turns=100):
    cups = list(start_order)
    cups = [int(cup) for cup in cups]

    cups = CircularList(cups)

    cups = play_game(cups, num_turns=num_turns)

    tmp = cups.get_element(1)
    out = ''
    for i in range(cups.length-1):
        tmp = tmp.next_node
        out += str(tmp.value)

    return out

def part2(start_order, num_turns=10000000):
    cups = list(start_order)
    cups = [int(cup) for cup in cups]

    min_value = min(cups)
    max_value = max(cups)

    for i in range(max_value+1, 1000001):
        cups.append(i)

    cups = CircularList(cups)

    cups = play_game(cups, num_turns=num_turns)

    tmp = cups.get_element(1)
    out = []
    for i in range(2):
        tmp = tmp.next_node
        out.append(tmp.value)

    return math.prod(out)

# Part 1

assert part1('389125467', 10) == '92658374'
assert part1('389125467') == '67384529'

print(part1('916438275'))

# Part 2

assert part2('389125467') == 149245887792

print(part2('916438275'))