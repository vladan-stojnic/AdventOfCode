import numpy as np
from scipy.signal import correlate2d


class InfiniteImage:
    def __init__(self, image, border_val):
        self.image = image
        self.border_val = border_val
        self.enchance_kernel = np.reshape(2 ** np.arange(8, -1, -1), (3, 3))

    def enchance(self, algorithm):
        idxs = correlate2d(
            self.image, self.enchance_kernel, fillvalue=self.border_val
        )

        self.image = algorithm[idxs]

        if self.border_val == 0:
            border = np.zeros((3, 3), dtype=np.int16)
        else:
            border = np.ones((3, 3), dtype=np.int16)

        idxs = correlate2d(border, self.enchance_kernel, mode="valid")

        self.border_val = algorithm[idxs][0, 0]

    def num_of_light_pixels(self):
        if self.border_val == 1:
            return float("inf")

        return np.sum(self.image)


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    algorithm = [1 if c == "#" else 0 for c in data[0]]

    image = []

    for line in data[2:]:
        image_row = [1 if c == "#" else 0 for c in line]
        image.append(image_row)

    return np.array(algorithm), InfiniteImage(np.array(image), 0)


data = read_input("day20")

algorithm, image = parse_data(data)

# Part 1

NUM_STEPS_1 = 2

for _ in range(NUM_STEPS_1):
    image.enchance(algorithm)

print(
    f"Number of light pixels after {NUM_STEPS_1} steps of enchancement: {image.num_of_light_pixels()}"
)

# Part 2

NUM_STEPS_2 = 50

for _ in range(NUM_STEPS_1, NUM_STEPS_2):
    image.enchance(algorithm)

print(
    f"Number of light pixels after {NUM_STEPS_2} steps of enchancement: {image.num_of_light_pixels()}"
)
