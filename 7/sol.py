from collections import Counter

def get_hand_type(hand):
    count = Counter(hand)
    max_count, next_count = max(count.values()), -1
    if len(count.values()) > 1:
        max_count, next_count = sorted(count.values(), reverse=True)[:2]

    # Five of a kind
    if max_count == 5:
        return 7
    # Four of a kind
    if max_count == 4:
        return 6
    # Full house
    if max_count == 3 and next_count == 2:
        return 5
    # Three of a kind
    if max_count == 3:
        return 4
    # Two pairs
    if max_count == 2 and next_count == 2:
        return 3
    # One pair
    if max_count == 2:
        return 2
    # Junk
    return 1

def hand_key(handbid):
    values = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"][::-1]
    hand, bid = handbid
    type_ = get_hand_type(hand)
    order = [values.index(card) for card in hand]
    return (type_, order)

with open("input.txt", "r") as file:
    data = [line.split() for line in file.read().splitlines()]

data = list(sorted(data, key=hand_key))
score = 0
for i, handbid in enumerate(data):
    score += (i+1)*int(handbid[1])

print(score)