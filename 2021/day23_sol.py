from abc import abstractmethod
from copy import deepcopy
from functools import lru_cache
from collections import Counter

homes = {
    2: "A",
    4: "B",
    6: "C",
    8: "D",
}


costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

part2_add = {
    "A": ("D", "D"),
    "B": ("C", "B"),
    "C": ("B", "A"),
    "D": ("A", "C"),
}


class Spot:
    def __init__(self, state):
        self.state = state

    def __repr__(self):
        return repr(self.state)

    def __hash__(self):
        return hash(self.state)

    @abstractmethod
    def is_free(self):
        pass

    @abstractmethod
    def get_amphipod(self):
        pass

    @abstractmethod
    def set_amphipod(self, amphipod):
        pass

    @abstractmethod
    def is_completed(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def is_room(self):
        pass

    @abstractmethod
    def can_be_put(self, amphipod):
        pass

    @abstractmethod
    def pop_amphipod(self):
        pass

    @abstractmethod
    def copy(self):
        pass


class Hallway(Spot):
    def __init__(self, state):
        super().__init__(state)

    def is_free(self):
        return self.state == "."

    def get_amphipod(self):
        if self.state == ".":
            raise ValueError("Tried to take amphipod from an empty spot!")

        return self.state, 0

    def pop_amphipod(self):
        if self.state == ".":
            raise ValueError("Tried to take amphipod from an empty spot!")

        self.state = "."

    def set_amphipod(self, amphipod):
        self.state = amphipod

        return 0

    def is_completed(self):
        return self.is_free()

    def is_empty(self):
        return self.is_free()

    def is_room(self):
        return False

    def can_be_put(self, amphipod):
        return self.is_free()

    def copy(self):
        return Hallway(deepcopy(self.state))

    def __eq__(self, __o: object):
        if not isinstance(__o, Hallway):
            return False
        return self.state == __o.state

    def __hash__(self):
        return hash(self.state)


class Room(Spot):
    def __init__(self, state, home_amphipod):
        super().__init__(state)
        self.home_amphipod = home_amphipod
        self.position_to_take = None
        for i, val in enumerate(self.state):
            if val != ".":
                self.position_to_take = i
                break

        if self.position_to_take == None:
            self.position_to_take = len(self.state)
        self.currently_there = Counter(self.state[self.position_to_take :])

    def is_free(self):
        return True

    def get_amphipod(self):
        if self.is_empty():
            raise ValueError("Tried to take amphipod from an empty spot!")
        return self.state[self.position_to_take], self.position_to_take + 1

    def pop_amphipod(self):
        if self.is_empty():
            raise ValueError("Tried to take amphipod from an empty spot!")
        self.currently_there[self.state[self.position_to_take]] -= 1
        if self.currently_there[self.state[self.position_to_take]] == 0:
            self.currently_there.pop(self.state[self.position_to_take])
        self.state = (
            self.state[: self.position_to_take]
            + (".",)
            + self.state[self.position_to_take + 1 :]
        )
        self.position_to_take += 1

    def set_amphipod(self, amphipod):
        if self.position_to_take <= 0:
            raise ValueError("Tried to put the amphipod to the full room")
        self.currently_there.update([amphipod])
        self.state = (
            self.state[: self.position_to_take - 1]
            + (amphipod,)
            + self.state[self.position_to_take :]
        )
        self.position_to_take -= 1

        return self.position_to_take + 1

    def is_completed(self):
        return self.currently_there.get(self.home_amphipod, 0) == len(
            self.state
        )

    def is_empty(self):
        return self.position_to_take >= len(self.state)

    def is_room(self):
        return True

    def can_be_put(self, amphipod):
        if self.home_amphipod != amphipod:
            return False

        return self.position_to_take > 0 and (
            (
                len(self.currently_there.keys()) == 1
                and self.currently_there.get(self.home_amphipod, 0) > 0
            )
            or (len(self.currently_there.keys()) == 0)
        )

    def is_sorted(self):
        return (
            len(self.currently_there.keys()) <= 1
            and self.currently_there.get(self.home_amphipod, 0) > 0
        )

    def copy(self):
        return Room(deepcopy(self.state), self.home_amphipod)

    def __eq__(self, __o: object):
        if not isinstance(__o, Room):
            return False
        return (
            self.state == __o.state and self.home_amphipod == __o.home_amphipod
        )

    def __hash__(self):
        return hash(self.state)


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    output = []

    for idx, val in enumerate(data[1]):
        if idx not in {3, 5, 7, 9}:
            output.append(Hallway(val))
        else:
            output.append(None)

    output = output[1:-1]

    for idx in range(3, 10, 2):
        room = tuple()
        for line in data[2:-1]:
            room = room + (line[idx],)
        output[idx - 1] = Room(room, homes[idx - 1])

    return tuple(output)


def is_finished(state):
    for position in state:
        if not position.is_completed():
            return False

    return True


def empty_path(state, old_idx, new_idx):
    if new_idx > old_idx:
        offset = 1
    else:
        offset = -1

    for i in range(old_idx + offset, new_idx, offset):
        if not state[i].is_free():
            return False

    return True


def is_valid_move(state, amphipod, old_idx, new_idx):
    if not empty_path(state, old_idx, new_idx):
        return False

    if state[old_idx].is_room():
        if state[old_idx].is_sorted():
            return False
        else:
            if state[new_idx].is_room():
                return state[new_idx].can_be_put(amphipod)
            else:
                return state[new_idx].is_free()
    else:
        if state[new_idx].is_room():
            return state[new_idx].can_be_put(amphipod)
        else:
            return False


def copy_state(state, position_idx, new_position_idx):
    if new_position_idx > position_idx:
        left_idx = position_idx
        right_idx = new_position_idx
    else:
        left_idx = new_position_idx
        right_idx = position_idx

    new_state = (
        state[:left_idx]
        + (state[left_idx].copy(),)
        + state[left_idx + 1 : right_idx]
        + (state[right_idx].copy(),)
        + state[right_idx + 1 :]
    )

    return new_state


@lru_cache(maxsize=None)
def find_neighbors(state):
    neighbors = []

    for position_idx, position in enumerate(state):
        if position.is_empty():
            continue

        if position.is_room() and position.is_sorted():
            continue

        amphipod, start_number_of_moves = state[position_idx].get_amphipod()

        for new_position_idx, new_position in enumerate(state):
            if new_position_idx == position_idx:
                continue

            if is_valid_move(state, amphipod, position_idx, new_position_idx):
                new_state = copy_state(state, position_idx, new_position_idx)

                new_state[position_idx].pop_amphipod()

                number_of_moves = start_number_of_moves

                number_of_moves += new_state[new_position_idx].set_amphipod(
                    amphipod
                )

                number_of_moves += abs(new_position_idx - position_idx)

                neighbors.append(
                    (new_state, number_of_moves * costs[amphipod])
                )

    return tuple(neighbors)


@lru_cache(maxsize=None)
def find_optimal(state):
    if is_finished(state):
        return 0

    cost_of_moves = []

    for neighbor, value in find_neighbors(state):
        cost = value + find_optimal(neighbor)
        cost_of_moves.append(cost)

    if len(cost_of_moves) == 0:
        cost_of_moves.append(float("inf"))

    return min(cost_of_moves)


def modify_part2(state):
    new_state = []

    for spot in state:
        if isinstance(spot, Hallway):
            new_state.append(deepcopy(spot))
        else:
            home_amphipod = spot.home_amphipod
            old_amphipods = spot.state
            new_state.append(
                Room(
                    (old_amphipods[0],)
                    + part2_add[home_amphipod]
                    + (old_amphipods[1],),
                    home_amphipod,
                )
            )

    return tuple(new_state)


data = read_input("day23")

state = parse_data(data)

# Part 1

print(f"Number of moves needed: {find_optimal(state)}")

# Part 2

find_neighbors.cache_clear()
find_optimal.cache_clear()

state = modify_part2(state)

print(f"Number of moves needed: {find_optimal(state)}")
