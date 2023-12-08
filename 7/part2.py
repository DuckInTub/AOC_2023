from collections import Counter

def get_hand_type(hand):
    count = Counter(hand.replace("J", ""))
    J_count = len(["J" for char in hand if char == "J"])

    if not len(count.values()) > 1 or J_count == 5:
        return 7

    max_count, next_count = sorted(count.values(), reverse=True)[:2]
    max_count += J_count

    hand_types = [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (4, 1), (5, 0)]
    return hand_types.index((max_count, next_count))

def hand_key(handbid):
    values = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"][::-1]
    hand, bid = handbid
    t = get_hand_type(hand)
    order = [values.index(card) for card in hand]
    return (t, order)

with open("input.txt", "r") as file:
    data = [line.split() for line in file.read().splitlines()]

data = list(sorted(data, key=hand_key))
score = 0
for i, handbid in enumerate(data):
    score += (i+1)*int(handbid[1])

print(score)