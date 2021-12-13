from collections import defaultdict
from copy import deepcopy


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    connections = defaultdict(list)

    for line in data:
        splitted = line.split("-")
        connections[splitted[0]].append(splitted[1])
        connections[splitted[1]].append(splitted[0])

    return connections


def find_all_valid_paths_part1(graph, start, end, visited, path):
    visited.add(start)
    path = path + start + "-"
    to_visit = graph[start]

    found_paths = []

    for visit in to_visit:
        if visit == end:
            path = path + end
            found_paths.append(path)
        elif visit.islower():
            if visit not in visited:
                found_paths = found_paths + find_all_valid_paths_part1(
                    graph, visit, end, deepcopy(visited), deepcopy(path),
                )
        else:
            found_paths = found_paths + find_all_valid_paths_part1(
                graph, visit, end, deepcopy(visited), deepcopy(path),
            )

    return found_paths


def find_all_valid_paths_part2(graph, start, end, visited, path):
    if start.islower():
        visited[start] += 1
    path = path + start + "-"
    to_visit = graph[start]

    found_paths = []

    for visit in to_visit:
        if visit == "start":
            continue
        elif visit == end:
            path = path + end
            found_paths = found_paths + [path]
        elif visit.islower():
            if visited[visit] == 0:
                found_paths = found_paths + find_all_valid_paths_part2(
                    graph, visit, end, deepcopy(visited), deepcopy(path),
                )
            elif visited[visit] == 1:
                if not any(map(lambda x: x > 1, visited.values())):
                    found_paths = found_paths + find_all_valid_paths_part2(
                        graph, visit, end, deepcopy(visited), deepcopy(path),
                    )
        else:
            found_paths = found_paths + find_all_valid_paths_part2(
                graph, visit, end, deepcopy(visited), deepcopy(path),
            )

    return found_paths


graph = parse_data(read_input("day12"))

# Part 1

found_paths = find_all_valid_paths_part1(graph, "start", "end", set(), "")

print(f"Number of possible paths: {len(found_paths)}")

# Part 2

found_paths = find_all_valid_paths_part2(
    graph, "start", "end", defaultdict(lambda: 0), ""
)

print(f"Number of possible paths: {len(found_paths)}")
