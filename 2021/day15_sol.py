import heapq
import itertools
from collections import defaultdict


class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = "REMOVED"
        self.counter = itertools.count()

    def push(self, task, priority=0):
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop(self):
        while self.pq:
            _, _, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError("Pop from an empty priority queue")

    def __len__(self):
        return len(self.pq)


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    output = []

    for line in data:
        row = [int(val) for val in line]
        output.append(row)

    return output


def get_neighbors(data, loc, full=False):
    i, j = loc
    neighbors = []

    if i - 1 >= 0:
        neighbors.append((i - 1, j))
    if (full and (i + 1 < 5 * len(data))) or (
        not full and (i + 1 < len(data))
    ):
        neighbors.append((i + 1, j))

    if j - 1 >= 0:
        neighbors.append((i, j - 1))
    if (full and (j + 1 < 5 * len(data[0]))) or (
        not full and (j + 1 < len(data[0]))
    ):
        neighbors.append((i, j + 1))

    return neighbors


def get_value(data, loc):
    i, j = loc
    x, y = len(data), len(data[0])

    val = data[i % x][j % y] + i // x + j // y

    if val > 9:
        return (val % 10) + 1
    else:
        return val


def find_mininal_value_in_dict(d, visited):
    min_val = float("inf")
    min_key = None

    for key in visited:
        if d[key] < min_val:
            min_val = d[key]
            min_key = key

    return min_key


def find_shortest_path(data, source, target, full=False):
    dist = defaultdict(lambda: float("inf"))
    pqueue = PriorityQueue()

    pqueue.push(source, 0)
    dist[source] = 0

    while len(pqueue) != 0:
        u = pqueue.pop()

        if u == target:
            return dist[u]

        for neighbor in get_neighbors(data, u, full):
            alt = dist[u] + get_value(data, neighbor)
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                pqueue.push(neighbor, alt)


data = read_input("day15")

# Part 1

data = parse_data(data)

SOURCE = (0, 0)
TARGET = (len(data) - 1, len(data[0]) - 1)

lowest_risk_path = find_shortest_path(data, SOURCE, TARGET)

print(f"Risk of the lowest risk path is {lowest_risk_path}")

# Part 2

TARGET = (5 * len(data) - 1, 5 * len(data[0]) - 1)

lowest_risk_path = find_shortest_path(data, SOURCE, TARGET, full=True)

print(f"Risk of the lowest risk path is {lowest_risk_path}")
