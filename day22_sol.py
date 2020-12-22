import copy

def read_input(path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.split('\n\n')

    player1 = data[0].split(':\n')[1]
    player1 = [int(p1.strip()) for p1 in player1.splitlines()]

    player2 = data[1].split(':\n')[1]
    player2 = [int(p2.strip()) for p2 in player2.splitlines()]

    return player1, player2

def calculate_score(winner_deck):
    score = 0
    for i, val in enumerate(winner_deck[::-1]):
        score += (i+1)*val

    return score

def play_game_1(player1, player2):
    while player1 and player2:
        p1 = player1.pop(0)
        p2 = player2.pop(0)

        if p1>p2:
            player1 += [p1, p2]
        else:
            player2 += [p2, p1]

    winner = player1 if player1 else player2

    return winner

def play_game_2(player1, player2):
    player1_history = set()
    player2_history = set()

    while player1 and player2:
        if (tuple(player1) in player1_history) and (tuple(player2) in player2_history):
            return 1, player1, player2

        player1_history.add(tuple(player1))
        player2_history.add(tuple(player2))

        p1 = player1.pop(0)
        p2 = player2.pop(0)

        if len(player1) >= p1 and len(player2) >= p2:
            winner, pp1, pp2 = play_game_2(copy.deepcopy(player1[:p1]), copy.deepcopy(player2[:p2]))
            if winner == 1:
                player1 += [p1, p2]
            else:
                player2 += [p2, p1]
        else:
            if p1>p2:
                player1 += [p1, p2]
            else:
                player2 += [p2, p1]
    
    if player1:
        return 1, player1, player2
    else:
        return 2, player1, player2


# Part 1

player1, player2 = read_input('day22')

winner_deck = play_game_1(player1, player2)

print(calculate_score(winner_deck))

# Part 2

player1, player2 = read_input('day22')

winner, player1, player2 = play_game_2(player1, player2)

if winner == 1:
    winner_deck = player1
else:
    winner_deck = player2

print(calculate_score(winner_deck))