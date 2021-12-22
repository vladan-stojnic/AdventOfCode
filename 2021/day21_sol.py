from dataclasses import dataclass
import itertools
from functools import lru_cache


@dataclass
class Player:
    name: str
    position: int
    score: int

    def increase_position(self, increment) -> None:
        self.position += increment
        self.position %= 10
        self.score += self.position + 1


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    data = data.splitlines()

    return data


def parse_data(data):
    p1 = int(data[0].split(": ")[1])
    p2 = int(data[1].split(": ")[1])

    return Player("Player 1", p1 - 1, 0), Player("Player 2", p2 - 1, 0)


@lru_cache(maxsize=None)
def play_part2(
    current_position, current_score, next_position, next_score, rolls
):
    if current_score >= 21:
        return 1, 0

    if next_score >= 21:
        return 0, 1

    current_wins, next_wins = 0, 0

    for roll in rolls:
        current_new_position = (current_position + roll) % 10
        current_new_score = current_score + current_new_position + 1

        nw, cw = play_part2(
            next_position,
            next_score,
            current_new_position,
            current_new_score,
            rolls,
        )

        current_wins += cw
        next_wins += nw

    return current_wins, next_wins


# Part 1

current_player, next_player = parse_data(read_input("day21"))

move = 0

for idx, roll in enumerate(itertools.cycle(range(1, 101)), start=1):
    move += roll
    if idx % 3 == 0:
        current_player.increase_position(move)
        if current_player.score >= 1000:
            break
        current_player, next_player = next_player, current_player
        move = 0

print(f"Answer: {next_player.score * idx}")

# Part 2

current_player, next_player = parse_data(read_input("day21"))

ROLLS = tuple(
    map(sum, itertools.product(range(1, 4), range(1, 4), range(1, 4)))
)

wins = play_part2(
    current_player.position,
    current_player.score,
    next_player.position,
    next_player.score,
    ROLLS,
)

print(f"Maximal number of wins in universes: {max(wins)}")
