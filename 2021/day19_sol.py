import itertools
from collections import Counter

import numpy as np


class Scanner:
    def __init__(self, idx, readings, location):
        self.idx = idx
        self.readings = readings
        self.location = location

    def __repr__(self):
        return f"Scanner: {self.idx} \n {self.readings}"


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    output = []

    for line in data:
        if line.startswith("---"):
            readings = []
            scanner = int(line.split(" ")[2])
        elif line == "":
            output.append(
                Scanner(scanner, np.array(readings), np.array([[0, 0, 0]]))
            )
        else:
            readings.append(np.array([int(v) for v in line.split(",")]))

    output.append(Scanner(scanner, np.array(readings), np.array([[0, 0, 0]])))

    return output


def sin90(x):
    if x == 0:
        return 0
    elif x == 90:
        return 1
    elif x == 180:
        return 0
    elif x == 270:
        return -1
    else:
        raise ValueError("Not supported value!")


def cos90(x):
    if x == 0:
        return 1
    elif x == 90:
        return 0
    elif x == 180:
        return -1
    elif x == 270:
        return 0
    else:
        raise ValueError("Not supported value!")


def get_rot_matrix_x(angle):
    return np.array(
        [
            [1, 0, 0],
            [0, cos90(angle), -sin90(angle)],
            [0, sin90(angle), cos90(angle)],
        ]
    )


def get_rot_matrix_y(angle):
    return np.array(
        [
            [cos90(angle), 0, sin90(angle)],
            [0, 1, 0],
            [-sin90(angle), 0, cos90(angle)],
        ]
    )


def get_rot_matrix_z(angle):
    return np.array(
        [
            [cos90(angle), -sin90(angle), 0],
            [sin90(angle), cos90(angle), 0],
            [0, 0, 1],
        ]
    )


def get_rot_hash(rot):
    flattened = rot.flatten()
    flattened += 1

    hash_val = 0
    for idx, val in enumerate(flattened[::-1]):
        hash_val += val * 3 ** idx

    return hash_val


def get_all_rotations():
    output = []
    used = set()

    angles = {0, 90, 180, 270}

    for x in angles:
        rot_x = get_rot_matrix_x(x)
        for y in angles:
            rot_y = get_rot_matrix_y(y)
            for z in angles:
                rot_z = get_rot_matrix_z(z)
                rot = rot_z @ rot_y @ rot_x
                rot_hash = get_rot_hash(rot)
                if rot_hash not in used:
                    used.add(rot_hash)
                    output.append(rot)

    return output


def rotate_scanner(scanner, rot):
    readings = scanner.readings
    location = scanner.location

    rotated = np.transpose(rot @ np.transpose(readings)).astype(np.int32)
    rotated_location = np.transpose(rot @ np.transpose(location)).astype(
        np.int32
    )

    return Scanner(scanner.idx, rotated, rotated_location)


def translate_scanner(scanner, tran):
    readings = scanner.readings
    location = scanner.location

    translated = readings + tran
    translated_location = location + tran

    return Scanner(scanner.idx, translated, translated_location)


def readings_to_set(readings):
    return set(map(tuple, readings))


def find_matchings(s1, s2, all_rotations):
    for rot in all_rotations:
        rotated = rotate_scanner(s2, rot)
        diffs = (
            s1.readings[np.newaxis, :, :] - rotated.readings[:, np.newaxis, :]
        )
        diffs = diffs.reshape((-1, 3))
        counts = Counter(map(tuple, diffs))
        pos, count = counts.most_common(1)[0]
        if count >= 12:
            return pos, rot

    return None, None


def find_reconstructions(data):
    all_rotations = get_all_rotations()

    reconstructions = {}
    found = set([0])
    to_search = set([0])

    while len(found) < len(data):
        new_found = set()
        for s1_idx, s2_idx in itertools.product(
            to_search, set(range(len(data))).difference(found)
        ):
            s1 = data[s1_idx]
            s2 = data[s2_idx]

            pos, rot = find_matchings(s1, s2, all_rotations)

            if pos != None:
                new_found.add(s2_idx)
                if s1_idx == 0:
                    reconstructions[s2_idx] = [(rot, pos)]
                else:
                    reconstructions[s2_idx] = [(rot, pos)] + reconstructions[
                        s1_idx
                    ]
        found.update(new_found)
        to_search = new_found

    return reconstructions


def reconstruct_map(data, reconstructions):
    beacons = set(readings_to_set(data[0].readings))
    scanners = set([(0, 0, 0)])

    for idx, scanner in enumerate(data[1:], start=1):
        reconstructed = scanner
        for rot, tran in reconstructions[idx]:
            reconstructed = translate_scanner(
                rotate_scanner(reconstructed, rot), tran
            )
        beacons.update(readings_to_set(reconstructed.readings))
        scanners.update(readings_to_set(reconstructed.location))

    return beacons, scanners


def find_max_distance(scanners):
    max_dist = 0

    scanners = list(scanners)

    for pos1_idx, pos2_idx in itertools.product(
        range(len(scanners)), range(len(scanners))
    ):
        pos1 = scanners[pos1_idx]
        pos2 = scanners[pos2_idx]
        dist = (
            abs(pos1[0] - pos2[0])
            + abs(pos1[1] - pos2[1])
            + abs(pos1[2] - pos2[2])
        )

        if dist > max_dist:
            max_dist = dist

    return max_dist


data = read_input("day19")

data = parse_data(data)

reconstructions = find_reconstructions(data)

beacons, scanners = reconstruct_map(data, reconstructions)

# Part 1

print(f"Number of beacons: {len(beacons)}")

# Part 2

max_dist = find_max_distance(scanners)

print(f"Maximal distance between scanners: {max_dist}")

