from collections import defaultdict
import heapq
import itertools

import numpy as np


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
    transformed_data = []
    start_loc = None
    end_loc = None

    for i, row in enumerate(data):
        row_vals = []
        for j, val in enumerate(row):
            if val == "S":
                start_loc = (i, j)
                row_vals.append(ord("a"))
            elif val == "E":
                end_loc = (i, j)
                row_vals.append(ord("z"))
            else:
                row_vals.append(ord(val))
        transformed_data.append(row_vals)

    return np.array(transformed_data), start_loc, end_loc


def get_neighbors(data, loc, reverse=False):
    i, j = loc
    val = data[i, j]
    valid_neighbors = []

    if i - 1 >= 0:
        n_val = data[i - 1, j]
        if not reverse:
            if n_val <= val + 1:
                valid_neighbors.append(((i - 1, j), n_val))
        else:
            if n_val + 1 >= val:
                valid_neighbors.append(((i - 1, j), n_val))

    if i + 1 < data.shape[0]:
        n_val = data[i + 1, j]
        if not reverse:
            if n_val <= val + 1:
                valid_neighbors.append(((i + 1, j), n_val))
        else:
            if n_val + 1 >= val:
                valid_neighbors.append(((i + 1, j), n_val))

    if j - 1 >= 0:
        n_val = data[i, j - 1]
        if not reverse:
            if n_val <= val + 1:
                valid_neighbors.append(((i, j - 1), n_val))
        else:
            if n_val + 1 >= val:
                valid_neighbors.append(((i, j - 1), n_val))

    if j + 1 < data.shape[1]:
        n_val = data[i, j + 1]
        if not reverse:
            if n_val <= val + 1:
                valid_neighbors.append(((i, j + 1), n_val))
        else:
            if n_val + 1 >= val:
                valid_neighbors.append(((i, j + 1), n_val))

    return valid_neighbors


def find_shortest_path(data, source, target=None, reverse=False):
    dist = defaultdict(lambda: float("inf"))
    steps = defaultdict(lambda: float("inf"))
    pqueue = PriorityQueue()

    pqueue.push(source, 0)
    dist[source] = 0
    steps[source] = 0

    while len(pqueue) != 0:
        u = pqueue.pop()

        if u == target:
            return steps[u]

        for neighbor, n_val in get_neighbors(data, u, reverse):
            alt = dist[u] + n_val
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                steps[neighbor] = steps[u] + 1
                pqueue.push(neighbor, alt)

    return steps


data = read_input("day12")

grid, start_loc, end_loc = parse_data(data)

# Part 1
dist = find_shortest_path(grid, start_loc, end_loc)

print(f"Path has a length of: {dist}")

# Part 2
possible_starts = list(zip(*np.where(grid == ord("a"))))

dist = find_shortest_path(grid, end_loc, reverse=True)

print(f"Shortest possible path: {min(dist[ps] for ps in possible_starts)}")
