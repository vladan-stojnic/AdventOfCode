from collections import defaultdict

def play_game(start, turns=2020):
    played = start.split(',')
    memory = defaultdict(lambda: (0, 0, 0))

    for i, p in enumerate(played):
        times, idx, _ = memory[int(p)]
        memory[int(p)] = (times+1, i+1, idx)

    current = int(played[-1])

    for i in range(len(played), turns):
        times, idx, old_idx = memory[current]
        if times == 1:
            current = 0
        else:
            current = idx - old_idx
        times, idx, old_idx = memory[current]
        memory[current] = (times+1, i+1, idx)

    return current

# Part 1

assert play_game('1,3,2') == 1
assert play_game('2,1,3') == 10
assert play_game('1,2,3') == 27
assert play_game('2,3,1') == 78
assert play_game('3,2,1') == 438
assert play_game('3,1,2') == 1836

print(play_game('15,5,1,4,7,0'))

# Part 2

assert play_game('0,3,6', 30000000) == 175594
assert play_game('1,3,2', 30000000) == 2578
assert play_game('2,1,3', 30000000) == 3544142
assert play_game('1,2,3', 30000000) == 261214
assert play_game('2,3,1', 30000000) == 6895259
assert play_game('3,2,1', 30000000) == 18
assert play_game('3,1,2', 30000000) == 362

print(play_game('15,5,1,4,7,0', 30000000))